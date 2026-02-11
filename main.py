import os
import json
import pandas as pd
from get_teams_players import get_players
from get_team_transfers import get_team_transfers
from get_valuations import get_all_team_valuations
import requests

with open("urls.json", "r") as f:
    urls = json.load(f)

def ensure_directory(club: str, temporada: str):
    path = f"datasets/{club}/{temporada}"
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Carpeta creada: {path}")
    return path

def team_data(club: str, temporada: str):
    path = ensure_directory(club, temporada)
    players = get_players(urls[club]["players"] + temporada)

    if players:
        df = pd.DataFrame(players)
        df.to_csv(f"{path}/{club}_{temporada}_players.csv", index=False, header=True, encoding="utf-8-sig")
        print(f"Datos de jugadores guardados en {path}")
        
        # CAMBIO AQUÍ: Usamos la función que recorre la lista
        total_valuations = get_all_team_valuations(players) 
        
        df_valuations = pd.DataFrame(total_valuations)
        df_valuations.to_csv(f"{path}/{club}_{temporada}_valuations.csv", index=False, header=True, encoding="utf-8-sig")
        print(f"Valoraciones guardadas en {path}")

def transfer_data(club: str, temporada: str):
    path = ensure_directory(club, temporada)
    player_info = get_team_transfers(urls[club]["transfers"], temporada)
    

    if player_info and len(player_info) == 2:
        tabla_altas, tabla_bajas = player_info
        df_altas = pd.DataFrame(tabla_altas)
        df_bajas = pd.DataFrame(tabla_bajas)
        
        df_altas.to_csv(f"{path}/{club}_{temporada}_altas.csv", index=False, header=True, encoding="utf-8-sig")
        df_bajas.to_csv(f"{path}/{club}_{temporada}_bajas.csv", index=False, header=True, encoding="utf-8-sig")
        print(f"Transferencias guardadas en {path}")

if __name__ == "__main__":
    club = input("Ingrese el nombre del club: ").lower()
    temporada = input("Ingrese el año de inicio de la temporada (ej: 2024): ")
    
    if club in urls:
        transfer_data(club, temporada)
        team_data(club, temporada)
    else:
        print("Club no encontrado en urls.json")