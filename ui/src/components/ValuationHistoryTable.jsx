function ValuationHistoryTable({ playerData, formatCurrency }) {
  if (!playerData?.valuations || playerData.valuations.length === 0) {
    return null
  }

  return (
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
  )
}

export default ValuationHistoryTable

