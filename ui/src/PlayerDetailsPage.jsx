import { useSearchParams } from "react-router-dom"
import { getPlayerInfo, playerValuation } from "./utils"
import { useEffect, useState } from "react"
import LoadingState from "./components/LoadingState"
import ErrorState from "./components/ErrorState"
import PlayerHeader from "./components/PlayerHeader"
import PlayerInfoCards from "./components/PlayerInfoCards"
import PersonalInfoCard from "./components/PersonalInfoCard"
import ValuationHistoryTable from "./components/ValuationHistoryTable"
import PlayerGraph from "./components/PlayerGraph"

function PlayerDetailsPage() {
  const [params] = useSearchParams()
  const nombre = params.get("name")
  const club = params.get("club")
  const season = params.get("season")
  
  const [playerData, setPlayerData] = useState(null)
  const [valuations, setValuations] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    const fetchData = async () => {
      if (!nombre || !club || !season) {
        setError("Faltan parámetros requeridos")
        setLoading(false)
        return
      }

      setLoading(true)
      setError(null)

      try {
        const payload = { nombre, club, season }
        const data = await getPlayerInfo(payload)
        
        if (data) {
          if (data.status === "success" && data.data) {
            setPlayerData(data)
            
            const valData = await playerValuation({
              player: nombre,
              club,
              season
            })
            setValuations(valData || [])
          } else if (data.message) {
            setError(data.message)
          } else if (data.error) {
            setError(data.error)
          } else {
            setError("No se encontró información del jugador")
          }
        } else {
          setError("No se encontró información del jugador")
        }
      } catch (err) {
        console.error("Error al obtener la info del jugador:", err)
        setError(err.message || "Error al cargar los datos")
      } finally {
        setLoading(false)
      }
    }

    fetchData()
  }, [nombre, club, season])
  const formatCurrency = (value) => {
    if (!value || value === 0) return "$0"
    return "$" + new Intl.NumberFormat('es-AR', {
      maximumFractionDigits: 0,
    }).format(value)
  }
  console.log(playerData)
  if (loading) {
    return <LoadingState />
  }

  if (error) {
    return <ErrorState error={error} />
  }

  return (
    <div className="min-h-screen bg-[#050816] text-white">
      <div className="max-w-6xl mx-auto py-8 px-4 space-y-6">
        <PlayerHeader />

        {playerData && (
          <>
            <PlayerInfoCards 
              playerData={playerData} 
              club={club} 
              season={season} 
              formatCurrency={formatCurrency} 
            />

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mt-4">
              <PersonalInfoCard playerData={playerData} />
              <PlayerGraph valuations={valuations} player={nombre} />
            </div>

            <ValuationHistoryTable playerData={playerData} formatCurrency={formatCurrency} />
          </>
        )}
      </div>
    </div>
  )
}

export default PlayerDetailsPage
