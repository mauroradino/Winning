function PlayerInfoCards({ playerData, club, season, formatCurrency }) {
  return (
    <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
      <div className="bg-[#0b1020] border border-[#1f2937] rounded-xl px-4 py-3 flex flex-col">
        <span className="text-xs text-gray-400 uppercase tracking-wide">Jugador</span>
        <span className="mt-1 font-semibold text-[#4ade80] text-lg">
          {playerData?.data?.['nombre y apellido'] || playerData?.name || ''}
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
  )
}

export default PlayerInfoCards

