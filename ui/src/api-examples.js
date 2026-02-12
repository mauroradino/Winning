/**
 * EJEMPLOS DE USO DE LA API
 * 
 * Este archivo muestra diferentes formas de usar las funciones de API
 * desde tus componentes React.
 */

import { 
  getPlayers, 
  getTransfers, 
  getValuations, 
  getClubData, 
  getAvailableClubs,
  callApi 
} from './utils'

// ============================================
// EJEMPLO 1: Usar en un componente con useState y useEffect
// ============================================
export const ejemploConUseEffect = `
import { useState, useEffect } from 'react'
import { getPlayers } from './utils'

function MiComponente() {
  const [players, setPlayers] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    const fetchPlayers = async () => {
      try {
        setLoading(true)
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
    <div>
      {players.map(player => (
        <div key={player.player_id}>
          {player['nombre y apellido']}
        </div>
      ))}
    </div>
  )
}
`

// ============================================
// EJEMPLO 2: Usar con un botón (onClick handler)
// ============================================
export const ejemploConBoton = `
import { useState } from 'react'
import { getTransfers } from './utils'

function TransferenciasComponent() {
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
          <h3>Altas: {transfers.altas?.length || 0}</h3>
          <h3>Bajas: {transfers.bajas?.length || 0}</h3>
        </div>
      )}
    </div>
  )
}
`

// ============================================
// EJEMPLO 3: Obtener todos los datos de un club
// ============================================
export const ejemploGetAllData = `
import { useState } from 'react'
import { getClubData } from './utils'

function ClubDataComponent() {
  const [clubData, setClubData] = useState(null)

  const loadData = async () => {
    try {
      const data = await getClubData('boca juniors', '2025')
      setClubData(data)
      
      // Acceder a los datos
      console.log('Jugadores:', data.players)
      console.log('Transferencias:', data.transfers)
      console.log('Valoraciones:', data.valuations)
    } catch (err) {
      console.error('Error:', err)
    }
  }

  return (
    <button onClick={loadData}>
      Cargar Datos Completos
    </button>
  )
}
`

// ============================================
// EJEMPLO 4: Usar callApi directamente para endpoints personalizados
// ============================================
export const ejemploCallApiDirecto = `
import { callApi } from './utils'

// Llamada GET simple
const fetchCustomData = async () => {
  try {
    const data = await callApi('/custom-endpoint')
    return data
  } catch (error) {
    console.error('Error:', error)
  }
}

// Llamada POST con body
const postData = async () => {
  try {
    const data = await callApi('/save-data', {
      method: 'POST',
      body: {
        club: 'boca juniors',
        temporada: '2025'
      }
    })
    return data
  } catch (error) {
    console.error('Error:', error)
  }
}
`

// ============================================
// EJEMPLO 5: Manejo de errores completo
// ============================================
export const ejemploManejoErrores = `
import { useState } from 'react'
import { getValuations } from './utils'

function ValuationsComponent() {
  const [valuations, setValuations] = useState([])
  const [error, setError] = useState(null)
  const [loading, setLoading] = useState(false)

  const loadValuations = async () => {
    setLoading(true)
    setError(null)
    
    try {
      const data = await getValuations('boca juniors', '2025')
      setValuations(data || [])
    } catch (err) {
      // El error ya fue logueado en callApi
      setError(err.message || 'Error desconocido')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div>
      <button onClick={loadValuations} disabled={loading}>
        {loading ? 'Cargando...' : 'Cargar Valoraciones'}
      </button>
      
      {error && (
        <div className="error-message">
          Error: {error}
        </div>
      )}
      
      {!loading && !error && valuations.length === 0 && (
        <div>No hay valoraciones disponibles</div>
      )}
      
      {valuations.map((val, index) => (
        <div key={index}>
          {val.nombre_jugador}: €{val.valuation_amount}
        </div>
      ))}
    </div>
  )
}
`

// ============================================
// EJEMPLO 6: Usar con formulario
// ============================================
export const ejemploConFormulario = `
import { useState } from 'react'
import { getPlayers } from './utils'

function SearchForm() {
  const [club, setClub] = useState('boca juniors')
  const [temporada, setTemporada] = useState('2025')
  const [players, setPlayers] = useState([])
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    
    try {
      const data = await getPlayers(club, temporada)
      setPlayers(data || [])
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
`

