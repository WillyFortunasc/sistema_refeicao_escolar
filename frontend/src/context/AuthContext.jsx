import { createContext, useState } from 'react'
import axios from 'axios'

export const AuthContext = createContext()

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)

  async function login(email, senha) {
    try {
      const response = await axios.post(
        'http://127.0.0.1:8000/api/login/',
        {
          email,
          senha,
        }
      )

      const { token, papel } = response.data

      // salva token
      localStorage.setItem('token', token)

      // salva usuário
      setUser({
        email,
        papel,
      })

      return true
    } catch (error) {
      console.error(error)
      return false
    }
  }

  function logout() {
    localStorage.removeItem('token')
    setUser(null)
  }

  return (
    <AuthContext.Provider value={{ user, login, logout }}>
      {children}
    </AuthContext.Provider>
  )
}
