import { Routes, Route } from 'react-router-dom'
import HomePage from './HomePage'
import PlayerDetailsPage from './PlayerDetailsPage'
import ChatAgent from './components/ChatAgent'

function App() {
  return (
    <>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/details" element={<PlayerDetailsPage />} />
      </Routes>
      <ChatAgent />
    </>
  )
}

export default App
