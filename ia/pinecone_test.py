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
    if index is None:
        print("⚠️ Ingesta deshabilitada: faltan variables de entorno.")
        return

    csv_types = ["altas", "bajas", "players", "valuations"]
    
    for csv_type in csv_types:
        file_path = f"../datasets/{club}/{season}/{club}_{season}_{csv_type}.csv"
        if not os.path.exists(file_path): continue
            
        loader = CSVLoader(file_path=file_path, encoding="utf-8")
        documents = loader.load()
        
        vectors_to_upsert = []

        for i, doc in enumerate(documents):
            row_text = doc.page_content.replace('\ufeff', '').replace('\n', ', ')
            clean_content = f"[tipo={csv_type} club={club} season={season}] {row_text}"

            embedding = client.embeddings.create(
                input=clean_content,
                model="text-embedding-3-small"
            ).data[0].embedding

            vectors_to_upsert.append({
                "id": f"{club}_{season}_{csv_type}_{i}",
                "values": embedding,
                "metadata": {
                    "text": clean_content, 
                    "tipo": csv_type,
                    "club": club,
                    "season": season
                }
            })

        if vectors_to_upsert:
            index.upsert(vectors=vectors_to_upsert)
    
    print(f"✅ Ingesta en Pinecone completada para {club} {season}")

def query_rag(question):
    if index is None or client is None:
        raise RuntimeError("RAG no disponible: faltan API Keys.")

    query_vector = client.embeddings.create(
        input=question,
        model="text-embedding-3-small"
    ).data[0].embedding

    results = index.query(
        vector=query_vector,
        top_k=5,
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
                    "Eres un asistente experto en finanzas de Boca Juniors. "
                    "Usa exclusivamente el CONTEXTO provisto. "
                    "Si la respuesta no está, di: 'No encuentro esa información en los datos disponibles.'"
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