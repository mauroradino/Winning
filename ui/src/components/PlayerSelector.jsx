import CustomSelect from "./CustomTeamSelect"

function PlayerSelector({players, onSelect}){
    return(
        <CustomSelect options={players} onSelect={onSelect} title={"Selecciona un jugador"}/>
    )
}

export default PlayerSelector