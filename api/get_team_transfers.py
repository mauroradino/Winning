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
            tds = item.find_all('td')
            from_club = "N/A"
            amount_numeric = 0 
            
            if len(tds) > 12:
                td_amount = tds[12]
                precio_sesion = td_amount.find('i', class_="normaler-text")
                if precio_sesion:
                    amount_text = precio_sesion.get_text(strip=True)
                    clean_amount = amount_text.replace("€", "").replace(".", "").replace(",", ".").strip()
                    try:
                        if "mill" in clean_amount:
                            val = float(clean_amount.split("mill")[0].strip())
                            amount_numeric = int(val * 1000000)
                        elif "mil" in clean_amount:
                            val = float(clean_amount.split("mil")[0].strip())
                            amount_numeric = int(val * 1000)
                        elif "Libre" in amount_text or "coste" in amount_text:
                            amount_numeric = "Libre / Cesión"
                        else:
                            amount_numeric = "Libre / Cesión"
                    except (ValueError, IndexError):
                        amount_numeric = 0
                else:
                    amount_link = td_amount.find('a')
                    if amount_link:
                        amount = amount_link.get_text(strip=True)
                        if amount:
                            clean_amount = amount.replace("€", "").replace(".", "").replace(",", ".").strip()
                            try:
                                if "mill" in clean_amount:
                                    val = float(clean_amount.split("mill")[0].strip())
                                    amount_numeric = int(val * 1000000)
                                elif "mil" in clean_amount:
                                    val = float(clean_amount.split("mil")[0].strip())
                                    amount_numeric = int(val * 1000)
                                elif "Libre" in amount or "coste" in amount:
                                    amount_numeric = "Libre / Cesión"
                                else:
                                    amount_numeric = "Libre / Cesión"
                            except (ValueError, IndexError):
                                amount_numeric = 0

            if len(tds) > 8:
                bloque_club = tds[8]
                club_link = bloque_club.find('a')
                if club_link and club_link.get('title'):
                    from_club = club_link["title"]
            
            nombre_link = name_tag.find('a') if name_tag else None
            id = nombre_link['href'].split('/')[-1] if nombre_link and nombre_link.get('href') else "N/A"
            tabla_altas.append({"player_id": id, "player_name": name, "from_club": from_club, "amount": amount_numeric})

        # --- PROCESAR BAJAS ---
        bajas_rows = tables[1].find('tbody').find_all('tr', class_=['odd', 'even'])
        for item in bajas_rows:
            name_tag = item.find('td', class_='hauptlink')
            name = name_tag.get_text(strip=True) if name_tag else "N/A"
            tds = item.find_all('td')
            to_club = "N/A"
            amount_numeric = 0  
            
            if len(tds) > 8:
                bloque_club = tds[8]
                club_link = bloque_club.find('a')
                if club_link and club_link.get('title'):
                    to_club = club_link["title"]
            
            if len(tds) > 12:
                td_amount = tds[12]
                precio_sesion = td_amount.find('i', class_="normaler-text")
                if precio_sesion:
                    amount_text = precio_sesion.get_text(strip=True)
                    clean_amount = amount_text.replace("€", "").replace(".", "").replace(",", ".").strip()
                    try:
                        if "mill" in clean_amount:
                            val = float(clean_amount.split("mill")[0].strip())
                            amount_numeric = int(val * 1000000)
                        elif "mil" in clean_amount:
                            val = float(clean_amount.split("mil")[0].strip())
                            amount_numeric = int(val * 1000)
                        elif "Libre" in amount_text or "coste" in amount_text:
                            amount_numeric = "Libre / Cesión"
                        else:
                            amount_numeric = "Libre / Cesión"
                    except (ValueError, IndexError):
                        amount_numeric = 0
                else:
                    amount_link = td_amount.find('a')
                    if amount_link:
                        amount = amount_link.get_text(strip=True)
                        if amount:
                            clean_amount = amount.replace("€", "").replace(".", "").replace(",", ".").strip()
                            try:
                                if "mill" in clean_amount:
                                    val = float(clean_amount.split("mill")[0].strip())
                                    amount_numeric = int(val * 1000000)
                                elif "mil" in clean_amount:
                                    val = float(clean_amount.split("mil")[0].strip())
                                    amount_numeric = int(val * 1000)
                                elif "Libre" in amount or "coste" in amount:
                                    amount_numeric = "Libre / Cesión"
                                else:
                                    amount_numeric = "Libre / Cesión"
                            except (ValueError, IndexError):
                                amount_numeric = 0
            
            nombre_link = name_tag.find('a') if name_tag else None
            id = nombre_link['href'].split('/')[-1] if nombre_link and nombre_link.get('href') else "N/A"
            tabla_bajas.append({"player_id": id, "player name": name, "to_club": to_club, "amount": amount_numeric})

        return tabla_altas, tabla_bajas
    else:
        print(f"Error al acceder: {response.status_code}")
