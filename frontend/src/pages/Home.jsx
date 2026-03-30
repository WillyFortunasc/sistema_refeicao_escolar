import { useContext } from 'react'
import { AuthContext } from '../context/AuthContext'
import { useNavigate } from 'react-router-dom'

function Home() {
  const { logout } = useContext(AuthContext)
  const navigate = useNavigate()

  function handleLogout() {
    logout()
    navigate('/login')
  }

  return (
    <div className="flex flex-col items-center justify-center h-screen bg-gray-100">
      <div className="bg-white p-10 rounded-2xl shadow-lg text-center">
        <h1 className="text-3xl font-bold text-blue-600">
          Sistema de Refeição Escolar
        </h1>
        <p className="mt-4 text-gray-600">
          Você está logado 🚀
        </p>

        <button
          onClick={handleLogout}
          className="mt-6 bg-red-500 text-white px-4 py-2 rounded"
        >
          Sair
        </button>
      </div>
    </div>
  )
}

export default Home

