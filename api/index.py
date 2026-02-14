from fastapi import FastAPI, BackgroundTasks, HTTPException
from typing import Optional
import os
import sys
import pandas as pd
import json
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import unicodedata
from pathlib import Path

# --- CONFIGURACIÓN DE RUTAS DINÁMICAS ---
# BASE_DIR apunta a la raíz del proyecto (donde está /datasets y /api)
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "datasets"

# Aseguramos que la raíz del proyecto esté en sys.path para poder importar `ia`
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

from ia.embeddings import ingest_data, query_rag, get_player_current_club
app = FastAPI(title="Winning Transfer Simulator API")




class RevenueRequest(BaseModel):
    club: str
    season: str
    transfer_budget: float

class PlayerValuationRequest(BaseModel):
    club: str
    season: str
    player: str

# Configuración de CORS
origins = [
    "http://localhost:5000",
    "http://127.0.0.1:5000",
    "https://winning-alpha.vercel.app/" 
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # En producción puedes restringirlo, para pruebas usamos "*"
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- ENDPOINTS ---

@app.get("/api/squad/{club}/{season}")
async def get_squad(club: str, season: str):
    file_path = DATA_PATH / club / season / f"{club}_{season}_players.csv"
    
    if file_path.exists():
        df = pd.read_csv(file_path)
        return {
            "status": "success",
            "source": "cache",
            "data": df.to_dict(orient="records")
        }
    
    raise HTTPException(status_code=404, detail=f"Datos no encontrados en {file_path}")

class TransfersData(BaseModel):
    club: str
    season: str

@app.post("/api/transfers")
def get_transfers(data: TransfersData):
    path_altas = DATA_PATH / data.club / data.season / f"{data.club}_{data.season}_altas.csv"
    path_bajas = DATA_PATH / data.club / data.season / f"{data.club}_{data.season}_bajas.csv"

    if not path_altas.exists() or not path_bajas.exists():
        raise HTTPException(status_code=404, detail="Archivos de transferencias no encontrados")

    df_altas = pd.read_csv(path_altas)
    df_bajas = pd.read_csv(path_bajas)

    for df in (df_altas, df_bajas):
        for col in df.select_dtypes(include=["int64", "float64"]).columns:
            df[col] = df[col].astype(float)

    return {
        "altas": df_altas.to_dict(orient="records"),
        "bajas": df_bajas.to_dict(orient="records"),
    }

@app.post("/api/transfers/revenue")
def revenue(data: RevenueRequest):
    path_altas = DATA_PATH / data.club / data.season / f"{data.club}_{data.season}_altas.csv"
    path_bajas = DATA_PATH / data.club / data.season / f"{data.club}_{data.season}_bajas.csv"

    if not path_altas.exists() or not path_bajas.exists():
        return {"net_benefit": 0, "budget_remaining": data.transfer_budget}

    df_altas = pd.read_csv(path_altas)
    df_bajas = pd.read_csv(path_bajas)

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
    path = DATA_PATH / data.club / data.season / f"{data.club}_{data.season}_valuations.csv"
    
    if not path.exists():
        raise HTTPException(status_code=404, detail="Valuaciones no encontradas")

    df_valuation = pd.read_csv(path)
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

class AgentMessage(BaseModel):
    from_role: str
    text: str


class AgentRequest(BaseModel):
    question: str
    history: list[AgentMessage] | None = None


@app.post("/api/agent")
async def query_agent(req: AgentRequest):
    """
    Endpoint principal del agente.
    - Tiene memoria breve (history) que se usa como parte de la pregunta.
    - Para preguntas del tipo '¿en qué club juega X?' usa lógica determinística con las valuaciones.
    """
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
    # 1. Usar la ruta segura con pathlib
    file_path = DATA_PATH / data.club / data.season / f"{data.club}_{data.season}_players.csv"
    
    if not file_path.exists():
        return {"error": "Archivo no encontrado", "path": str(file_path)}

    df = pd.read_csv(file_path)

    # 2. Filtrado robusto: normalizar y usar contains para ser más flexible
    search_name = normalize(data.name)
    
    # Aplicar filtro con contains (más flexible que ==)
    # Esto permite encontrar "Valentino Simoni" aunque haya espacios extra o diferencias sutiles
    filtered_data = df[df["nombre y apellido"].apply(lambda x: search_name in normalize(x))]

    # 3. Verificar si se encontró algo y convertir a diccionario
    if filtered_data.empty:
        return {"message": "Jugador no encontrado", "buscado": data.name, "status": "error"}

    # Retornamos el primer registro encontrado como un JSON válido
    return {
        "status": "success",
        "data": filtered_data.to_dict(orient="records")[0]
    }