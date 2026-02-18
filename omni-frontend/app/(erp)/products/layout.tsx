"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { isAuthenticated, logout } from "@/utils/auth";
import { LayoutDashboard, Package, Users, ShoppingCart, LogOut } from "lucide-react";
import Link from "next/link"

export default function ProdutosLayout({ children }: { children: React.ReactNode }) {
  const router = useRouter();
  const [authorized, setAuthorized] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem("token")

    if (!token) {
      router.replace("/login")
    } else {
      setAuthorized(true)
    }
  }, [])


  if (!authorized) {
    return (
      <div className="flex h-screen items-center justify-center text-slate-400">
        Verificando sessão...
      </div>
    );
  }

  return (
    <div className="flex min-h-screen bg-slate-950 text-white">
      {/* Sidebar */}
      <aside className="w-64 border-r border-white/10 bg-slate-900/60 backdrop-blur-xl">
        <div className="px-6 py-6 text-xl font-semibold">
          Omni<span className="text-indigo-400">Serviços</span>
        </div>

        <nav className="space-y-1 px-4">
          <NavItem icon={<LayoutDashboard size={18} />} label="Dashboard" href="/dashboard" />
          <NavItem icon={<Package size={18} />} label="Produtos" href="/erp/products" />
          <NavItem icon={<Users size={18} />} label="Clientes" href="/crm" />
          <NavItem icon={<ShoppingCart size={18} />} label="PDV" href="/pdv" />
        </nav>
      </aside>

      <div className="flex flex-1 flex-col">
        <header className="flex items-center justify-between border-b border-white/10 bg-slate-900/60 px-6 py-4 backdrop-blur-xl">
          <span className="text-sm text-slate-400">Bem-vindo 👋</span>

          <button
            onClick={() => {
              logout();
              router.replace("/login");
            }}
            className="flex items-center gap-2 text-sm text-red-400 hover:text-red-300"
          >
            <LogOut size={16} />
            Sair
          </button>
        </header>

        <main className="flex-1 p-8 bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950">
          {children}
        </main>
      </div>
    </div>
  );
}

function NavItem({ icon, label, href }: any) {
  return (
    <Link
      href={href}
      className="flex items-center gap-3 rounded-xl px-4 py-3 text-sm text-slate-300 hover:bg-white/5 hover:text-white"
    >
      {icon}
      {label}
    </Link>
  );
}
