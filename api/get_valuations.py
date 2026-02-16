import requests
import time
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

club_cache = {}

def get_session():
    session = requests.Session()
    retry_strategy = Retry(
        total=3, 
        backoff_factor=2, 
        status_forcelist=[429, 500, 502, 503, 504], 
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "es-ES,es;q=0.9",
        "Connection": "keep-alive"
    })
    return session

session = get_session()

def get_club_name_by_id(club_id):
    if not club_id or str(club_id) in ["0", "N/A", "None"]:
        return "Sin Club / Desconocido"
    
    club_id_str = str(club_id)
    if club_id_str in club_cache:
        return club_cache[club_id_str]

    try:
        url = f"https://www.transfermarkt.es/codigoz/startseite/verein/{club_id_str}"
        response = session.get(url, timeout=15)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            h1_name = soup.find('h1', class_='data-header__headline-wrapper')
            
            if h1_name:
                name = h1_name.get_text(strip=True)
                club_cache[club_id_str] = name
                return name
                
    except Exception as e:
        print(f"Error obteniendo nombre del club {club_id}: {e}")
            
    return f"Club {club_id}"

def get_valuations(player_id, player_name):
    url = f"https://tmapi-alpha.transfermarkt.technology/player/{player_id}/market-value-history"
    try:
        response = session.get(url, timeout=10)
        if response.status_code != 200:
            return []
        
        data = response.json()
        if not data.get('success') or 'data' not in data or 'history' not in data['data']:
            return []
            
        history_raw = data['data']['history']
        valuations_parsed = []
        
        for entry in history_raw:
            c_id = entry.get('clubId')
            
            c_nombre = get_club_name_by_id(c_id)
            
            valuations_parsed.append({
                "player_id": player_id,
                "nombre_jugador": player_name, 
                "valuation_amount": entry['marketValue']['value'], 
                "valuation_date": entry['marketValue']['determined'],
                "age_at_valuation": entry['age'],
                "club_id": c_id,
                "club_nombre": c_nombre
            })
            
        return valuations_parsed

    except Exception as e: 
        print(f"Error fetching valuations for player {player_id}: {e}")
        return []

def get_all_team_valuations(players_list):
    all_history = []
    print(f"Iniciando extracción de valoraciones para {len(players_list)} jugadores...")
    start_time = time.time()
    
    for player in players_list:
        p_id = player.get("player_id")
        p_name = player.get("nombre y apellido")
        
        if p_id and p_id != "N/A":
            historial_jugador = get_valuations(p_id, p_name)
            all_history.extend(historial_jugador)
            time.sleep(0.3) 
    
    end_time = time.time()
    print(f"Finalizado en {round(end_time - start_time, 2)} segundos.")
    return all_history