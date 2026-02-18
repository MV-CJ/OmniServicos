"use client"

import {
  createContext,
  useContext,
  useEffect,
  useState,
} from "react"
import { useRouter } from "next/navigation"
import axios from "axios"
import { api } from "@/services/api"

type User = {
  id: number
  name: string
  email: string
  picture?: string
}

type AuthContextData = {
  user: User | null
  loading: boolean
  logout: () => void
}

const AuthContext = createContext<AuthContextData | null>(null)

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const router = useRouter()
  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState(true)

  async function loadUser() {
    try {
      const { data } = await api.get("/users/me")
      setUser({
        id: data.id,
        name: data.name,
        email: data.email,
        picture: data.picture,
      })
    } catch (err) {
      // ❗ NÃO DESLOGA AQUI
      console.error("Auth load error:", err)
    } finally {
      setLoading(false)
    }
  }

  function logout() {
    localStorage.removeItem("access_token")
    setUser(null)
    router.replace("/login")
  }

  useEffect(() => {
    const token = localStorage.getItem("access_token")

    // ⛔ NÃO REDIRECIONA AQUI
    if (!token) {
      setLoading(false)
      return
    }

    loadUser()
  }, [])

  return (
    <AuthContext.Provider value={{ user, loading, logout }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error("useAuth must be used inside AuthProvider")
  }
  return context
}
