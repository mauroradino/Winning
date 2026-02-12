from fastapi import FastAPI, BackgroundTasks, HTTPException
from typing import Optional
import os
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

app = FastAPI(title="Winning Transfer Simulator API")

# Configuración de CORS
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://winning-tu-usuario.vercel.app" # Agrega aquí tu URL de Vercel cuando la tengas
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

# Mock de endpoints adicionales para que no rompa la UI
@app.post("/api/ingest/{club}/{season}")
async def ingest_club_data(club: str, season: str):
    return {"message": "Ingesta no disponible en Serverless (Vercel). Use datos locales."}

@app.get("/api/simulate")
async def simulate_strategy(club: str, season: str, transfer_budget: float, salary_budget: float):
    return {
        "club": club,
        "net_financial_benefit": 0,
        "ai_summary": "Simulador en mantenimiento."
    }