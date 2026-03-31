import { useContext } from 'react'
import { AuthContext } from '../context/AuthContext'
import { useNavigate } from 'react-router-dom'

function Login() {
  const { login } = useContext(AuthContext)
  const navigate = useNavigate()

  function handleLogin() {
    login()
    navigate('/home')
  }

  return (
    <div className="flex items-center justify-center h-screen bg-gray-100">
      <div className="bg-white p-8 rounded-2xl shadow-lg w-96">
        <h2 className="text-2xl font-bold mb-6 text-center">
          Login
        </h2>

        <input
          type="email"
          placeholder="Email"
          className="w-full mb-4 p-2 border rounded"
        />

        <input
          type="password"
          placeholder="Senha"
          className="w-full mb-4 p-2 border rounded"
        />

        <button
          onClick={handleLogin}
          className="w-full bg-blue-600 text-white p-2 rounded mb-4"
        >
          Entrar
        </button>

        <button className="w-full bg-red-500 text-white p-2 rounded flex items-center justify-center gap-2">
          🔐 Entrar com Google
        </button>
      </div>
    </div>
  )
}

export default Login
