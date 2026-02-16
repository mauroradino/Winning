from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import json
import pandas as pd
import time

with open("urls.json", "r") as f:
    urls = json.load(f)

def get_salaries(club: str, temporada: str):
    url = f"{urls[club]["salaries"]}{temporada}-{int(temporada) + 1}"
    chrome_options = Options()
    chrome_options.add_argument("--headless") 
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(options=chrome_options)

    try:
        driver.get(url)
        wait = WebDriverWait(driver, 15)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#table tbody tr")))
        time.sleep(2)

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        # 1. Encontrar el índice de la columna "Gross P/Y" dinámicamente
        header_row = soup.find('table', id='table').find('thead').find_all('tr')[-1]
        headers = [th.get_text(strip=True) for th in header_row.find_all('th')]
        
        # Buscamos la columna que diga "Gross P/Y" (Sueldo anual bruto)
        try:
            # En la Premier suele decir "Gross P/Y (GBP)"
            target_col_index = next(i for i, h in enumerate(headers) if "Gross P/Y" in h)
        except StopIteration:
            print("❌ No se encontró la columna de sueldo anual.")
            return pd.DataFrame()

        # 2. Extraer los datos usando el índice dinámico
        rows = soup.find('table', id='table').find('tbody').find_all('tr')
        players_data = []
        
        for row in rows:
            cols = row.find_all('td')
            if len(cols) > target_col_index:
                players_data.append({
                    "nombre": cols[0].get_text(strip=True),
                    # Usamos el índice que encontramos dinámicamente
                    "sueldo_anual": cols[target_col_index].get_text(strip=True).replace('£', '').replace(',', '').replace(' ', ''),
                })

        print(f"✅ Éxito ({temporada}): Se encontraron {len(players_data)} jugadores.")
        return pd.DataFrame(players_data)
    
    except Exception as e:
        print(f"❌ Error con Selenium: {e}")
        return []
    finally:
        driver.quit()

