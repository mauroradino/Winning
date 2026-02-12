function PurchaseTable({ players = [] }) {
  return (
    <div className="mt-6 bg-[#020617] border border-[#1f2937] rounded-2xl overflow-hidden">
      <div className="px-4 py-3 border-b border-[#1f2937] flex items-center justify-between">
        <h2 className="text-sm font-semibold text-gray-100">ALTAS</h2>
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
                <td
                  colSpan={3} // Corregido de 4 a 3 ya que hay 3 columnas
                  className="px-4 py-6 text-center text-xs text-gray-500"
                >
                  No hay jugadores cargados todavía.
                </td>
              </tr>
            ) : (
              players.map((p) => {
                // Obtenemos el valor numérico
                const rawValue = p.valor ?? p.amount;
                // Verificamos si es un número válido y mayor a 0
                const hasValue = rawValue !== null && rawValue !== undefined && !isNaN(Number(rawValue)) && Number(rawValue) > 0;

                return (
                  <tr
                    key={p.player_id || p.nombre}
                    className="border-t border-[#111827] hover:bg-[#020617]"
                  >
                    <td className="px-4 py-3 text-gray-100">
                      {p['nombre y apellido'] || p.player_name || p['player name']}
                    </td>
                    <td className="px-4 py-3 text-gray-300">
                      {p.posicion || p.from_club || '-'}
                    </td>
                    <td className="px-4 py-3 text-right">
                      {hasValue ? (
                        <span className="text-emerald-400">
                          {'$' + new Intl.NumberFormat('es-AR', {
                            maximumFractionDigits: 0,
                          }).format(rawValue)}
                        </span>
                      ) : (
                        <span className="text-emerald-500 font-medium">
                          Libre / Cesión
                        </span>
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

export default PurchaseTable