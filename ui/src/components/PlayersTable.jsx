import { useMemo } from 'react' 
import { useNavigate } from 'react-router-dom'

function PlayersTable({ players = [], club, season }) {
  const navigate = useNavigate()
  const valorTotalPlantel = useMemo(() => {
    return players.reduce((acc, p) => {
      const rawValue = p.valor ?? p.amount;
      const val = Number(rawValue);
      return acc + (isNaN(val) ? 0 : val);
    }, 0);
  }, [players]);

  const handleRowClick = (playerName) => {
    if (playerName && club && season) {
      const seasonYear = season.toString().slice(0, 4)
      navigate(`/details?name=${encodeURIComponent(playerName)}&season=${encodeURIComponent(seasonYear)}&club=${encodeURIComponent(club)}`)
      console.log(`/details?name=${encodeURIComponent(playerName)}&season=${encodeURIComponent(seasonYear)}&club=${encodeURIComponent(club)}`)
    }
  }

  return (
    <div className="w-full mt-6 bg-[#020617] border border-[#1f2937] rounded-2xl overflow-hidden ">
      <div className="px-4 py-3 border-b border-[#1f2937] flex items-center justify-between">
        <h2 className="text-sm font-semibold text-gray-100">PLANTEL</h2>
        <span className='text-sm text-gray-500'>
          Valor del plantel: 
          <span className="text-emerald-400 ml-1">
            ${new Intl.NumberFormat('es-AR').format(valorTotalPlantel)}
          </span>
        </span>
        <span className="text-xs text-gray-500">
          {players.length} jugadores
        </span>
      </div>

      <div className="overflow-x-auto">
        <table className="min-w-full text-sm text-left">
          <thead className="bg-[#0b1120] text-gray-400 text-xs uppercase tracking-wide">
            <tr>
              <th className="px-4 py-3">Jugador</th>
              <th className="px-4 py-3">Posición</th>
              <th className="px-4 py-3 text-right">Valor</th>
            </tr>
          </thead>
          <tbody>
            {players.length === 0 ? (
              <tr>
                <td colSpan={3} className="px-4 py-6 text-center text-xs text-gray-500">
                  No hay jugadores cargados todavía.
                </td>
              </tr>
            ) : (
              players.map((p) => {
                const rawValue = p.valor ?? p.amount;
                const hasValue = rawValue !== null && rawValue !== undefined && !isNaN(Number(rawValue)) && Number(rawValue) > 0;
                const playerName = p['nombre y apellido'] || p.player_name || p['player name'] || '';

                return (
                  <tr
                    key={p.player_id || p.nombre || Math.random()}
                    onClick={() => handleRowClick(playerName)}
                    className="border-t border-[#111827] hover:bg-[#0a0e1f] hover:cursor-pointer"
                  >
                    <td className="px-4 py-3 text-gray-100">{playerName}</td>
                    <td className="px-4 py-3 text-gray-300">{p.posicion || p.from_club || '-'}</td>
                    <td className="px-4 py-3 text-right">
                      {hasValue ? (
                        <span className="text-emerald-400">
                          {'$' + new Intl.NumberFormat('es-AR', {
                            maximumFractionDigits: 0,
                          }).format(rawValue)}
                        </span>
                      ) : (
                        <span className="text-emerald-500 font-medium">Libre / Cesión</span>
                      )}
                    </td>
                  </tr>
                );
              })
            )}
          </tbody>
        </table>
      </div>
    </div>
  )
}

export default PlayersTable