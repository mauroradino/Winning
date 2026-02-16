import os
from pinecone import Pinecone
from langchain_community.document_loaders.csv_loader import CSVLoader
from openai import OpenAI
import tempfile
import sys
from dotenv import load_dotenv
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from api.aws_s3 import read_aws_csv
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
INDEX_NAME = "winning" 

if OPENAI_API_KEY and PINECONE_API_KEY:
    client = OpenAI(api_key=OPENAI_API_KEY)
    pc = Pinecone(api_key=PINECONE_API_KEY)
    index = pc.Index(INDEX_NAME)
else:
    client = None
    index = None

def ingest_data(club, season):
    if index is None or client is None:
        print("❌ Error: Configuración de IA no disponible.")
        return

    csv_types = ["altas", "bajas", "players", "valuations"]
    print(f"☁️ Iniciando ingesta desde S3 (vía Pandas) para: {club.upper()} {season}")

    for csv_type in csv_types:
        s3_path = f"datasets/{club.lower()}/{season}/{club.lower()}_{season}_{csv_type}.csv"
        
        df = read_aws_csv(s3_path)
        
        if df is not None:
            try:
                csv_text = df.to_csv(index=False, encoding="utf-8-sig")
                
                with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix=".csv", encoding="utf-8-sig") as f:
                    f.write(csv_text)
                    temp_path = f.name

                loader = CSVLoader(file_path=temp_path, encoding="utf-8-sig")
                documents = loader.load()
                os.remove(temp_path) 

                all_vectors = []
                for i, doc in enumerate(documents):
                    row_text = doc.page_content.replace('\n', ', ').strip()
                    clean_content = f"[tipo={csv_type} club={club.lower()} season={season}] {row_text}"

                    embedding = client.embeddings.create(
                        input=clean_content,
                        model="text-embedding-3-small"
                    ).data[0].embedding

                    all_vectors.append({
                        "id": f"{club.lower()}_{season}_{csv_type}_{i}",
                        "values": embedding,
                        "metadata": {
                            "text": clean_content, 
                            "tipo": csv_type, 
                            "club": club.lower(), 
                            "season": str(season) 
                        }
                    })

                batch_size = 100
                for j in range(0, len(all_vectors), batch_size):
                    index.upsert(vectors=all_vectors[j : j + batch_size])
                
                print(f"✅ {csv_type.capitalize()} de {club} {season} ingestado correctamente.")

            except Exception as e:
                print(f"❌ Error procesando el DataFrame de {csv_type}: {e}")
        else:
            print(f"⚠️ No se pudo obtener el DataFrame para {s3_path}")

    print(f"🏁 Finalizada ingesta de {club} {season}.")

def query_rag(question):
    if index is None or client is None:
        raise RuntimeError("RAG no disponible: faltan API Keys.")

    query_vector = client.embeddings.create(
        input=question,
        model="text-embedding-3-small"
    ).data[0].embedding

    results = index.query(
        vector=query_vector,
        top_k=10,
        include_metadata=True
    )

    matches = results.get('matches', [])
    if not matches:
        return "No encuentro esa información en los datos disponibles."

    context = "\n".join([m['metadata']['text'] for m in matches])

    response = client.chat.completions.create(
        model="gpt-4o",
        temperature=0.0,
        messages=[
    {
        "role": "system",
        "content": (
            "Eres un experto en el mercado de pases de Boca Juniors. "
            "En el CONTEXTO verás datos con etiquetas como [tipo=valuations]. "
            "Si el usuario pregunta por el valor de un jugador en una fecha específica, "
            "busca en las líneas de 'tipo=valuations' y extrae el 'valuation_amount'. "
            "No seas excesivamente estricto con el formato de la fecha; si el usuario dice '12 de diciembre' "
            "y en el contexto dice '2024-12-12', relaciónalos correctamente. "
            "Si el dato está ahí, dalo. Solo si NO existe ninguna mención al jugador o al valor, "
            "di: 'No encuentro esa información en los datos disponibles.'"
        )
    },
    {"role": "user", "content": f"CONTEXTO:\n{context}\n\nPREGUNTA: {question}"}
]
    )
    return response.choices[0].message.content.strip()

def get_player_current_club(player_name: str) -> str:
    """
    Obtiene el club actual de un jugador usando metadatos y búsqueda semántica en Pinecone.
    Filtra los resultados para buscar específicamente en documentos de tipo 'valuations'.
    """
    if index is None or client is None:
        return "Servicio de datos no disponible."

    query_vector = client.embeddings.create(
        input=player_name,
        model="text-embedding-3-small"
    ).data[0].embedding

    results = index.query(
        vector=query_vector,
        top_k=10,
        include_metadata=True,
        filter={
            "tipo": {"$eq": "valuations"}
        }
    )

    matches = results.get('matches', [])
    if not matches:
        return "No encuentro esa información en los datos disponibles."

    candidatos = []
    for match in matches:
        line = match['metadata']['text']
        
        if "]" in line:
            row_text = line.split("]", 1)[1].strip()
        else:
            row_text = line

        parts = [p.strip() for p in row_text.split(",")]
        
        if len(parts) < 7:
            continue

        nombre_en_data = parts[1]
        fecha_valuacion = parts[3]
        club_nombre = parts[-1]

        if player_name.lower() in nombre_en_data.lower():
            candidatos.append((fecha_valuacion, club_nombre))

    if not candidatos:
        return "No encuentro esa información en los datos disponibles."

    candidatos.sort(key=lambda x: x[0])
    _, club_actual = candidatos[-1]
    
    return club_actual

def get_season_summary(club, season):
    print(club, season)
    busquedas = [
        {"q": f"Ventas y bajas de {club} en {season}", "tipos": ["bajas"]},
        {"q": f"Compras y altas de {club} en {season}", "tipos": ["altas"]},
        {"q": f"Plantilla y jugadores de {club} en {season}", "tipos": ["players", "valuations"]}
    ]
    
    contexto_total = []
    
    for item in busquedas:
        query_vector = client.embeddings.create(
            input=item["q"], 
            model="text-embedding-3-small"
        ).data[0].embedding
        res = index.query(
            vector=query_vector,
            top_k=40, 
            filter={
                "club": {"$eq": club.lower()}, 
                "season": {"$eq": str(season)}, 
                "tipo": {"$in": item["tipos"]} 
            },
            include_metadata=True
        )
        contexto_total.extend([m['metadata']['text'] for m in res['matches']])

    context_str = "\n".join(list(set(contexto_total)))

    response = client.chat.completions.create(
        model="gpt-4o",
        temperature=0, 
        messages=[
            {
                "role": "system", 
                "content": (
                    "Eres un analista financiero deportivo de alto nivel. "
                    "Tu objetivo es realizar un balance contable exacto de la temporada. "
                    "Suma todos los montos de 'altas' para obtener el gasto total. "
                    "Suma todos los montos de 'bajas' para obtener el ingreso total. "
                    "Resta Gastos de Ingresos para el Balance Neto. "
                    "Presenta los datos en un formato profesional y legible."
                )
            },
            {"role": "user", "content": f"DATOS DE LA TEMPORADA:\n{context_str}\n\nPregunta: Resume el balance financiero, jugadores clave y bajas."}
        ]
    )
    return response.choices[0].message.content