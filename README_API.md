# Guía para Levantar la API

Esta guía explica cómo configurar y ejecutar el servidor API para el proyecto Winning.

## Requisitos Previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

## Instalación

### 1. Instalar dependencias

Abre una terminal en la raíz del proyecto y ejecuta:

```bash
pip install -r requirements.txt
```

O si usas Python 3 específicamente:

```bash
python3 -p install -r requirements.txt
```

### 2. Verificar que todo esté instalado

```bash
python -c "import flask; print('Flask instalado correctamente')"
```

## Ejecutar el Servidor

### Opción 1: Ejecución directa

```bash
python api.py
```

### Opción 2: Con variables de entorno

```bash
# Windows (PowerShell)
$env:PORT=5000
$env:DEBUG="True"
python api.py

# Windows (CMD)
set PORT=5000
set DEBUG=True
python api.py

# Linux/Mac
PORT=5000 DEBUG=True python api.py
```

### Opción 3: Usando Flask directamente

```bash
flask --app api run --port 5000 --debug
```

## Verificar que Funciona

Una vez que el servidor esté corriendo, deberías ver:

```
🚀 Iniciando servidor API en http://localhost:5000
📋 Endpoints disponibles:
   - GET /api/health
   - GET /api/clubs
   - GET /api/players?club=<club>&temporada=<año>
   - GET /api/transfers?club=<club>&temporada=<año>
   - GET /api/valuations?club=<club>&temporada=<año>
 * Running on http://0.0.0.0:5000
```

Puedes probar que funciona abriendo en tu navegador:
- http://localhost:5000/api/health
- http://localhost:5000/api/clubs

## Endpoints Disponibles

### 1. GET /api/health
Verifica que el servidor está funcionando.

**Respuesta:**
```json
{
  "status": "ok",
  "message": "API funcionando correctamente"
}
```

### 2. GET /api/clubs
Obtiene la lista de clubes disponibles.

**Respuesta:**
```json
["boca juniors", "arsenal", "manchester city"]
```

### 3. GET /api/players
Obtiene los jugadores de un club y temporada.

**Parámetros:**
- `club` (requerido): Nombre del club (ej: 'boca juniors')
- `temporada` (requerido): Año de la temporada (ej: '2025')

**Ejemplo:**
```
GET /api/players?club=boca%20juniors&temporada=2025
```

### 4. GET /api/transfers
Obtiene las transferencias (altas y bajas) de un club y temporada.

**Parámetros:**
- `club` (requerido): Nombre del club
- `temporada` (requerido): Año de la temporada

**Ejemplo:**
```
GET /api/transfers?club=boca%20juniors&temporada=2025
```

**Respuesta:**
```json
{
  "altas": [...],
  "bajas": [...]
}
```

### 5. GET /api/valuations
Obtiene las valoraciones de los jugadores de un club y temporada.

**Parámetros:**
- `club` (requerido): Nombre del club
- `temporada` (requerido): Año de la temporada

**Ejemplo:**
```
GET /api/valuations?club=boca%20juniors&temporada=2025
```

## Configuración del Frontend

Una vez que el servidor esté corriendo, asegúrate de que el frontend esté configurado para apuntar a la API.

Crea un archivo `.env` en la carpeta `ui`:

```env
VITE_API_URL=http://localhost:5000/api
```

## Solución de Problemas

### Error: "ModuleNotFoundError: No module named 'flask'"
**Solución:** Instala las dependencias con `pip install -r requirements.txt`

### Error: "Address already in use"
**Solución:** El puerto 5000 está ocupado. Cambia el puerto:
```bash
PORT=5001 python api.py
```

Y actualiza el `.env` del frontend:
```env
VITE_API_URL=http://localhost:5001/api
```

### Error: "CORS policy"
**Solución:** El servidor ya tiene CORS habilitado. Si persiste el error, verifica que el servidor esté corriendo y que la URL en el frontend sea correcta.

### Las peticiones son lentas
**Nota:** Las peticiones pueden tardar varios segundos porque el servidor está haciendo scraping en tiempo real. Esto es normal.

## Producción

Para producción, considera usar un servidor WSGI como Gunicorn:

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 api:app
```


