import { Router, Routes, Route } from 'react-router-dom'
import HomePage from "./HomePage"
import PlayerDetailsPage from './PlayerDetailsPage'
function App(){
  
  return(
      <Routes>
        <Route path="/" element={<HomePage/>}/>
        <Route path="/details" element={<PlayerDetailsPage/>}/>
      </Routes>
  )
}

export default App