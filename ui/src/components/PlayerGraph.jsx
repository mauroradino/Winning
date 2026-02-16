import { useEffect, useRef } from 'react'
import Chart from 'chart.js/auto'

function PlayerGraph({ valuations, player }) {
  const canvasRef = useRef(null)
  const chartRef = useRef(null)

  useEffect(() => {
    const ctx = canvasRef.current
    if (!ctx || !valuations || valuations.length === 0) return

    const labels = valuations.map((v) => v.valuation_date)
    const data = valuations.map((v) => v.valuation_amount)

    if (chartRef.current) {
      chartRef.current.destroy()
    }

    chartRef.current = new Chart(ctx, {
      type: 'line',
      data: {
        labels,
        datasets: [
          {
            label: `Precio de ${player || 'jugador'}`,
            data,
            borderWidth: 2,
            borderColor: 'rgba(74, 222, 128, 1)', 
            backgroundColor: 'rgba(74, 222, 128, 0.15)',
            pointBackgroundColor: 'rgba(74, 222, 128, 1)',
            pointBorderColor: '#020617',
            pointRadius: 4,
            pointHoverRadius: 5,
            tension: 0.3,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false },
          tooltip: {
            backgroundColor: '#020617',
            borderColor: '#1f2937',
            borderWidth: 1,
            titleColor: '#e5e7eb',
            bodyColor: '#9ca3af',
            padding: 20,
            displayColors: false,
            callbacks: {
              label: (ctx) =>
                `Valor: $${new Intl.NumberFormat('es-AR').format(ctx.parsed.y || 0)}`,
            },
          },
        },
        scales: {
          x: {
            grid: { color: 'rgba(31, 41, 55, 0.4)' },
            ticks: { color: '#6b7280', maxTicksLimit: 6 },
          },
          y: {
            beginAtZero: false,
            grid: { color: 'rgba(31, 41, 55, 0.4)' },
            ticks: {
              color: '#6b7280',
              callback: (value) =>
                '$' + new Intl.NumberFormat('es-AR', { notation: 'compact' }).format(value),
            },
          },
        },
      },
    })

    return () => {
      if (chartRef.current) {
        chartRef.current.destroy()
        chartRef.current = null
      }
    }
  }, [valuations, player])

  // --- COMPONENTE DE ESTADO VACÍO CON EL MISMO WRAPPER ---
  if (!valuations || valuations.length === 0) {
    return (
      <div className="lg:col-span-2"> {/* Mismo ancho que el gráfico original */}
        <div className="bg-[#0b1020] border border-[#1f2937] rounded-2xl p-6 h-full flex flex-col">
          <h2 className="text-lg font-semibold mb-4">Historial de Precio</h2>
          <div
            className="bg-[#020617] rounded-2xl mt-4 border border-[#1f2937] flex items-center justify-center"
            style={{ width: '100%', height: '320px' }}
          >
            <p className="text-sm text-gray-500 text-center px-4">
              No hay datos de valoraciones disponibles para {player || 'este jugador'}.
            </p>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="lg:col-span-2">
      <div className="bg-[#0b1020] border border-[#1f2937] rounded-2xl p-6 h-full flex flex-col">
        <div className="flex items-baseline justify-between mb-4">
          <div>
            <h2 className="text-lg font-semibold">Historial de Precio</h2>
            {player && (
              <p className="text-xs text-gray-400 mt-1">
                Seguimiento de valoración:{' '}
                <span className="text-emerald-400 font-medium">{player}</span>
              </p>
            )}
          </div>
        </div>
        <div
          className="bg-[#020617] rounded-2xl mt-4 border border-[#1f2937]"
          style={{ width: '100%', height: '320px' }}
        >
          <canvas ref={canvasRef} />
        </div>
      </div>
    </div>
  )
}

export default PlayerGraph