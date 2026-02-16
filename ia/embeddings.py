import os
import chromadb
from chromadb.utils import embedding_functions
from langchain_community.document_loaders.csv_loader import CSVLoader
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")

if API_KEY:
    client = OpenAI(api_key=API_KEY)

    openai_ef = embedding_functions.OpenAIEmbeddingFunction(
        api_key=API_KEY,
        model_name="text-embedding-3-small"
    )

    chroma_client = chromadb.Client()  
    collection = chroma_client.get_or_create_collection(
        name="boca_juniors_data",
        embedding_function=openai_ef
    )
else:
    client = None
    openai_ef = None
    chroma_client = None
    collection = None


def ingest_data(club, season):
    if collection is None:
        print("⚠️ Ingesta deshabilitada: falta OPENAI_API_KEY en el entorno (.env).")
        return
    csv_types = ["altas", "bajas", "players", "valuations"]

    for csv_type in csv_types:
        file_path = f"../datasets/{club}/{season}/{club}_{season}_{csv_type}.csv"
        
        if not os.path.exists(file_path):
            continue
            
        loader = CSVLoader(file_path=file_path, encoding="utf-8")
        documents = loader.load()
        
        clean_rows = []
        row_ids = []
        metadatas = []

        for i, doc in enumerate(documents):
            row_text = doc.page_content.replace('\ufeff', '').replace('\n', ', ')
            clean_content = f"[tipo={csv_type} club={club} season={season}] {row_text}"

            clean_rows.append(clean_content)
            row_ids.append(f"{csv_type}_{i}")
            metadatas.append({"tipo": csv_type, "club": club, "season": season})

        collection.add(
            documents=clean_rows,
            ids=row_ids,
            metadatas=metadatas
        )
    
    print(f"✅ Ingesta completada para {club} {season}")


def get_player_current_club(player_name: str) -> str:
    if collection is None:
        return "No encuentro esa información en los datos disponibles."

    results = collection.query(
        query_texts=[player_name],
        n_results=10,
        where={"tipo": "valuations"},
    )

    docs = results.get("documents", [[]])
    if not docs or not docs[0]:
        return "No encuentro esa información en los datos disponibles."

    candidatos = []
    for line in docs[0]:
        if "]" in line:
            row_text = line.split("]", 1)[1].strip()
        else:
            row_text = line

        parts = [p.strip() for p in row_text.split(",")]
        if len(parts) < 7:
            continue

        nombre = parts[1]
        fecha = parts[3]
        club_nombre = parts[-1]

        if player_name.lower() in nombre.lower():
            candidatos.append((fecha, club_nombre))

    if not candidatos:
        return "No encuentro esa información en los datos disponibles."

    candidatos.sort(key=lambda x: x[0])  
    _, club_actual = candidatos[-1]
    return club_actual


def query_rag(question):
    if collection is None or client is None:
        raise RuntimeError("RAG no disponible: falta OPENAI_API_KEY en el entorno (.env).")
    results = collection.query(
        query_texts=[question],
        n_results=5
    )
    
    docs = results.get('documents', [[]])
    if not docs or not docs[0]:
        return "No encuentro esa información en los datos disponibles."

    context = "\n".join(docs[0])

    response = client.chat.completions.create(
        model="gpt-4o",
        temperature=0.0,
        messages=[
            {
                "role": "system",
                "content": (
                    "Eres un asistente experto en finanzas y mercado de pases. "
                    "Cada línea de CONTEXTO puede comenzar con metadatos del tipo "
                    "[tipo=... club=... season=...]. "
                    "Cuando te pregunten en qué club juega un jugador, toma el valor de 'club=' "
                    "de esos metadatos como club actual de referencia, incluso si en el texto "
                    "aparecen otros clubes históricos. "
                    "No inventes datos y SOLO puedes responder usando EXCLUSIVAMENTE la información "
                    "del CONTEXTO que se te provee. "
                    "Si la respuesta no está claramente en el contexto, responde exactamente: "
                    "'No encuentro esa información en los datos disponibles.'"
                ),
            },
            {
                "role": "user",
                "content": f"CONTEXTO:\n{context}\n\nPREGUNTA: {question}",
            },
        ],
    )
    return response.choices[0].message.content.strip()

