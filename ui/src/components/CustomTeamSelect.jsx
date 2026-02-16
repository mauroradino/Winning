import React, { useState } from 'react';

const CustomSelect = ({ options, onSelect }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [selected, setSelected] = useState('');

  return (
    <div className="relative w-full max-w-md">
      {/* Botón del Select */}
      <div 
        onClick={() => setIsOpen(!isOpen)}
        className="w-full bg-[#020617] border border-[#1f2937] rounded-lg px-3 py-2 text-sm text-white cursor-pointer flex justify-between items-center hover:border-emerald-500 transition-colors"
      >
        {selected || "Seleccioná un Club"}
        <span className={`transform text-[10px] transition-transform ${isOpen ? 'rotate-180' : ''}`}>▼</span>
      </div>

      {/* Lista Desplegable Custom */}
      {isOpen && (
        <ul className="absolute z-10 w-full mt-1 bg-[#020617] border border-[#1f2937] rounded-lg overflow-hidden shadow-xl">
          {options.map((option) => (
            <li 
              key={option}
              onClick={() => {
                setSelected(option);
                setIsOpen(false);
                onSelect(option);
              }}
              className="px-3 py-2 text-sm text-white cursor-pointer hover:bg-emerald-500 transition-colors"
            >
              {option.toUpperCase()}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};


export default CustomSelect