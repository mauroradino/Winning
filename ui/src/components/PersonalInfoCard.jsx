function PersonalInfoCard({ playerData }) {
  return (
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
  )
}

export default PersonalInfoCard

