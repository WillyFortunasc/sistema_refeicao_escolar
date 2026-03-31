import { useContext } from 'react'
import { AuthContext } from '../context/AuthContext'

function Navbar() {
  const { user } = useContext(AuthContext)

  return (
    <div className="bg-blue-600 text-white p-4 flex justify-between">
      <span>Sistema</span>

      <div>
        {user?.papel === 'admin' && <span className="mr-4">Admin Panel</span>}
        {user?.papel === 'operador' && <span className="mr-4">Operador Área</span>}
        {user?.papel === 'empresa' && <span className="mr-4">Empresa Área</span>}

        <span>{user?.nome}</span>
      </div>
    </div>
  )
}

export default Navbar
