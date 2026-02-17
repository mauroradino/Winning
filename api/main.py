import json
import pandas as pd
from get_teams_players import get_players
from get_team_transfers import get_team_transfers
from get_valuations import get_all_team_valuations
from salaries_scrapper import get_salaries
from .aws_s3 import upload_file
import math 
import time 

with open("urls.json", "r") as f:
    urls = json.load(f)

def team_data(club: str, temporada: str):
    players = get_players(urls[club]["players"] + temporada)

    if players:
        df = pd.DataFrame(players)
        
        salarios = get_salaries(club, temporada)
        if not salarios.empty:
            salarios['sueldo_anual'] = pd.to_numeric(salarios['sueldo_anual'], errors='coerce').fillna(0)
            complete_df = pd.merge(df, salarios, left_on="nombre y apellido", right_on="nombre", how='left')
            complete_df.drop(columns=["nombre"], inplace=True)
            complete_df['sueldo_anual'] = complete_df['sueldo_anual'].fillna(0)
        else:
            df['sueldo_anual'] = 0
            complete_df = df
        
        upload_file(complete_df, f"datasets/{club}/{temporada}/{club}_{temporada}_players.csv")
                    
        print(f"Datos de jugadores guardados en datasets/{club}/{temporada}/{club}_{temporada}_players.csv")
        total_valuations = get_all_team_valuations(players) 
        clean_valuations = [{k: (v if not (isinstance(v, float) and math.isnan(v)) else 0) for k, v in d.items()}for d in total_valuations]
        df_valuations = pd.DataFrame(clean_valuations)
        upload_file(df_valuations,f"datasets/{club}/{temporada}/{club}_{temporada}_valuations.csv")
        print(f"Valoraciones guardadas en datasets/{club}/{temporada}/{club}_{temporada}_valuations.csv")

def transfer_data(club: str, temporada: str):
    player_info = get_team_transfers(urls[club]["transfers"], temporada)
    

    if player_info and len(player_info) == 2:
        tabla_altas, tabla_bajas = player_info
        df_altas = pd.DataFrame(tabla_altas)
        df_bajas = pd.DataFrame(tabla_bajas)
        
        upload_file(df_altas, f"datasets/{club}/{temporada}/{club}_{temporada}_altas.csv")
        upload_file(df_bajas, f"datasets/{club}/{temporada}/{club}_{temporada}_bajas.csv")
        print(f"Transferencias guardadas en datasets/{club}/{temporada}")

if __name__ == "__main__":
    clubes = list(urls.keys())
    temporadas = ["2020", "2021", "2022", "2023", "2024", "2025"]
    
    for club in clubes:
        print(f"--- Procesando Club: {club.upper()} ---")
        for temporada in temporadas:
            try:
                print(f"Extrayendo datos de {club} - Temporada {temporada}...")
                transfer_data(club, temporada)
                team_data(club, temporada)
                time.sleep(2) 
                
            except Exception as e:
                print(f"❌ Error procesando {club} en {temporada}: {e}")
                continue 
    
    print("✅ Proceso de scraping finalizado para todos los clubes.")