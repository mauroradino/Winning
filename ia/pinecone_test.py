import os
from pinecone import Pinecone
from langchain_community.document_loaders.csv_loader import CSVLoader
from openai import OpenAI
from dotenv import load_dotenv

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
    if index is None: return

    csv_types = ["altas", "bajas", "players", "valuations"]
    
    for csv_type in csv_types:
        file_path = f"../datasets/{club}/{season}/{club}_{season}_{csv_type}.csv"
        if not os.path.exists(file_path): continue
            
        loader = CSVLoader(file_path=file_path, encoding="utf-8")
        documents = loader.load()
        
        all_vectors = []

        for i, doc in enumerate(documents):
            row_text = doc.page_content.replace('\ufeff', '').replace('\n', ', ')
            clean_content = f"[tipo={csv_type} club={club} season={season}] {row_text}"

            embedding = client.embeddings.create(
                input=clean_content,
                model="text-embedding-3-small"
            ).data[0].embedding

            # ✅ CORRECCIÓN DE METADATOS:
            # Usamos 'season' en lugar de 'temporada' para coincidir con get_season_summary
            # Usamos .lower() en club para evitar errores de mayúsculas
            all_vectors.append({
                "id": f"{club}_{season}_{csv_type}_{i}",
                "values": embedding,
                "metadata": {
                    "text": clean_content, 
                    "tipo": csv_type, 
                    "club": club.lower(), 
                    "season": str(season) 
                }
            })

        batch_size = 100
        for i in range(0, len(all_vectors), batch_size):
            batch = all_vectors[i : i + batch_size]
            index.upsert(vectors=batch)
            print(f"📦 Enviado lote de {len(batch)} vectores ({csv_type})")
    
    print(f"✅ Ingesta total completada con éxito con metadatos 'season'.")

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

    # 1. Generamos el embedding del nombre del jugador
    query_vector = client.embeddings.create(
        input=player_name,
        model="text-embedding-3-small"
    ).data[0].embedding

    # 2. Buscamos en Pinecone aplicando un FILTRO de metadatos
    # Esto asegura que solo traiga datos del archivo 'valuations'
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
        # Extraemos el texto que guardamos en la ingesta
        line = match['metadata']['text']
        
        # Quitamos los metadatos visuales [tipo=... club=... season=...]
        if "]" in line:
            row_text = line.split("]", 1)[1].strip()
        else:
            row_text = line

        # Parseamos la fila del CSV (id, nombre, monto, fecha, edad, club_id, club_nombre)
        parts = [p.strip() for p in row_text.split(",")]
        
        if len(parts) < 7:
            continue

        nombre_en_data = parts[1]
        fecha_valuacion = parts[3] # Formato YYYY-MM-DD
        club_nombre = parts[-1]

        # Verificamos que el nombre coincida (por si el embedding trajo a otro jugador similar)
        if player_name.lower() in nombre_en_data.lower():
            candidatos.append((fecha_valuacion, club_nombre))

    if not candidatos:
        return "No encuentro esa información en los datos disponibles."

    # 3. Ordenamos por fecha (el primer elemento de la tupla) y devolvemos el último
    candidatos.sort(key=lambda x: x[0])
    _, club_actual = candidatos[-1]
    
    return club_actual

def get_season_summary(club, season):
    # Definimos búsquedas específicas para cubrir todos los ángulos
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
            top_k=40, # Ajustamos para no saturar pero asegurar cobertura
            filter={
                "club": {"$eq": club.lower()}, # Usamos la variable
                "season": {"$eq": str(season)}, # Aseguramos que sea string
                "tipo": {"$in": item["tipos"]} # Filtramos por el tipo específico de la sub-query
            },
            include_metadata=True
        )
        contexto_total.extend([m['metadata']['text'] for m in res['matches']])

    # Limpieza de duplicados
    context_str = "\n".join(list(set(contexto_total)))

    response = client.chat.completions.create(
        model="gpt-4o",
        temperature=0, # Importante: 0 para cálculos matemáticos precisos
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