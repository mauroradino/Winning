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
                nombre = td_nombre.find('a').text.strip() if td_nombre and td_nombre.find('a') else "N/A"
                link_perfil = td_nombre.find('a')['href'] if td_nombre and td_nombre.find('a') else None
                
                inline_table = item.find('table', class_='inline-table')
                all_inline_tds = inline_table.find_all('td') if inline_table else []
                posicion = all_inline_tds[-1].get_text(strip=True) if all_inline_tds else "N/A"
                tds_zentriert = item.find_all('td', class_='zentriert')
                
                link_detalles = item.find_all('td', class_='rechts hauptlink')
                
                valor_num = "N/A"
                valor_fecha = "N/A"

                for link_td in link_detalles:
                    a_tag = link_td.find('a')
                    if a_tag and 'href' in a_tag.attrs:
                        detalles_url = a_tag['href']
                        time.sleep(0.1)
                        detalles_response = session.get(f"https://www.transfermarkt.es{detalles_url}")
                        if detalles_response.status_code == 200:
                            detalles_soup = BeautifulSoup(detalles_response.text, 'html.parser')
                            wrapper = detalles_soup.find('a', class_='data-header__market-value-wrapper')
                            if wrapper:
                                valor_num = wrapper.get_text(strip=True).split('Última')[0].strip()
                                date_p = wrapper.find('p', class_='data-header__last-update')
                                valor_fecha = date_p.get_text(strip=True).replace('Última revisión:', '').strip() if date_p else "N/A"

                fecha, edad = "N/A", "N/A"
                if len(tds_zentriert) > 1:
                    nacimiento_raw = tds_zentriert[1].get_text(strip=True)
                    if " (" in nacimiento_raw:
                        partes = nacimiento_raw.split(" (")
                        fecha = partes[0]
                        edad = partes[1].replace(")", "")
                
                club_anterior = "N/A"
                if len(tds_zentriert) > 6:
                    club_escudo = tds_zentriert[6].find('img')
                    if club_escudo:
                        club_anterior = club_escudo['title'].split(':')[0]

                pie = tds_zentriert[4].get_text(strip=True) if len(tds_zentriert) > 4 else "N/A"
                
                altura_raw = tds_zentriert[3].get_text(strip=True) if len(tds_zentriert) > 3 else "N/A"
                
                if altura_raw in ["indeterminado", "indeterminadom", "N/A"]:
                    altura = 0.0
                elif 'm' in altura_raw:
                    altura_limpia = altura_raw.replace('m', '').replace(',', '.').strip()
                    try:
                        altura = int(float(altura_limpia) * 100)
                    except ValueError:
                        altura = 0.0
                else:
                    altura = 0.0


                nacionalidad = "N/A"
                if len(tds_zentriert) > 2:
                    img_flag = tds_zentriert[2].find('img')
                    if img_flag:
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
                    "altura": altura,
                    "valor": valor_num,
                    "ultima valoracion": valor_fecha,
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