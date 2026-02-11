import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def get_players(url: str):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    session = requests.Session()
    session.headers.update(headers)
    
    try:
        response = session.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error en la petición: {e}")
        return []

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        players = []
        
        items_table = soup.find('table', class_='items')
        if not items_table:
            print("No se encontró la tabla de jugadores.")
            return []
            
        body = items_table.find('tbody')
        rows = body.find_all('tr')

        for item in rows: 
            td_numero = item.find('td', class_='rueckennummer')
            if not td_numero:
                continue
            
            try:
                div_rn = td_numero.find('div', class_='rn_nummer')
                numero = div_rn.text.strip() if div_rn else "N/A"
                
                td_nombre = item.find('td', class_='hauptlink')
                nombre_link = td_nombre.find('a') if td_nombre else None
                nombre = nombre_link.text.strip() if nombre_link else "N/A"
                link_perfil = nombre_link['href'] if nombre_link and nombre_link.get('href') else None
                
                inline_table = item.find('table', class_='inline-table')
                all_inline_tds = inline_table.find_all('td') if inline_table else []
                posicion = all_inline_tds[-1].get_text(strip=True) if all_inline_tds else "N/A"
                tds_zentriert = item.find_all('td', class_='zentriert')
                td_valor = item.find('td', class_='rechts hauptlink')
                valor_num = 0  # Inicializar con valor por defecto
                if td_valor and td_valor.find('a'):
                    raw_v = td_valor.find('a').get_text(strip=True).replace('€', '').replace(',', '.')
                    if 'mill' in raw_v:
                        val_str = raw_v.replace('mill.', '').replace('mill', '').strip()
                        valor_num = int(float(val_str) * 1000000)
                    elif 'mil' in raw_v:
                        val_str = raw_v.replace('mil.', '').replace('mil', '').strip()
                        valor_num = int(float(val_str) * 1000)
                fecha, edad = "N/A", "N/A"
                if len(tds_zentriert) > 1:
                    nacimiento_raw = tds_zentriert[1].get_text(strip=True)
                    if " (" in nacimiento_raw:
                        partes = nacimiento_raw.split(" (")
                        fecha = partes[0]
                        edad = partes[1].replace(")", "")
                
                club_anterior = "N/A"  # Valor por defecto
                if len(tds_zentriert) > 7:
                    club_link = tds_zentriert[6].find('a')
                    if club_link and club_link.get('title'):
                        club_anterior = club_link['title'].split(':')[0]
                pie = tds_zentriert[4].get_text(strip=True) if len(tds_zentriert) > 5 else "N/A"
                
                altura_raw = tds_zentriert[3].get_text(strip=True) if len(tds_zentriert) > 3 else "N/A"
                        
                if altura_raw in ["indeterminado", "indeterminadom", "N/A"]:
                            altura_limpia = 0.0
                elif 'm' in altura_raw:
                    altura_limpia = altura_raw.replace('m', '').replace(',', '.').strip()
                    try:
                        altura_limpia = int(float(altura_limpia) * 100)
                    except ValueError:
                        altura_limpia = 0.0
                else: 
                    altura_limpia = altura_raw


                nacionalidad = "N/A"
                if len(tds_zentriert) > 2:
                    img_flag = tds_zentriert[2].find('img')
                    if img_flag and img_flag.get('title'):
                        nacionalidad = img_flag['title']

                players.append({
                    "player_id": link_perfil.split('/')[-1] if link_perfil else "N/A",
                    "número": numero, 
                    "nombre y apellido": nombre, 
                    "posicion": posicion, 
                    "edad": edad, 
                    "fecha de nacimiento": fecha, 
                    "pie": pie,
                    "pais de orígen": nacionalidad,
                    "altura": altura_limpia,
                    "valor": valor_num,
                    "club anterior": club_anterior
                })
                
            except Exception as e:
                print(f"Error procesando a {nombre}: {e}")
                continue

        print(f"Éxito: Se procesaron {len(players)} jugadores.")
        return players
    else:
        print(f"Error de acceso: {response.status_code}")
        return []
    
#print(get_players("https://www.transfermarkt.es/ca-boca-juniors/kader/verein/189/plus/1/galerie/0?saison_id=2025"))