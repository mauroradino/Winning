import React, { useState } from 'react';

const YearSelect = ({ onSelect }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [selectedYear, setSelectedYear] = useState('');

  const years = ['2020', '2021', '2022', '2023', '2024', '2025'];

  const handleYearClick = (year) => {
    setSelectedYear(year);
    setIsOpen(false);
    onSelect(year); 
  };

  return (
    <div className="relative w-full"> {/* Más angosto para años */}
      <div 
        onClick={() => setIsOpen(!isOpen)}
        className="w-full bg-[#020617] border border-[#1f2937] rounded-lg px-3 py-2 text-sm text-white cursor-pointer flex justify-between items-center hover:border-emerald-500 transition-colors"
      >
        {selectedYear || "Seleccioná una Temporada"}
        <span className={`text-[10px] transform transition-transform ${isOpen ? 'rotate-180' : ''}`}>
          ▼
        </span>
      </div>

      {isOpen && (
        <ul className="absolute z-20 w-full mt-1 bg-[#020617] border border-[#1f2937] rounded-lg overflow-hidden shadow-xl border-t-0">
          {years.map((year) => (
            <li 
              key={year}
              onClick={() => handleYearClick(year)}
              className="px-3 py-2 text-sm text-white cursor-pointer hover:bg-emerald-500 hover:text-black transition-colors"
            >
              {year}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default YearSelect;