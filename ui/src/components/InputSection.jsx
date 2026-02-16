import PlayerSelector from './PlayerSelector'
import TeamSelector from './TeamSelector'
import YearSelect from './YearSelect'
function InputSection({club, players, onSelect, player, temporada, presupuestoFichajes, presupuestoSalarios, handleClubChange, handleYearChange, setPresupuestoFichajes, setPresupuestoSalarios, setPlayer}){
    return(
        <>
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
            <PlayerSelector players={players} onSelect={onSelect}/>
          </div>
        </div>
        </>
    )
}

export default InputSection