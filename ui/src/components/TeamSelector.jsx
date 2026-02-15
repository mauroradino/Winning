import clubsData from '../../../urls.json'; 
import CustomSelect from  './CustomTeamSelect'
const TransferSimulator = ({handle}) => {
  const clubsName = Object.keys(clubsData);
  return (
    <div className="w-full max-w-md mx-auto space-y-4">
      <div className="relative group ">
        <CustomSelect options={clubsName} onSelect={handle}/>
        <div className="absolute inset-y-0 right-0 flex items-center px-2 pointer-events-none text-gray-400 group-hover:text-white">
          <svg className="fill-current h-4 w-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20">
            <path d="M9.293 12.95l.707.707L15.657 8l-1.414-1.414L10 10.828 5.757 6.586 4.343 8z"/>
          </svg>
        </div>
      </div>
    </div>
  );
};

export default TransferSimulator;