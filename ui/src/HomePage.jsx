import { useState, useEffect, useRef } from 'react'
import './App.css'
import {
  getPlayers,
  getTransfers,
  getClubData,
  getRevenue,
  playerValuation,
  launchIngestion,
} from './utils'
import RevenueCard from './components/RevenueCard'
import PlayerGraph from './components/PlayerGraph'
import PurchaseTable from './components/PurchaseTable'
import SalesTable from './components/SalesTable'
import PlayersTable from './components/PlayersTable'
import SeasonSummary from './components/SeasonSummary'
import TeamSelector from './components/TeamSelector'
import YearSelect from './components/YearSelect'

function HomePage() {
  const [club, setClub] = useState('')
  const [temporada, setTemporada] = useState('')
  const [presupuestoFichajes, setPresupuestoFichajes] = useState(0)
  const [presupuestoSalarios, setPresupuestoSalarios] = useState(0)
  const [player, setPlayer] = useState('')
  const [revenue, setRevenue] = useState(0)
  const [restante, setRestante] = useState(0)
  const [gasto, setGasto] = useState(0)
  const [ingreso, setIngreso] = useState(0)
  const [valuations, setValuations] = useState([])
  const [squadPlayers, setSquadPlayers] = useState([])       // Plantel completo
  const [purchasedPlayers, setPurchasedPlayers] = useState([]) // Altas
  const [soldPlayers, setSoldPlayers] = useState([])           // Bajas
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [data, setData] = useState(null)
  const transfersRequestRef = useRef(null)

  useEffect(() => {
    setPurchasedPlayers([])
    setSoldPlayers([])
    transfersRequestRef.current = null
  }, [club, temporada])

  const handleGetPlayers = async () => {
    setSquadPlayers([])
    setData(null)
    setLoading(true)
    setError(null)
    try {
      const playersResp = await getPlayers(
        club.toLowerCase(),
        temporada.slice(0, 4),
      )
      setSquadPlayers(playersResp || [])
      setData({ players: playersResp })
    } catch (err) {
      setError(err.message)
      console.error('Error:', err)
    } finally {
      setLoading(false)
    }
  }

  const handleGetTransfers = async () => {
    const currentClub = club.toLowerCase()
    const currentSeason = temporada.slice(0, 4)
    const requestId = `${currentClub}-${currentSeason}-${Date.now()}`
    transfersRequestRef.current = requestId
    setPurchasedPlayers([])
    setSoldPlayers([])
    setData(null)
    setLoading(true)
    setError(null)
    try {
      const transfers = await getTransfers(
        currentClub,
        currentSeason,
      )
      if (transfersRequestRef.current === requestId && club.toLowerCase() === currentClub && temporada.slice(0, 4) === currentSeason) {
        setData({ transfers })
        setPurchasedPlayers(transfers?.altas || [])
        setSoldPlayers(transfers?.bajas || [])
      }
    } catch (err) {
      if (transfersRequestRef.current === requestId && club.toLowerCase() === currentClub && temporada.slice(0, 4) === currentSeason) {
        setError(err.message)
        console.error('Error:', err)
      }
    } finally {
      if (transfersRequestRef.current === requestId && club.toLowerCase() === currentClub && temporada.slice(0, 4) === currentSeason) {
        setLoading(false)
      }
    }
  }

  const handleGetAllData = async () => {
    const currentClub = club.toLowerCase()
    const currentSeason = temporada.slice(0, 4)
    const requestId = `${currentClub}-${currentSeason}-${Date.now()}`
    transfersRequestRef.current = requestId
    setLoading(true)
    setError(null)
    try {
      const clubData = await getClubData(currentClub, currentSeason)
      if (transfersRequestRef.current === requestId && club.toLowerCase() === currentClub && temporada.slice(0, 4) === currentSeason) {
        setData(clubData)
        setSquadPlayers(clubData.players || [])
        setPurchasedPlayers(clubData.transfers?.altas || [])
        setSoldPlayers(clubData.transfers?.bajas || [])
      }
    } catch (err) {
      if (transfersRequestRef.current === requestId && club.toLowerCase() === currentClub && temporada.slice(0, 4) === currentSeason) {
        setError(err.message)
        console.error('Error:', err)
      }
    } finally {
      if (transfersRequestRef.current === requestId && club.toLowerCase() === currentClub && temporada.slice(0, 4) === currentSeason) {
        setLoading(false)
      }
    }
  }

  const showRevenue = async (payload) => {
    const res = await getRevenue(payload)
    if (!res) return
    setRevenue(res.net_benefit)
    setRestante(res.budget_remaining)
    setGasto(res.total_spent || 0)
    setIngreso(res.total_income || 0)
  }

  const showValuations = async (payload) => {
    if (payload.player != ''){
      const result = await playerValuation(payload)
      setValuations(result || [])
    }
  }

  const handleClubChange = (name) => {
    setClub(name);
  };

  const handleYearChange = (name) => {
    setTemporada(name);
  };

  const seasonYear = temporada.slice(0, 4)

  return (
    <div className="bg-[#050816] min-h-screen text-white">
      <h1 className='text-4xl font-bold text-center pt-4'>Winning - Technical Challenge</h1>
      <div className="max-w-6xl mx-auto py-8 px-4 space-y-6">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div className="bg-[#0b1020] border border-[#1f2937] rounded-xl px-4 py-3 flex flex-col">
            <span className="text-xs text-gray-400 uppercase tracking-wide">Club actual</span>
            <span className="mt-1 font-semibold text-[#4ade80]">{club}</span>
          </div>

          <div className="bg-[#0b1020] border border-[#1f2937] rounded-xl px-4 py-3 flex flex-col">
            <span className="text-xs text-gray-400 uppercase tracking-wide">Temporada</span>
            <span className="mt-1 font-semibold">{temporada}</span>
          </div>

          <div className="bg-[#0b1020] border border-[#1f2937] rounded-xl px-4 py-3 flex flex-col">
            <span className="text-xs text-gray-400 uppercase tracking-wide">Presupuesto de fichajes</span>
            <span className="mt-1 font-semibold">${presupuestoFichajes}</span>
          </div>

          <div className="bg-[#0b1020] border border-[#1f2937] rounded-xl px-4 py-3 flex flex-col">
            <span className="text-xs text-gray-400 uppercase tracking-wide">Presupuesto salarial</span>
            <span className="mt-1 font-semibold">${presupuestoSalarios}</span>
          </div>
        </div>

        <div className="bg-[#0b1020] border border-[#1f2937] rounded-xl px-4 py-4 grid grid-cols-1 md:grid-cols-4 gap-4">
          <div className="flex flex-col gap-1">
            <label className="text-xs text-gray-400 uppercase">Club</label>
            <TeamSelector handle={handleClubChange}/>
            
          </div>

          <div className="flex flex-col gap-1">
            <label className="text-xs text-gray-400 uppercase">Temporada</label>
            <YearSelect onSelect={handleYearChange}/>
          </div>

          <div className="flex flex-col gap-1">
            <label className="text-xs text-gray-400 uppercase">Presupuesto fichajes</label>
            <input
              type="number"
              value={presupuestoFichajes}
              onChange={(e) => setPresupuestoFichajes(e.target.value)}
              className="bg-[#020617] border border-[#1f2937] rounded-lg px-3 py-2 text-sm text-white outline-none focus:ring-2 focus:ring-emerald-500"
            />
          </div>

          <div className="flex flex-col gap-1">
            <label className="text-xs text-gray-400 uppercase">Presupuesto salarial</label>
            <input
              type="number"
              value={presupuestoSalarios}
              onChange={(e) => setPresupuestoSalarios(e.target.value)}
              className="bg-[#020617] border border-[#1f2937] rounded-lg px-3 py-2 text-sm text-white outline-none focus:ring-2 focus:ring-emerald-500"
            />
          </div>

          <div className="flex flex-col gap-1 md:col-span-2">
            <label className="text-xs text-gray-400 uppercase">Jugador</label>
            <input
              type="text"
              value={player}
              onChange={(e) => setPlayer(e.target.value)}
              className="bg-[#020617] border border-[#1f2937] rounded-lg px-3 py-2 text-sm text-white outline-none focus:ring-2 focus:ring-emerald-500"
              placeholder="Ej: Leandro Brey"
            />
          </div>
        </div>

        <div className="flex flex-wrap gap-3">
          <button
            onClick={handleGetPlayers}
            disabled={loading}
            className="px-4 py-2 rounded-lg text-sm font-medium bg-emerald-500 hover:bg-emerald-400 disabled:opacity-50"
          >
            Obtener Jugadores
          </button>
          <button
            onClick={handleGetTransfers}
            disabled={loading}
            className="px-4 py-2 rounded-lg text-sm font-medium bg-[#111827] hover:bg-[#1f2937] disabled:opacity-50"
          >
            Obtener Transferencias
          </button>
          <button
            onClick={handleGetAllData}
            disabled={loading}
            className="px-4 py-2 rounded-lg text-sm font-medium bg-[#111827] hover:bg-[#1f2937] disabled:opacity-50"
          >
            Obtener Todos los Datos
          </button>
          <button
            onClick={() =>
              showRevenue({
                club: club.toLowerCase(),
                season: seasonYear,
                transfer_budget: presupuestoFichajes,
              })
            }
            disabled={loading}
            className="px-4 py-2 rounded-lg text-sm font-medium bg-[#111827] hover:bg-[#1f2937] disabled:opacity-50"
          >
            Simular Transferencias
          </button>
          <button
            onClick={() =>
              showValuations({
                club: club.toLowerCase(),
                season: seasonYear,
                player,
              })
            }
            disabled={loading}
            className="px-4 py-2 rounded-lg text-sm font-medium bg-[#111827] hover:bg-[#1f2937] disabled:opacity-50"
          >
            Cargar Historial Precio
          </button>
        </div>

        {loading && <p className="text-sm text-gray-300">Cargando...</p>}
        {error && <p className="text-sm text-red-400">Error: {error}</p>}

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mt-4">
          <div className="lg:col-span-1">
            <div className="bg-[#0b1020] border border-[#1f2937] rounded-2xl p-6 h-full flex flex-col">
              <h2 className="text-lg font-semibold mb-4">Resumen Financiero</h2>
              <RevenueCard
                ganancia={revenue}
                restante={restante}
                presupuesto={presupuestoFichajes}
                gasto={gasto}
                ingreso={ingreso}
              />
            </div>
          </div>

          <div className="lg:col-span-2">
            <div className="bg-[#0b1020] border border-[#1f2937] rounded-2xl p-6 h-full flex flex-col">
              <div className="flex items-baseline justify-between mb-4">
                <div>
                  <h2 className="text-lg font-semibold">Historial de Precio</h2>
                  {player && (
                    <p className="text-xs text-gray-400 mt-1">
                      Seguimiento de valoración:{' '}
                      <span className="text-emerald-400 font-medium">{player}</span>
                    </p>
                  )}
                </div>
              </div>
              <PlayerGraph valuations={valuations} player={player} />
            </div>
          </div>

          <div className="lg:col-span-3 grid grid-cols-1 gap-6">
            <PlayersTable players={squadPlayers} club={club} season={temporada} />
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <PurchaseTable
                players={purchasedPlayers}
                club={club}
                season={temporada}
              />
              <SalesTable players={soldPlayers} />
            </div>
          <SeasonSummary club={club} season={temporada}/>
          </div>
        </div>
        {data && (
          <div className="bg-[#020617] border border-[#1f2937] rounded-xl p-4 mt-4 text-xs text-gray-300">
            <h3 className="font-semibold mb-2">Datos crudos (debug)</h3>
            <pre className="whitespace-pre-wrap break-all">
              {JSON.stringify(data, null, 2)}
            </pre>
          </div>
        )}
      </div>
    </div>
  )
}

export default HomePage