import { useSearchParams, useNavigate } from "react-router-dom"
import { getPlayerInfo, playerValuation } from "./utils"
import { useEffect, useState } from "react"
import PlayerGraph from "./components/PlayerGraph"

function PlayerDetailsPage() {
  const [params] = useSearchParams()
  const navigate = useNavigate()
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
    return (
      <div className="min-h-screen bg-[#050816] text-white flex items-center justify-center">
        <div className="text-center">
          <p className="text-lg text-gray-400">Cargando información del jugador...</p>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="min-h-screen bg-[#050816] text-white flex items-center justify-center">
        <div className="text-center">
          <p className="text-lg text-red-400 mb-4">{error}</p>
          <button
            onClick={() => navigate("/")}
            className="px-4 py-2 rounded-lg text-sm font-medium bg-emerald-500 hover:bg-emerald-400"
          >
            Volver al inicio
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-[#050816] text-white">
      <div className="max-w-6xl mx-auto py-8 px-4 space-y-6">
        <div className="flex items-center justify-between mb-6">
          <h1 className="text-4xl font-bold">Detalles del Jugador</h1>
          <button
            onClick={() => navigate("/")}
            className="px-4 py-2 rounded-lg text-sm font-medium bg-[#111827] hover:bg-[#1f2937]"
          >
            ← Volver
          </button>
        </div>

        {playerData && (
          <>
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              <div className="bg-[#0b1020] border border-[#1f2937] rounded-xl px-4 py-3 flex flex-col">
                <span className="text-xs text-gray-400 uppercase tracking-wide">Jugador</span>
                <span className="mt-1 font-semibold text-[#4ade80] text-lg">
                  {playerData?.data?.['nombre y apellido'] || playerData?.name || nombre}
                </span>
              </div>

              <div className="bg-[#0b1020] border border-[#1f2937] rounded-xl px-4 py-3 flex flex-col">
                <span className="text-xs text-gray-400 uppercase tracking-wide">Club</span>
                <span className="mt-1 font-semibold">{playerData?.data?.club || club}</span>
              </div>

              <div className="bg-[#0b1020] border border-[#1f2937] rounded-xl px-4 py-3 flex flex-col">
                <span className="text-xs text-gray-400 uppercase tracking-wide">Temporada</span>
                <span className="mt-1 font-semibold">{season}</span>
              </div>

              <div className="bg-[#0b1020] border border-[#1f2937] rounded-xl px-4 py-3 flex flex-col">
                <span className="text-xs text-gray-400 uppercase tracking-wide">Valoración Actual</span>
                <span className="mt-1 font-semibold text-emerald-400">
                  {formatCurrency(playerData?.data?.valor || 0)}
                </span>
              </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mt-4">
              <div className="lg:col-span-1">
                <div className="bg-[#0b1020] border border-[#1f2937] rounded-2xl p-6 h-full">
                  <h2 className="text-lg font-semibold mb-4">Información Personal</h2>
                  <div className="space-y-4">
                    {playerData?.data?.posicion && (
                      <div className="flex justify-between items-center border-b border-[#1f2937] pb-2">
                        <span className="text-xs text-gray-400 uppercase">Posición</span>
                        <span className="text-sm font-medium">{playerData?.data?.posicion}</span>
                      </div>
                    )}
                    {playerData?.data?.edad && (
                      <div className="flex justify-between items-center border-b border-[#1f2937] pb-2">
                        <span className="text-xs text-gray-400 uppercase">Edad</span>
                        <span className="text-sm font-medium">{playerData?.data?.edad} años</span>
                      </div>
                    )}
                    {playerData?.data?.["pais de orígen"] && (
                      <div className="flex justify-between items-center border-b border-[#1f2937] pb-2">
                        <span className="text-xs text-gray-400 uppercase">Nacionalidad</span>
                        <span className="text-sm font-medium">{playerData?.data?.["pais de orígen"]}</span>
                      </div>
                    )}
                    {playerData?.data?.altura && (
                      <div className="flex justify-between items-center border-b border-[#1f2937] pb-2">
                        <span className="text-xs text-gray-400 uppercase">Altura</span>
                        <span className="text-sm font-medium">{playerData?.data?.altura} cm</span>
                      </div>
                    )}
                    {playerData?.data?.pie && (
                      <div className="flex justify-between items-center border-b border-[#1f2937] pb-2">
                        <span className="text-xs text-gray-400 uppercase">Pie</span>
                        <span className="text-sm font-medium">{playerData?.data?.pie}</span>
                      </div>
                    )}
                    {playerData?.data?.número && (
                      <div className="flex justify-between items-center border-b border-[#1f2937] pb-2">
                        <span className="text-xs text-gray-400 uppercase">Número</span>
                        <span className="text-sm font-medium">{playerData?.data?.número}</span>
                      </div>
                    )}
                  </div>
                </div>
              </div>

              <div className="lg:col-span-2">
                <div className="bg-[#0b1020] border border-[#1f2937] rounded-2xl p-6 h-full flex flex-col">
                  <div className="flex items-baseline justify-between mb-4">
                    <div>
                      <h2 className="text-lg font-semibold">Historial de Valoración</h2>
                      <p className="text-xs text-gray-400 mt-1">
                        Evolución del valor de mercado:{' '}
                        <span className="text-emerald-400 font-medium">{nombre}</span>
                      </p>
                    </div>
                  </div>
                  <PlayerGraph valuations={valuations} player={nombre} />
                </div>
              </div>
            </div>

            {playerData?.valuations && playerData.valuations.length > 0 && (
              <div className="bg-[#0b1020] border border-[#1f2937] rounded-2xl p-6 mt-6">
                <h2 className="text-lg font-semibold mb-4">Historial Completo de Valoraciones</h2>
                <div className="overflow-x-auto">
                  <table className="min-w-full text-sm text-left">
                    <thead className="bg-[#0b1120] text-gray-400 text-xs uppercase tracking-wide">
                      <tr>
                        <th className="px-4 py-3">Fecha</th>
                        <th className="px-4 py-3">Valoración</th>
                        <th className="px-4 py-3">Edad</th>
                        <th className="px-4 py-3">Club</th>
                      </tr>
                    </thead>
                    <tbody>
                      {playerData?.valuations?.map((val, index) => (
                        <tr
                          key={index}
                          className="border-t border-[#111827] hover:bg-[#020617]"
                        >
                          <td className="px-4 py-3 text-gray-100">
                            {val.valuation_date || val.date}
                          </td>
                          <td className="px-4 py-3 text-emerald-400 font-medium">
                            {formatCurrency(val.valuation_amount || val.amount)}
                          </td>
                          <td className="px-4 py-3 text-gray-300">
                            {val.age_at_valuation || val.age} años
                          </td>
                          <td className="px-4 py-3 text-gray-300">
                            {val.club_nombre || val.club || '-'}
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            )}
          </>
        )}
      </div>
    </div>
  )
}

export default PlayerDetailsPage
