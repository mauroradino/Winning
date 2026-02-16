import { useNavigate } from "react-router-dom"

function ErrorState({ error }) {
  const navigate = useNavigate()
  
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

export default ErrorState

