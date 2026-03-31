import { useContext } from 'react'
import { AuthContext } from '../context/AuthContext'
import { Link } from 'react-router-dom'

function Navbar() {
  const { user } = useContext(AuthContext)

  return (
    <div className="bg-blue-600 text-white p-4 flex justify-between">
      <span>Sistema</span>

      <div>
        <Link to="/home" className="mr-4">Home</Link>
        <Link to="/profile" className="mr-4">Perfil</Link>

        {user?.papel === 'admin' && <span className="mr-4">Admin Panel</span>}
        {user?.papel === 'operador' && <span className="mr-4">Operador Área</span>}

        <span>{user?.nome}</span>
      </div>
    </div>
  )
}

export default Navbar
