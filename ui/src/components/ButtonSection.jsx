function ButtonSection({club, seasonYear, player, loading, handleGetPlayers, handleGetTransfers, handleGetAllData, showRevenue, showValuations, presupuestoFichajes}){
    return(
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
            Simular Calculos
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
    )
}

export default ButtonSection