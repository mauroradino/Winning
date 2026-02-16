import { useNavigate } from "react-router-dom"

function PlayerHeader() {
  const navigate = useNavigate()
  
  return (
    <div className="flex items-center justify-between mb-6">
      <h1 className="text-4xl font-bold">Detalles del Jugador</h1>
      <button
        onClick={() => navigate("/")}
        className="px-4 py-2 rounded-lg text-sm font-medium bg-[#111827] hover:bg-[#1f2937]"
      >
        ← Volver
      </button>
    </div>
  )
}

export default PlayerHeader

