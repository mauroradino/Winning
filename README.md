# Winning Technical Challenge ⚽🤖

Este proyecto es una solución integral para el **Winning Technical Challenge**. Combina un motor de extracción de datos de fútbol (Web Scraping) con una plataforma interactiva de simulación de transferencias potenciada por Inteligencia Artificial y arquitecturas RAG.

## 🚀 Live Demo
Podes probar la aplicación con este enlace: **[winning-black.vercel.app](https://winning-black.vercel.app/)** 

---

## 🛠️ Stack Tecnológico

### Frontend & UI
* **React + Vite:** Para una interfaz reactiva, rápida y moderna.
* **TailwindCSS:** Estilizado eficiente y diseño de interfaz profesional.

### Backend & Data Engine
* **Python + BeautifulSoup:** Scraper robusto encargado de extraer datos estructurados de dominios deportivos.
* **AWS S3:** Almacenamiento de los datasets extraídos en formato CSV.

### AI & Vector Intelligence
* **Pinecone:** Base de datos vectorial utilizada para indexar los datos de los jugadores, permitiendo búsquedas semánticas y recuperación de contexto para la IA.
* **LangChain:** Orquestador utilizado para implementar el `CSVLoader` y gestionar el flujo de datos.
* **OpenAI SDK:** Motor de IA encargado de generar resúmenes estratégicos y análisis de profundidad de plantilla.

---

## 🏗️ Arquitectura de Datos (RAG)
El sistema sigue un flujo de **Generación Aumentada por Recuperación**:
1. **Extracción:** El script en Python captura información de jugadores (edad, pie, nacionalidad), transferencias y valuaciones.
2. **Persistencia:** Los datos se cargan en un bucket de **S3**.
3. **Indexación:** LangChain procesa los archivos CSV y genera embeddings que se almacenan en **Pinecone**.
4. **Simulación:** La IA consulta los vectores en Pinecone para ofrecer una respuesta precisa basada en el mercado real, el presupuesto de transferencias y el límite salarial ingresado.

---

## 📋 Entregables del Desafío

### 1. Data Integration & Web Scraping 
* **Objetivo:** Extracción de datos de equipos y temporadas específicas.
* **Entidades:** Jugadores, Clubes, Transferencias y Valuaciones.
* **Desafíos:** Manejo de consistencia de datos y estructuras de dominios específicos.

### 2. AI Transfer Simulator 
* **Visualización:** Simulación de jugadores comprados/vendidos, lista de plantilla actual y cambios en la valoración neta.
* **IA Component:** Generación de un resumen de texto de la temporada y generación de análisis de plantel asistido por LLMs.

### 3.  🧠 Decisiones Técnicas & Desafíos
## Desafíos de Scraping (Anti-Scraping & Inconsistencias)
* **Renderizado Dinámico:** Se detectó que los datos salariales se inyectan vía JavaScript. Se migró de BeautifulSoup estático a **Selenium** para asegurar la hidratación completa del DOM antes de la extracción.
* **Sanitización de Datos:** Se implementó una lógica de limpieza para manejar caracteres Unicode (como el em-dash `—`) y formatos numéricos complejos en las funciones de JavaScript de la fuente, garantizando que el pipeline hacia S3/Pinecone reciba datos limpios.
* **Estructura Cambiante:** Se desarrolló un sistema de indexación dinámica de columnas por nombre de encabezado para manejar variaciones en las tablas entre diferentes temporadas.

### Mejoras (Enhancements)
* **Automatización Multiclub:** A diferencia de un scraper simple, el sistema procesa múltiples clubes y un rango de 6 temporadas (2020-2025) de forma automática mediante la configuración en `urls.json`.

### Limitaciones y Trade-offs
* **Dependencia de la Fuente:** El scraper es sensible a cambios estructurales mayores en el DOM de los sitios objetivo.
* **Costo de Latencia:** El uso de un navegador headless (Selenium) aumenta el tiempo de recolección pero garantiza la fidelidad de los datos frente a métodos de request simples.

## 🔑 Variables de Entorno
Para ejecutar el backend (`api`) y la indexación, se requiere un archivo `.env` con:
`OPENAI_API_KEY`, `PINECONE_API_KEY`, `PINECONE_ENV`, `AWS_ACCESS_KEY`, `AWS_SECRET_KEY`.
---

## ⚙️ Instalación Local

```bash
# 1. Clonar el repositorio
git clone [https://github.com/mauroradino/Winning](https://github.com/mauroradino/Winning)

# 2. Configurar el Frontend
cd ui
npm install
npm run dev

# 3. Ejecutar el Scraper (Python) [No necesario para la utilización del proyecto]
cd api
pip install -r requirements.txt
python main.py