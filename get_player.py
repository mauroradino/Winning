import requests
from bs4 import BeautifulSoup
import pandas as pd


def get_player(player_name: str):
    # Configuración de headers para evitar bloqueos del servidor [cite: 82, 184]
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        response = requests.get(f"https://www.transfermarkt.com.ar/schnellsuche/ergebnis/schnellsuche?query={player_name}", headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error en la petición: {e}")
        return []
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        items_table = soup.find('table', class_='items')
        if not items_table:
            print("No se encontró la tabla de jugadores.")
            return []
            
        body = items_table.find('tbody')
        rows = body.find_all('tr')
        for row in rows:
            table = row.find('table', class_='inline-table')
            tbody = table.find('tbody')