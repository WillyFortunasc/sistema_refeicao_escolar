import { createContext, useState } from 'react'

export const AuthContext = createContext()

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)

  function login() {
    // simulação de login
    setUser({
      nome: 'Willy',
      papel: 'operador', // pode mudar para: operador, empresa, fiscal, gestor
    })
  }

  function logout() {
    setUser(null)
  }

  return (
    <AuthContext.Provider value={{ user, login, logout }}>
      {children}
    </AuthContext.Provider>
  )
}
