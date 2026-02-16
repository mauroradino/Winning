import { useState } from "react"
import { callApi } from "../utils"
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm'

const MarkdownReport = ({ content }) => {
  return (
    <div className="w-full mx-auto my-6 bg-[#030712]/50 backdrop-blur-sm shadow-2xl rounded-2xl overflow-hidden">
      <div className="p-6 md:p-10">
        <article className="prose prose-invert prose-slate max-w-none 
          /* Títulos: Usamos el azul claro de tu tema */
          prose-headings:text-blue-400 prose-headings:font-bold
          prose-h1:text-3xl prose-h1:mb-8 prose-h1:tracking-tight
          
          /* Tablas: Estilo deportivo/financiero */
          prose-table:border-collapse
          prose-th:text-emerald-400 prose-th:border-b prose-th:border-slate-700 prose-th:py-3
          prose-td:border-b prose-td:border-slate-800/50 prose-td:py-4
          
          /* Enlaces y acentos: Usamos el verde del botón 'Generar' */
          prose-a:text-emerald-400 hover:prose-a:text-emerald-300
          prose-strong:text-blue-300
          
          /* Citas (Resumen IA): Fondo sutil para destacar el análisis */
          prose-blockquote:border-l-emerald-500 prose-blockquote:bg-emerald-500/5 
          prose-blockquote:text-slate-300 prose-blockquote:italic prose-blockquote:rounded-r-xl
          
          /* Listas */
          prose-li:marker:text-yellow-500">
          
          <ReactMarkdown remarkPlugins={[remarkGfm]}>
            {content}
          </ReactMarkdown>
        </article>
      </div>
    </div>
  );
};




function SeasonSummary({club, season, loading}){
  const [content, setContent] = useState("")
  const [isGenerating, setIsGenerating] = useState(false)

  const generateSummary = async () =>{
    setIsGenerating(true)
    setContent("") 
    try {
      const response = await callApi(`/summary/${club}/${season}`,{
        method: "POST"
      })
      setContent(response)
    } finally {
      setIsGenerating(false)
    }
  }

  return(
    <div className="w-full mt-6 bg-[#020617] border border-[#1f2937] rounded-2xl overflow-hidden ">
      <div className="px-4 py-3 border-b border-[#1f2937] flex items-center justify-between">
        <h2 className="text-sm font-semibold text-gray-100">RESUMEN DE TEMPORADA GENERADO POR IA</h2>
        {isGenerating ? (
          <p className="text-emerald-500 text-sm font-medium animate-pulse">Generando Resumen...</p>
        ) : loading ? (
          <p className="text-gray-400 text-sm">Cargando Datos...</p>
        ) : null}
        <button 
          onClick={generateSummary} 
          disabled={isGenerating || !club || !season}
          className="px-4 py-2 rounded-lg text-sm font-medium bg-emerald-500 hover:bg-emerald-400 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          {isGenerating ? "Procesando..." : "Generar Resumen"}
        </button>
      </div>
      {content && <MarkdownReport content={content}/>}
    </div>
  )
}

export default SeasonSummary