"use client"

import { useEffect } from "react"
import { useRouter, useSearchParams } from "next/navigation"

export default function Page() {
  const router = useRouter()
  const params = useSearchParams()

  useEffect(() => {
    const token = params.get("token")

    if (!token) {
      router.replace("/login")
      return
    }

    localStorage.setItem("token", token)
    router.replace("/dashboard")
  }, [params, router])

  return <p>Autenticando...</p>
}
