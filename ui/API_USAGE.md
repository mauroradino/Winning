# Guía de Uso de la API - Frontend

Esta guía explica cómo usar las funciones de API desde el frontend React.

## Configuración

### Variable de Entorno

Crea un archivo `.env` en la carpeta `ui` con la URL de tu API:

```env
VITE_API_URL=http://localhost:5000/api
```

Si no defines esta variable, por defecto usará `http://localhost:5000/api`.

## Funciones Disponibles

### 1. `getPlayers(club, temporada)`

Obtiene la lista de jugadores de un club y temporada.

**Parámetros:**
- `club` (string): Nombre del club (ej: 'boca juniors', 'arsenal', 'manchester city')
- `temporada` (string): Año de la temporada (ej: '2025')

**Retorna:** Array de objetos con información de jugadores

**Ejemplo:**
```javascript
import { getPlayers } from './utils'

const players = await getPlayers('boca juniors', '2025')
console.log(players)
```

### 2. `getTransfers(club, temporada)`

Obtiene las transferencias (altas y bajas) de un club y temporada.

**Parámetros:**
- `club` (string): Nombre del club
- `temporada` (string): Año de la temporada

**Retorna:** Objeto con `{ altas: [], bajas: [] }`

**Ejemplo:**
```javascript
import { getTransfers } from './utils'

const transfers = await getTransfers('boca juniors', '2025')
console.log('Altas:', transfers.altas)
console.log('Bajas:', transfers.bajas)
```

### 3. `getValuations(club, temporada)`

Obtiene las valoraciones de los jugadores de un club y temporada.

**Parámetros:**
- `club` (string): Nombre del club
- `temporada` (string): Año de la temporada

**Retorna:** Array de objetos con información de valoraciones

**Ejemplo:**
```javascript
import { getValuations } from './utils'

const valuations = await getValuations('boca juniors', '2025')
console.log(valuations)
```

### 4. `getClubData(club, temporada)`

Obtiene todos los datos de un club (jugadores, transferencias y valoraciones) en una sola llamada.

**Parámetros:**
- `club` (string): Nombre del club
- `temporada` (string): Año de la temporada

**Retorna:** Objeto con `{ players: [], transfers: {}, valuations: [] }`

**Ejemplo:**
```javascript
import { getClubData } from './utils'

const clubData = await getClubData('boca juniors', '2025')
console.log('Jugadores:', clubData.players)
console.log('Transferencias:', clubData.transfers)
console.log('Valoraciones:', clubData.valuations)
```

### 5. `getAvailableClubs()`

Obtiene la lista de clubes disponibles.

**Retorna:** Array de clubes disponibles

**Ejemplo:**
```javascript
import { getAvailableClubs } from './utils'

const clubs = await getAvailableClubs()
console.log(clubs)
```

### 6. `callApi(endpoint, options)`

Función genérica para hacer llamadas personalizadas a la API.

**Parámetros:**
- `endpoint` (string): Endpoint de la API (ej: '/custom-endpoint')
- `options` (object, opcional): Opciones de fetch (method, body, headers, etc.)

**Retorna:** Datos de la respuesta

**Ejemplo:**
```javascript
import { callApi } from './utils'

// GET request
const data = await callApi('/custom-endpoint')

// POST request
const result = await callApi('/save-data', {
  method: 'POST',
  body: {
    club: 'boca juniors',
    temporada: '2025'
  }
})
```

## Ejemplos de Uso en Componentes

### Ejemplo 1: Cargar datos al montar el componente

```javascript
import { useState, useEffect } from 'react'
import { getPlayers } from './utils'

function PlayersList() {
  const [players, setPlayers] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    const fetchPlayers = async () => {
      try {
        const data = await getPlayers('boca juniors', '2025')
        setPlayers(data)
      } catch (err) {
        setError(err.message)
      } finally {
        setLoading(false)
      }
    }

    fetchPlayers()
  }, [])

  if (loading) return <div>Cargando...</div>
  if (error) return <div>Error: {error}</div>

  return (
    <ul>
      {players.map(player => (
        <li key={player.player_id}>
          {player['nombre y apellido']}
        </li>
      ))}
    </ul>
  )
}
```

### Ejemplo 2: Cargar datos con un botón

```javascript
import { useState } from 'react'
import { getTransfers } from './utils'

function TransfersButton() {
  const [transfers, setTransfers] = useState(null)
  const [loading, setLoading] = useState(false)

  const handleClick = async () => {
    setLoading(true)
    try {
      const data = await getTransfers('boca juniors', '2025')
      setTransfers(data)
    } catch (err) {
      console.error('Error:', err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div>
      <button onClick={handleClick} disabled={loading}>
        {loading ? 'Cargando...' : 'Cargar Transferencias'}
      </button>
      
      {transfers && (
        <div>
          <p>Altas: {transfers.altas?.length || 0}</p>
          <p>Bajas: {transfers.bajas?.length || 0}</p>
        </div>
      )}
    </div>
  )
}
```

### Ejemplo 3: Formulario de búsqueda

```javascript
import { useState } from 'react'
import { getClubData } from './utils'

function SearchForm() {
  const [club, setClub] = useState('boca juniors')
  const [temporada, setTemporada] = useState('2025')
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    
    try {
      const clubData = await getClubData(club, temporada)
      setData(clubData)
    } catch (err) {
      console.error('Error:', err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        value={club}
        onChange={(e) => setClub(e.target.value)}
        placeholder="Club"
      />
      <input
        type="text"
        value={temporada}
        onChange={(e) => setTemporada(e.target.value)}
        placeholder="Temporada"
      />
      <button type="submit" disabled={loading}>
        {loading ? 'Buscando...' : 'Buscar'}
      </button>
    </form>
  )
}
```

## Manejo de Errores

Todas las funciones lanzan errores que puedes capturar con `try/catch`:

```javascript
try {
  const players = await getPlayers('boca juniors', '2025')
  // Usar los datos
} catch (error) {
  // Manejar el error
  console.error('Error al obtener jugadores:', error.message)
}
```

## Notas Importantes

1. **URL Base**: Asegúrate de que la URL base de la API esté correctamente configurada en el archivo `.env`

2. **Clubes Disponibles**: Los nombres de clubes deben coincidir exactamente con los definidos en `urls.json`:
   - `'boca juniors'`
   - `'arsenal'`
   - `'manchester city'`

3. **Formato de Temporada**: Usa el año como string (ej: `'2025'`, no `2025`)

4. **Async/Await**: Todas las funciones son asíncronas, asegúrate de usar `await` o `.then()`

5. **Errores**: Las funciones lanzan errores que debes manejar con `try/catch` o `.catch()`

## Ver Más Ejemplos

Revisa el archivo `src/api-examples.js` para ver más ejemplos de uso detallados.

