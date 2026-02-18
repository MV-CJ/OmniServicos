"use client"

import { useEffect, useRef, useState } from "react"
import { useRouter } from "next/navigation"
import { api } from "@/services/api"
import axios from "axios"

type User = {
  id: number
  name: string
  email: string
  picture?: string
}

export function useAuth() {
  const router = useRouter()
  const initialized = useRef(false)

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
      if (axios.isAxiosError(err) && err.response?.status === 401) {
        console.log("AUTH ERROR", err)

      }
    } finally {
      setLoading(false)
    }
  }

  function logout() {
    localStorage.removeItem("access_token")
    router.replace("/login")
  }

  useEffect(() => {
    if (initialized.current) return
    initialized.current = true

    const token = localStorage.getItem("access_token")
    if (!token) {
      router.replace("/login")
      return
    }

    loadUser()
  }, [])

  return { user, loading, logout }
}
