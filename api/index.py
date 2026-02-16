from fastapi import FastAPI, BackgroundTasks
import sys
import pandas as pd
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import unicodedata
from pathlib import Path
from .aws_s3 import read_aws_csv

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "datasets"

if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

from ia.pinecone_test import ingest_data, get_season_summary
#from ia.embeddings import ingest_data, query_rag, get_player_current_club
app = FastAPI(title="Winning Transfer Simulator API")


class RevenueRequest(BaseModel):
    club: str
    season: str
    transfer_budget: float

class PlayerValuationRequest(BaseModel):
    club: str
    season: str
    player: str

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://winning-alpha.vercel.app/" 
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- ENDPOINTS ---
@app.get("/api/squad/{club}/{season}")
async def get_squad(club: str, season: str):
    df = read_aws_csv(f"datasets/{club}/{season}/{club}_{season}_players.csv")
    df_clean = df.astype(object).replace({pd.NA: None, float('nan'): None})
    
    return {
        "status": "success",
        "source": "cache",
        "data": df_clean.to_dict(orient="records")
    }

class TransfersData(BaseModel):
    club: str
    season: str

@app.post("/api/transfers")
def get_transfers(data: TransfersData):
    df_altas = read_aws_csv(f"datasets/{data.club}/{data.season}/{data.club}_{data.season}_altas.csv")
    df_bajas = read_aws_csv(f"datasets/{data.club}/{data.season}/{data.club}_{data.season}_bajas.csv")

    for df in (df_altas, df_bajas):
        for col in df.select_dtypes(include=["int64", "float64"]).columns:
            df[col] = df[col].astype(float)
    df.replace({float('nan'): None}, inplace=True)
    return {
        "altas": df_altas.to_dict(orient="records"),
        "bajas": df_bajas.to_dict(orient="records"),
    }

@app.post("/api/transfers/revenue")
def revenue(data: RevenueRequest):
    df_altas = read_aws_csv(f"datasets/{data.club}/{data.season}/{data.club}_{data.season}_altas.csv")
    df_bajas = read_aws_csv(f"datasets/{data.club}/{data.season}/{data.club}_{data.season}_bajas.csv")

    total_spent = pd.to_numeric(df_altas["amount"], errors="coerce").fillna(0).sum()
    total_income = pd.to_numeric(df_bajas["amount"], errors="coerce").fillna(0).sum()

    net_benefit = float(total_income - total_spent)
    budget_remaining = float(data.transfer_budget - total_spent + total_income)

    return {
        "net_benefit": net_benefit,
        "budget_remaining": budget_remaining,
        "total_spent": float(total_spent),
        "total_income": float(total_income),
    }

@app.post("/api/valuations")
def get_player_valuation(data: PlayerValuationRequest):
    df_valuation = read_aws_csv(f"datasets/{data.club}/{data.season}/{data.club}_{data.season}_valuations.csv")
    player_query = normalize(data.player)

    def row_match(row):
        player_name_norm = normalize(str(row.get("nombre_jugador", "")))
        return player_query in player_name_norm

    mask = df_valuation.apply(row_match, axis=1)
    result = df_valuation.loc[mask, ["valuation_amount", "valuation_date"]]

    return result.to_dict(orient="records")

# --- MODELOS Y UTILIDADES ---

class TransfersData(BaseModel):
    club: str
    season: str

class RevenueRequest(BaseModel):
    club: str
    season: str
    transfer_budget: float

class PlayerValuationRequest(BaseModel):
    club: str
    season: str
    player: str

def normalize(text: str) -> str:
    if not isinstance(text, str):
        return ""
    text_nfkd = unicodedata.normalize("NFD", text)
    without_accents = "".join(c for c in text_nfkd if unicodedata.category(c) != "Mn")
    return without_accents.lower()

# Endpoint para lanzar la ingesta de datos en segundo plano
@app.post("/api/ingest/{club}/{season}")
async def ingest_club_data(club: str, season: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(ingest_data, club, season)
    return {"message": f"Ingesta lanzada para {club} {season}"}
 

@app.post("/api/summary/{club}/{season}")
async def generate_summary(club: str, season: str):
    res = get_season_summary(club, season)
    return res

class AgentMessage(BaseModel):
    from_role: str
    text: str


class AgentRequest(BaseModel):
    question: str
    history: list[AgentMessage] | None = None


""" @app.post("/api/agent")
async def query_agent(req: AgentRequest):
    Endpoint principal del agente.
    - Tiene memoria breve (history) que se usa como parte de la pregunta.
    - Para preguntas del tipo '¿en qué club juega X?' usa lógica determinística con las valuaciones.
    question = req.question.strip()
    q_lower = question.lower()

    # 1. Caso especial: club actual de un jugador (usando sólo CSV de valuaciones)
    if "en que club juega" in q_lower or "en qué club juega" in q_lower or "club actual" in q_lower:
        # Tomamos todo lo que viene después de 'juega' como nombre aproximado
        if "juega" in q_lower:
            idx = q_lower.rfind("juega")
            raw_name = question[idx + len("juega") :].strip(" ?.,")
        else:
            raw_name = question.strip(" ?.,")

        club_actual = get_player_current_club(raw_name)
        if club_actual == "No encuentro esa información en los datos disponibles.":
            return {"answer": club_actual}

        return {"answer": f"{raw_name} juega actualmente en {club_actual}."}

    # 2. Construimos una pregunta enriquecida con el historial (memoria de conversación)
    history_text = ""
    if req.history:
        partes = []
        for m in req.history:
            rol = "Usuario" if m.from_role == "user" else "Agente"
            partes.append(f"{rol}: {m.text}")
        history_text = "\n".join(partes)

    if history_text:
        full_question = f"Historial de conversación:\n{history_text}\n\nPregunta actual: {question}"
    else:
        full_question = question

    answer = query_rag(full_question)
    return {"answer": answer}
 """

@app.get("/api/simulate")
async def simulate_strategy(club: str, season: str, transfer_budget: float, salary_budget: float):
    return {
        "club": club,
        "net_financial_benefit": 0,
        "ai_summary": "Simulador en mantenimiento."
    }


class PlayerRequest(BaseModel):
    name:str
    club:str
    season:str

def normalize(text):
    """Normaliza texto: quita acentos y pasa a minúsculas"""
    if pd.isna(text) or text is None:
        return ""
    text_str = str(text)
    text_nfkd = unicodedata.normalize("NFD", text_str)
    without_accents = "".join(c for c in text_nfkd if unicodedata.category(c) != "Mn")
    return without_accents.lower().strip()

@app.post("/api/playerInfo")
async def get_player_info(data: PlayerRequest):
    df = read_aws_csv(f"datasets/{data.club}/{data.season}/{data.club}_{data.season}_players.csv")

    if df is None:
        return {
            "status": "error",
            "message": f"No se pudo cargar la base de datos para {data.club} en la temporada {data.season}"
        }

    search_name = normalize(data.name)
    
    filtered_data = df[df["nombre y apellido"].apply(lambda x: search_name in normalize(str(x)) if x else False)]

    if filtered_data.empty:
        return {"message": "Jugador no encontrado", "buscado": data.name, "status": "error"}

    clean_data = filtered_data.replace({float('nan'): None}).to_dict(orient="records")[0]

    return {
        "status": "success",
        "data": clean_data
    }