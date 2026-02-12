from fastapi import FastAPI, BackgroundTasks, HTTPException
from typing import Optional
import os
import pandas as pd
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from main import team_data, transfer_data 
import unicodedata

app = FastAPI(title="Winning Transfer Simulator API")

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

# 2. Agregar el middleware a la aplicación
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,            # Permite tu puerto de Svelte
    allow_credentials=True,
    allow_methods=["*"],              # Permite todos los métodos (GET, POST, etc.)
    allow_headers=["*"],              # Permite todos los headers
)


DATA_PATH = "datasets"

@app.get("/api/squad/{club}/{season}")
async def get_squad(club: str, season: str):
    file_path = f"{DATA_PATH}/{club}/{season}/{club}_{season}_players.csv"
    
    # 1. Verificar si ya tenemos los datos (Cache en disco)
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        return {
            "status": "success",
            "source": "cache",
            "data": df.to_dict(orient="records")
        }
    
    # 2. Si no existen, informar que deben ser generados
    # Nota: Podrías disparar el scraper aquí automáticamente, 
    # pero para un challenge es mejor tener un endpoint de "ingesta" separado.
    raise HTTPException(status_code=404, detail="Datos no encontrados. Use el endpoint /api/ingest")

@app.post("/api/ingest/{club}/{season}")
async def ingest_club_data(club: str, season: str, background_tasks: BackgroundTasks):
    """
    Endpoint para disparar el scraper. 
    Usa BackgroundTasks para no bloquear al usuario mientras scrapea.
    """
    # Aquí llamarías a tus funciones del Ejercicio 1
    # background_tasks.add_task(team_data, club, season)
    # background_tasks.add_task(transfer_data, club, season)
    
    return {"message": f"Iniciando captura de datos para {club} {season}. Estarán listos en breve."}

@app.get("/api/simulate")
async def simulate_strategy(club: str, season: str, transfer_budget: float, salary_budget: float):
    """
    Endpoint base para el Ejercicio 2 (Simulador).
    Aquí es donde integrarás la IA más adelante.
    """
    # Lógica de simulación mock-up
    return {
        "club": club,
        "net_financial_benefit": 1500000, # Ejemplo
        "ai_summary": "La estrategia sugiere vender a jugadores veteranos para liberar presupuesto salarial."
    }


class TransfersData(BaseModel):
    club: str
    season: str

@app.post("/api/transfers")
def get_transfers(data: TransfersData):
    df_altas = pd.read_csv(
        f"./datasets/{data.club}/{data.season}/{data.club}_{data.season}_altas.csv"
    )
    df_bajas = pd.read_csv(
        f"./datasets/{data.club}/{data.season}/{data.club}_{data.season}_bajas.csv"
    )

    for df in (df_altas, df_bajas):
        for col in df.select_dtypes(include=["int64", "float64"]).columns:
            df[col] = df[col].astype(float)

    return {
        "altas": df_altas.to_dict(orient="records"),
        "bajas": df_bajas.to_dict(orient="records"),
    }


class RevenueRequest(BaseModel):
    club: str
    season: str
    transfer_budget: float


@app.post("/api/transfers/revenue")
def revenue(data: RevenueRequest):
    df_altas = pd.read_csv(
        f"./datasets/{data.club}/{data.season}/{data.club}_{data.season}_altas.csv"
    )
    df_bajas = pd.read_csv(
        f"./datasets/{data.club}/{data.season}/{data.club}_{data.season}_bajas.csv"
    )

    total_spent = pd.to_numeric(df_altas["amount"], errors="coerce").fillna(0).sum()
    total_income = pd.to_numeric(df_bajas["amount"], errors="coerce").fillna(0).sum()

    net_benefit = float(total_income - total_spent)
    budget_remaining = float(data.transfer_budget - total_spent + total_income)

    return {
        "net_benefit": net_benefit,
        "budget_remaining": budget_remaining,
    }



def normalize(text: str) -> str:
    if not isinstance(text, str):
        return ""
    # Quita acentos y pasa a minúsculas
    text_nfkd = unicodedata.normalize("NFD", text)
    without_accents = "".join(c for c in text_nfkd if unicodedata.category(c) != "Mn")
    return without_accents.lower()

class PlayerValuationRequest(BaseModel):
    club: str
    season: str
    player: str

@app.post("/api/valuations")
def get_player_valuation(data: PlayerValuationRequest):
    path = f"./datasets/{data.club}/{data.season}/{data.club}_{data.season}_valuations.csv"
    df_valuation = pd.read_csv(path)

    player_query = normalize(data.player)

    def row_match(row):
        player_name_norm = normalize(row.get("nombre_jugador", ""))
        return player_query in player_name_norm

    mask = df_valuation.apply(row_match, axis=1)
    result = df_valuation.loc[mask, ["valuation_amount", "valuation_date"]]

    return result.to_dict(orient="records")