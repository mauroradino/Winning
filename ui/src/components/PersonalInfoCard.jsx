function PersonalInfoCard({ playerData }) {
  const d = playerData?.data || {};
  let alturaFinal = d.altura;
  let pieFinal = d.pie;

  if (typeof d.pie === 'string' && d.pie.includes('m') && (!d.altura || !String(d.altura).includes('m'))) {
    alturaFinal = d.pie;
    pieFinal = d.altura;
  } 
  else if (d.altura && String(d.altura).includes('m')) {
    alturaFinal = d.altura;
    pieFinal = d.pie;
  }

  return (
    <div className="lg:col-span-1">
      <div className="bg-[#0b1020] border border-[#1f2937] rounded-2xl p-6 h-full">
        <h2 className="text-lg font-semibold mb-4">Información Personal</h2>
        <div className="space-y-4">
          
          <div className="flex justify-between items-center border-b border-[#1f2937] pb-2">
            <span className="text-xs text-gray-400 uppercase">Posición</span>
            <span className="text-sm font-medium">{d.posicion || '-'}</span>
          </div>

          <div className="flex justify-between items-center border-b border-[#1f2937] pb-2">
            <span className="text-xs text-gray-400 uppercase">Edad</span>
            <span className="text-sm font-medium">{d.edad ? `${d.edad} años` : '-'}</span>
          </div>

          <div className="flex justify-between items-center border-b border-[#1f2937] pb-2">
            <span className="text-xs text-gray-400 uppercase">Nacionalidad</span>
            <span className="text-sm font-medium">{d["pais de orígen"] || '-'}</span>
          </div>

          <div className="flex justify-between items-center border-b border-[#1f2937] pb-2">
            <span className="text-xs text-gray-400 uppercase">Altura</span>
            <span className="text-sm font-medium">{alturaFinal || '-'}</span>
          </div>

          <div className="flex justify-between items-center border-b border-[#1f2937] pb-2">
            <span className="text-xs text-gray-400 uppercase">Pie</span>
            <span className="text-sm font-medium">{pieFinal || '-'}</span>
          </div>

          <div className="flex justify-between items-center border-b border-[#1f2937] pb-2">
            <span className="text-xs text-gray-400 uppercase">Número</span>
            <span className="text-sm font-medium">{d.número || '-'}</span>
          </div>

        </div>
      </div>
    </div>
  )
}

export default PersonalInfoCard