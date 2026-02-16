import CustomSelect from "./CustomTeamSelect"

function PlayerSelector({players, onSelect}){
    return(
        <CustomSelect options={players} onSelect={onSelect}/>
    )
}

export default PlayerSelector