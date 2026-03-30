import { useContext } from 'react'
import { AuthContext } from '../context/AuthContext'
import { Navigate } from 'react-router-dom'

function PrivateRoute({ children, allowedRoles }) {
  const { user } = useContext(AuthContext)

  if (!user) {
    return <Navigate to="/login" />
  }

  if (allowedRoles && !allowedRoles.includes(user.papel)) {
    return <Navigate to="/login" />
  }

  return children
}

export default PrivateRoute
