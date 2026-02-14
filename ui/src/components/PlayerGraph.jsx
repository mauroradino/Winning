import { useEffect, useRef } from 'react'
import Chart from 'chart.js/auto'

function PlayerGraph({ valuations, player }) {
  const canvasRef = useRef(null)
  const chartRef = useRef(null)

  useEffect(() => {
    const ctx = canvasRef.current
    if (!ctx) return

    if (!valuations || valuations.length === 0) return

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
          legend: {
            display: false,
          },
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
                `Valor: $${new Intl.NumberFormat('es-AR').format(
                  ctx.parsed.y || 0
                )}`,
            },
          },
        },
        scales: {
          x: {
            grid: {
              color: 'rgba(31, 41, 55, 0.4)',
            },
            ticks: {
              color: '#6b7280',
              maxTicksLimit: 6,
            },
          },
          y: {
            beginAtZero: false,
            grid: {
              color: 'rgba(31, 41, 55, 0.4)',
            },
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

  if (!valuations || valuations.length === 0) {
    return (
      <div
        className="bg-[#020617] rounded-2xl mt-4 border border-[#1f2937] flex items-center justify-center"
        style={{ width: '100%', height: '320px' }}
      >
        <p className="text-sm text-gray-500">
          No hay datos de valoraciones para mostrar.
        </p>
      </div>
    )
  }

  return (
    <div
      className="bg-[#020617] rounded-2xl mt-4 border border-[#1f2937]"
      style={{ width: '100%', height: '320px' }}
    >
      <canvas ref={canvasRef} />
    </div>
  )
}

export default PlayerGraph