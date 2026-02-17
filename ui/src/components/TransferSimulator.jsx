import { useState, useEffect } from "react"
import PlayerSelector from "./PlayerSelector"
import TeamSelector from "./TeamSelector"
import YearSelect from "./YearSelect"
import { callApi, getPlayers } from "../utils"
import clubsData from '../../../urls.json'

function TransferSimulator() {
    const [clubOrigen, setClubOrigen] = useState('')
    const [clubDestino, setClubDestino] = useState('')
    const [jugadorSeleccionado, setJugadorSeleccionado] = useState('')
    const [jugadoresOrigen, setJugadoresOrigen] = useState([])
    const [jugadoresDestino, setJugadoresDestino] = useState([])
    const [temporada, setTemporada] = useState('2024')
    const [monto, setMonto] = useState(0)
    const [montoDisplay, setMontoDisplay] = useState('')
    const [loading, setLoading] = useState(false)
    const [transferiendo, setTransferiendo] = useState(false)
    const [transferencias, setTransferencias] = useState([])

    useEffect(() => {
        const fetchJugadoresOrigen = async () => {
            if (clubOrigen && temporada) {
                setLoading(true)
                try {
                    const players = await getPlayers(clubOrigen, temporada)
                    setJugadoresOrigen(players || [])
                } catch (error) {
                    console.error("Error cargando origen:", error)
                } finally {
                    setLoading(false)
                }
            }
        };
        fetchJugadoresOrigen()
    }, [clubOrigen, temporada])

    useEffect(() => {
        const fetchJugadoresDestino = async () => {
            if (clubDestino && temporada) {
                try {
                    const players = await getPlayers(clubDestino, temporada)
                    setJugadoresDestino(players || [])
                } catch (error) {
                    console.error("Error cargando destino:", error)
                }
            }
        };
        fetchJugadoresDestino()
    }, [clubDestino, temporada])

    const handleMonto = (e) => {
        const rawValue = e.target.value.replace(/\D/g, '')
        if (!rawValue) {
            setMontoDisplay('')
            setMonto(0)
            return
        }
        const formattedValue = new Intl.NumberFormat('es-AR').format(rawValue)
        setMontoDisplay(formattedValue)
        setMonto(Number(rawValue))
    }

    const handleTransferir = async () => {
    setTransferiendo(true)
    try {
        await callApi("/simulateTransfer", {
            method: 'POST',
            body: {
                "player": jugadorSeleccionado, 
                "season": temporada, 
                "from_club": clubOrigen, 
                "to_club": clubDestino,  
                "transfer_amount": monto
            }
        })

        const nuevaTrans = {
            jugador: jugadorSeleccionado,
            monto: montoDisplay,
            clubOrigen,
            clubDestino
        }
        setTransferencias([nuevaTrans, ...transferencias])

        setJugadorSeleccionado('')
        setMontoDisplay('')
        setMonto(0)

    } catch (error) {
        console.error("Error en la transferencia:", error)
        alert("Hubo un error al procesar la transferencia en el servidor.")
    } finally {
        setTransferiendo(false)
    }
}

    return (
        <div className="w-full mt-6 bg-[#020617] border border-[#1f2937] rounded-2xl overflow-hidden shadow-xl">
            <div className="px-4 py-3 border-b border-[#1f2937] bg-[#0b1120]">
                <h2 className="text-sm font-semibold text-gray-100 tracking-wider">SIMULADOR DE TRANSFERENCIAS</h2>
            </div>
            
            <div className="p-4 space-y-6">
                {/* Selectores Principales */}
                <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
                    <div className="flex flex-col gap-1">
                        <label className="text-[10px] text-gray-500 uppercase font-bold">Temporada</label>
                        <YearSelect onSelect={setTemporada} />
                    </div>
                    
                    <div className="flex flex-col gap-1">
                        <label className="text-[10px] text-gray-500 uppercase font-bold">Club Origen</label>
                        <TeamSelector handle={setClubOrigen} />
                    </div>

                    <div className="flex flex-col gap-1">
                        <label className="text-[10px] text-gray-500 uppercase font-bold">Jugador</label>
                        <PlayerSelector players={jugadoresOrigen} onSelect={setJugadorSeleccionado} />
                    </div>

                    <div className="flex flex-col gap-1">
                        <label className="text-[10px] text-gray-500 uppercase font-bold">Club Destino</label>
                        <TeamSelector handle={setClubDestino} />
                    </div>

                    <div className="flex flex-col gap-1">
                        <label className="text-[10px] text-gray-500 uppercase font-bold">Monto (€)</label>
                        <input 
                            value={montoDisplay}
                            onChange={handleMonto}
                            placeholder="0"
                            className="bg-[#020617] border border-[#1f2937] rounded-lg px-3 py-2 text-sm text-white outline-none focus:ring-2 focus:ring-emerald-500 transition-all" 
                            type="text" 
                        />
                    </div>
                </div>

                {/* Botón de Acción */}
                <div className="flex justify-end items-center gap-4 border-t border-[#1f2937] pt-4">
                    {loading && <span className="text-xs text-gray-500 animate-pulse">Cargando planteles...</span>}
                    <button
                        onClick={handleTransferir}
                        disabled={!jugadorSeleccionado || !clubOrigen || !clubDestino || loading || transferiendo}
                        className="px-6 py-2 rounded-lg text-sm font-bold bg-emerald-500 text-[#020617] hover:bg-emerald-400 disabled:opacity-30 disabled:cursor-not-allowed transition-all transform active:scale-95"
                    >
                        {transferiendo ? 'PROCESANDO...' : 'EJECUTAR TRANSFERENCIA'}
                    </button>
                </div>

                {/* Listas Comparativas de Planteles */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div className="bg-[#0b1120]/50 border border-[#1f2937] rounded-xl p-4">
                        <div className="flex justify-between items-center mb-3">
                            <h3 className="text-xs font-bold text-gray-400 uppercase">Plantel {clubOrigen}</h3>
                            <span className="text-[10px] bg-red-500/10 text-red-400 px-2 py-0.5 rounded">ORIGEN</span>
                        </div>
                        <div className="max-h-48 overflow-y-auto custom-scrollbar">
                            {jugadoresOrigen.length === 0 ? (
                                <p className="text-xs text-gray-600 italic">Selecciona un club para ver jugadores</p>
                            ) : (
                                <ul className="divide-y divide-[#1f2937]">
                                    {jugadoresOrigen.map((j, i) => (
                                        <li key={i} className="py-2 text-xs text-gray-300 hover:text-white transition-colors">
                                            {j["nombre y apellido"] || j.player_name || j.nombre}
                                        </li>
                                    ))}
                                </ul>
                            )}
                        </div>
                    </div>

                    <div className="bg-[#0b1120]/50 border border-[#1f2937] rounded-xl p-4">
                        <div className="flex justify-between items-center mb-3">
                            <h3 className="text-xs font-bold text-gray-400 uppercase">Plantel {clubDestino}</h3>
                            <span className="text-[10px] bg-blue-500/10 text-blue-400 px-2 py-0.5 rounded">DESTINO</span>
                        </div>
                        <div className="max-h-48 overflow-y-auto custom-scrollbar">
                            {jugadoresDestino.length === 0 ? (
                                <p className="text-xs text-gray-600 italic">Selecciona un destino</p>
                            ) : (
                                <ul className="divide-y divide-[#1f2937]">
                                    {jugadoresDestino.map((j, i) => (
                                        <li key={i} className="py-2 text-xs text-gray-300">
                                            {j["nombre y apellido"] || j.player_name || j.nombre}
                                        </li>
                                    ))}
                                </ul>
                            )}
                        </div>
                    </div>
                </div>

                {/* Historial de Transferencias */}
                <div className="bg-[#0b1120] border border-[#1f2937] rounded-xl p-4">
                    <h3 className="text-xs font-bold text-emerald-500 uppercase mb-3 flex items-center gap-2">
                        Registro de Movimientos - Temporada {temporada}
                    </h3>
                    <div className="max-h-40 overflow-y-auto">
                        {transferencias.length === 0 ? (
                            <div className="flex flex-col items-center py-4 text-gray-600">
                                <p className="text-xs">No se han realizado movimientos en esta sesión.</p>
                            </div>
                        ) : (
                            <div className="space-y-2">
                                {transferencias.map((t, i) => (
                                    <div key={i} className="flex items-center justify-between text-[11px] bg-[#020617] p-3 rounded-lg border border-[#1f2937]">
                                        <div className="flex items-center gap-2">
                                            <span className="font-bold text-white">{t.jugador}</span>
                                            <span className="text-gray-500">→</span>
                                            <span className="text-emerald-400 font-medium">€{t.monto}</span>
                                        </div>
                                        <div className="text-gray-500">
                                            {t.clubOrigen} <span className="mx-1">≫</span> {t.clubDestino}
                                        </div>
                                    </div>
                                ))}
                            </div>
                        )}
                    </div>
                </div>
            </div>
        </div>
    )
}

export default TransferSimulator