import { useState } from 'react'
import { queryAgent } from '../utils'

function ChatAgent() {
  const [isOpen, setIsOpen] = useState(false)
  const [messages, setMessages] = useState([
    { from: 'agent', text: 'Hola, soy tu asistente. ¿En qué te puedo ayudar?' },
  ])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)

  const handleSend = async (e) => {
    e.preventDefault()
    const text = input.trim()
    if (!text) return

    setMessages((prev) => [...prev, { from: 'user', text }])
    setInput('')

    try {
      setLoading(true)
      const agentResponse = await queryAgent(text, messages)
      const answer =
        typeof agentResponse === 'string'
          ? agentResponse
          : agentResponse?.answer ||
            'No he podido generar una respuesta en este momento.'

      setMessages((prev) => [...prev, { from: 'agent', text: answer }])
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        {
          from: 'agent',
          text: 'Hubo un error al consultar al agente. Revisa la consola del servidor.',
        },
      ])
    } finally {
      setLoading(false)
    }
  }

  return (
    <>
      {/* Ventana de chat */}
      {isOpen && (
        <div className="fixed bottom-24 right-6 w-80 max-h-[60vh] bg-[#020617] border border-[#1f2937] rounded-2xl shadow-xl flex flex-col z-50">
          <div className="px-4 py-3 border-b border-[#1f2937] flex items-center justify-between">
            <div>
              <p className="text-sm font-semibold text-white">Chat con el agente</p>
              <p className="text-xs text-gray-400">Asistente para dudas y análisis</p>
            </div>
            <button
              onClick={() => setIsOpen(false)}
              className="text-gray-400 hover:text-gray-200 text-lg leading-none"
            >
              ×
            </button>
          </div>

          <div className="flex-1 overflow-y-auto px-3 py-2 space-y-2 text-sm">
            {messages.map((msg, idx) => (
              <div
                key={idx}
                className={`flex ${
                  msg.from === 'user' ? 'justify-end' : 'justify-start'
                }`}
              >
                <div
                  className={`px-3 py-2 rounded-2xl max-w-[80%] ${
                    msg.from === 'user'
                      ? 'bg-emerald-500 text-black rounded-br-sm'
                      : 'bg-[#0b1120] text-gray-100 rounded-bl-sm'
                  }`}
                >
                  {msg.text}
                </div>
              </div>
            ))}
          </div>

          <form onSubmit={handleSend} className="border-t border-[#1f2937] p-2 flex gap-2">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Escribe tu mensaje..."
              className="flex-1 bg-[#020617] border border-[#1f2937] rounded-xl px-3 py-2 text-xs text-white outline-none focus:ring-2 focus:ring-emerald-500"
            />
             <button
               type="submit"
               disabled={loading}
               className="px-3 py-2 rounded-xl bg-emerald-500 hover:bg-emerald-400 text-xs font-semibold text-black disabled:opacity-50"
             >
               {loading ? '...' : 'Enviar'}
             </button>
          </form>
        </div>
      )}

      {/* Botón flotante circular */}
      <button
        type="button"
        onClick={() => setIsOpen((prev) => !prev)}
        className="fixed bottom-6 right-6 w-14 h-14 rounded-full bg-emerald-500 hover:bg-emerald-400 text-black shadow-xl flex items-center justify-center text-2xl font-bold z-40"
        aria-label="Abrir chat con el agente"
      >
        ?
      </button>
    </>
  )
}

export default ChatAgent


