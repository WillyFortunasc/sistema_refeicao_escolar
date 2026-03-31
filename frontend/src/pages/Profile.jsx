import { useContext } from 'react'
import { AuthContext } from '../context/AuthContext'
import Navbar from '../components/Navbar'

function Profile() {
  const { user } = useContext(AuthContext)

  return (
    <div className="bg-gray-100 min-h-screen">
      <Navbar />

      <div className="flex items-center justify-center mt-20">
        <div className="bg-white p-10 rounded-2xl shadow-lg text-center">
          <h2 className="text-2xl font-bold mb-4">Perfil do Usuário</h2>

          <p><strong>Nome:</strong> {user?.nome}</p>
          <p><strong>Papel:</strong> {user?.papel}</p>
        </div>
      </div>
    </div>
  )
}

export default Profile
