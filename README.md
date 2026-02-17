# Winning Technical Challenge ⚽🤖

Este proyecto es una solución para el **Winning Technical Challenge**. Combina un motor de extracción de datos de fútbol mediante Web Scraping con una plataforma interactiva de simulación de transferencias potenciada por Inteligencia Artificial.

## 🚀 Live Demo
Podes probar la aplicación en vivo en este enlace: **[winning-black.vercel.app](https://winning-black.vercel.app/)** 

---

## 🛠️ Stack Tecnológico 

### Frontend & UI
* **React + Vite:** Para una interfaz reactiva, rápida y moderna.
* **TailwindCSS:** Estilizado eficiente y diseño de interfaz profesional.

### Backend & Data Engine
* **FastAPI (Python):** Framework asíncrono para la API de simulación y gestión de datos.
* **Pandas:** Procesamiento y limpieza de grandes volúmenes de datos estructurados.
* **AWS S3:** Persistencia de datasets en la nube (formatos CSV/JSON).

### AI & Vector Intelligence 
* **Pinecone:** Base de datos vectorial para búsquedas semánticas y recuperación de contexto.
* **LangChain:** Orquestador para el procesamiento de documentos y flujos RAG.
* **OpenAI SDK:** Generación de resúmenes estratégicos y análisis de profundidad de plantilla.

---

## 🏗️ Arquitectura y Lógica de Simulación
La aplicación permite visualizar y simular resultados basados en:
* **Inputs:** Club, Temporada, Presupuesto de Transferencias y Presupuesto Salarial.
* **Simulación:** Lógica interactiva para compra/venta de jugadores, lista de plantilla actualizada y cambios en la valoración del equipo.
* **Net Financial Benefit:** Cálculo automático del balance financiero tras cada movimiento.

---

## 📋 Desafíos Técnicos y Soluciones (Challenges)

Durante el desarrollo se enfrentaron y resolvieron los siguientes retos de ingeniería:

### 1. Inconsistencias de Datos (Data Scraping)
* **Sanitización de Nulos (NaN):** Se resolvió el error de serialización JSON (`ValueError: Out of range float values`) mediante una capa de limpieza con Pandas que convierte valores `NaN` en `null` antes de enviarlos a la UI.

### 2. Integración y Arquitectura (Backend)
* **Dependencias Circulares:** Se reestructuraron los módulos de la API (`aws_s3.py` e `index.py`) utilizando *deferred imports* para permitir que la normalización de datos y la persistencia en S3 funcionen de forma independiente.
* **Normalización de Nombres:** Se implementó una función basada en `unicodedata` para manejar acentos y caracteres especiales (ej. "Julián Álvarez" vs "Julian Alvarez"), asegurando que las transferencias encuentren siempre el ID correcto del jugador.

---

## 🧠 Decisiones Técnicas (Technical Decisions) 

* **Boto3 vs Local:** Se eligió AWS S3 para permitir que el scraper y la aplicación web compartan una fuente de verdad escalable y centralizada.
* **Separación de Estados:** En el simulador, se separó el `montoDisplay` (formateado con puntos) del `monto` (numérico), optimizando la UX sin comprometer la precisión de los cálculos financieros.
* **Modularidad:** Se optó por una estructura de paquetes con imports absolutos para que los notebooks de IA y el servidor de producción compartan la misma lógica de negocio.

---

## ⚠️ Limitaciones y Trade-offs 
* **Persistencia Atómica:** La escritura en S3 es secuencial; interrupciones manuales durante la carga (`Ctrl+C`) pueden generar archivos parciales.
* **Latencia de IA:** El tiempo de respuesta del resumen de temporada depende de la cuota y latencia del proveedor de LLM.

---

## Variables de Entonrno
* En el archivo example.env podes encontrar las variables de entorno necesarias para ejecutar el proyecto

## Esquemas de datos
* **Jugadores:**
     "player_id": int,
     "número": int,
     "nombre y apellido": str,
     "posicion": str,
     "edad": int,
     "fecha de nacimiento": str,
     "pie": str,
     "pais de orígen": str,
     "altura": int,
     "valor": int,
     "club anterior": str,
     "sueldo_anual": str

* **Valuaciones:**
    valuation_amount: int 
    valuation_date:str
    
* **Transferencias:**
    altas:
        amount: str 
        from_club:str 
        player_id: int
        player_name:str
    
    bajas:
        amount: str 
        from_club:str 
        player_id: int
        player_name:str

## ⚙️ Instalación Local 

1. **Clonar el repositorio:**
   ```bash
   git clone [https://github.com/mauroradino/Winning](https://github.com/mauroradino/Winning)

2. **Configurar el Frontend**
    ```bash
    cd ui
    npm install
    npm run dev

3. **Ejecutar el Scraper (Python) [No necesario para la utilización del proyecto]**
    ```bash
    cd api
    pip install -r requirements.txt
    python main.py