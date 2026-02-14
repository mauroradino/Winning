function RevenueCard({ presupuesto, ganancia, restante, gasto, ingreso }) {
  const formatCurrency = (value) => {
    return new Intl.NumberFormat('es-AR', {
      maximumFractionDigits: 0,
    }).format(value || 0);
  };

  const isHealthy = restante >= 0;

  return (
    <div className="flex flex-col gap-4 text-sm text-gray-200">
      {/* Presupuesto inicial */}
      <div className="flex items-center justify-between">
        <span className="text-xs uppercase tracking-wide text-gray-400">
          Presupuesto inicial
        </span>
        <span className="text-lg font-semibold">
          ${formatCurrency(presupuesto)}
        </span>
      </div>

      {/* Gasto en transferencias */}
      <div className="flex items-center justify-between">
        <span className="text-xs uppercase tracking-wide text-gray-400">
          Gasto en transferencias
        </span>
        <span className="text-lg font-semibold text-red-400">
          -${formatCurrency(Math.abs(gasto || 0))}
        </span>
      </div>

      {/* Ingreso por ventas */}
      <div className="flex items-center justify-between">
        <span className="text-xs uppercase tracking-wide text-gray-400">
          Ingreso por ventas
        </span>
        <span className="text-lg font-semibold text-emerald-400">
          +${formatCurrency(Math.abs(ingreso || 0))}
        </span>
      </div>
      {/* Presupuesto restante */}
      <div className="flex items-center justify-between border-t border-[#1f2937] pt-3 mt-1">
        <span className="text-xs uppercase tracking-wide text-gray-400">
          Presupuesto restante
        </span>
        <span
          className={`text-lg font-semibold ${
            restante >= 0 ? 'text-emerald-400' : 'text-red-400'
          }`}
        >
          {restante >= 0 ? '+' : '-'}${formatCurrency(Math.abs(restante))}
        </span>
      </div>

      {/* Estado */}
      <div className="mt-3 rounded-lg bg-[#020617] border border-[#1f2937] px-3 py-3 flex gap-3 items-start">
        <span
          className={`mt-1 h-2 w-2 rounded-full ${
            isHealthy ? 'bg-emerald-400' : 'bg-red-400'
          }`}
        />
        <div className="text-xs text-gray-400 leading-relaxed">
          {isHealthy
            ? 'Sus finanzas están equilibradas. No se han detectado desviaciones significativas para la temporada actual.'
            : 'Advertencia: el presupuesto restante es negativo. Revise sus operaciones de mercado para equilibrar las finanzas.'}
        </div>
      </div>
    </div>
  );
}

export default RevenueCard;