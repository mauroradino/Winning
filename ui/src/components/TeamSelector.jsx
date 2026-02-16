import clubsData from '../../../urls.json'; 
import CustomSelect from  './CustomTeamSelect'
const TransferSimulator = ({handle}) => {
  const clubsName = Object.keys(clubsData);
  return (
    <div className="w-full max-w-md mx-auto space-y-4">
      <div className="relative group ">
        <CustomSelect options={clubsName} onSelect={handle}/>
      </div>
    </div>
  );
};

export default TransferSimulator;