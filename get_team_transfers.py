import requests
from bs4 import BeautifulSoup

def get_team_transfers(url: str, season: str):
    url = f"{url}{season}/pos//detailpos/0/w_s//plus/1#zugaenge"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    tabla_altas = []
    tabla_bajas = []
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error en la petición: {e}")
        return []

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        tables = soup.find_all('table', class_='items')
        
        if len(tables) < 2:
            print("No se encontraron ambas tablas de transferencias.")
            return []

        # --- PROCESAR ALTAS ---
        altas_rows = tables[0].find('tbody').find_all('tr', class_=['odd', 'even'])
        for item in altas_rows:
            name_tag = item.find('td', class_='hauptlink')
            name = name_tag.get_text(strip=True) if name_tag else "N/A"
            
            club_tag = item.find_all('td')[-2].find('a')
            from_club = club_tag['title'] if club_tag else "N/A"
            id = name_tag.find('a')['href'].split('/')[-1] if name_tag and name_tag.find('a') else "N/A"
            tabla_altas.append({"player_id": id, "player_name": name, "from_club": from_club})

        # --- PROCESAR BAJAS ---
        bajas_rows = tables[1].find('tbody').find_all('tr', class_=['odd', 'even'])
        for item in bajas_rows:
            name_tag = item.find('td', class_='hauptlink')
            name = name_tag.get_text(strip=True) if name_tag else "N/A"
            
            club_tag = item.find_all('td')[-2]
            club_name = club_tag.find('a') if club_tag else None
            if club_name:
                club_name = club_name['title']
            club_league = club_tag.find('img') if club_tag else None
            to_league = club_league['title'] if club_league else "N/A"

            id = name_tag.find('a')['href'].split('/')[-1] if name_tag and name_tag.find('a') else "N/A"
            tabla_bajas.append({"player_id": id, "player name": name, "to_club": club_name, "to_league": to_league})

        return tabla_altas, tabla_bajas
    else:
        print(f"Error al acceder: {response.status_code}")