"use client";

import { useEffect, useState } from "react";
import { api } from "@/services/api";
import { Trash, Edit, Plus } from "lucide-react";

interface Produto {
  id: number;
  cd_sku: string;
  nome: string;
  quantidade: number;
  vl_venda: number;
  ativo: boolean;
}

export default function ProdutosPage() {
  const [produtos, setProdutos] = useState<Produto[]>([]);
  const [loading, setLoading] = useState(true);
  const [modalOpen, setModalOpen] = useState(false);

  const [novoProduto, setNovoProduto] = useState({
    cd_sku: "",
    nome: "",
    quantidade: 0,
    vl_venda: 0,
  });

  const fetchProdutos = async () => {
    try {
      const res = await api.get("/products");
      setProdutos(res.data.produtos);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchProdutos();
  }, []);

  const handleCriarProduto = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const res = await api.post("/products", novoProduto);
      setProdutos((prev) => [...prev, res.data]);
      setModalOpen(false);
      setNovoProduto({ cd_sku: "", nome: "", quantidade: 0, vl_venda: 0 });
    } catch (err: any) {
      alert(err.response?.data?.error || "Erro ao criar produto");
    }
  };

  if (loading) return <p>Carregando produtos...</p>;

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-semibold">Produtos</h1>
        <button
          onClick={() => setModalOpen(true)}
          className="flex items-center gap-2 rounded bg-indigo-600 px-4 py-2 text-sm font-medium hover:bg-indigo-500"
        >
          <Plus size={16} />
          Novo Produto
        </button>
      </div>

      <table className="w-full table-auto border-collapse bg-slate-900/80 border border-white/10 rounded-xl overflow-hidden">
        <thead className="bg-slate-900/60">
          <tr>
            <th className="px-4 py-2 text-left">SKU</th>
            <th className="px-4 py-2 text-left">Nome</th>
            <th className="px-4 py-2 text-left">Qtd</th>
            <th className="px-4 py-2 text-left">Preço</th>
            <th className="px-4 py-2 text-left">Ativo</th>
            <th className="px-4 py-2 text-left">Ações</th>
          </tr>
        </thead>
        <tbody>
          {produtos.map((p) => (
            <tr key={p.id} className="hover:bg-white/5">
              <td className="px-4 py-2">{p.cd_sku}</td>
              <td className="px-4 py-2">{p.nome}</td>
              <td className="px-4 py-2">{p.quantidade}</td>
              <td className="px-4 py-2">R$ {p.vl_venda.toFixed(2)}</td>
              <td className="px-4 py-2">{p.ativo ? "✅" : "❌"}</td>
              <td className="px-4 py-2 flex gap-2">
                <button className="p-1 rounded bg-yellow-500 hover:bg-yellow-400">
                  <Edit size={16} />
                </button>
                <button className="p-1 rounded bg-red-500 hover:bg-red-400">
                  <Trash size={16} />
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      {modalOpen && (
        <div className="fixed inset-0 flex items-center justify-center bg-black/50 z-50">
          <div className="bg-slate-900 rounded-xl p-6 w-96 space-y-4">
            <h2 className="text-lg font-semibold">Criar Produto</h2>
            <form onSubmit={handleCriarProduto} className="space-y-3">
              <input
                type="text"
                placeholder="SKU"
                value={novoProduto.cd_sku}
                onChange={(e) =>
                  setNovoProduto((prev) => ({ ...prev, cd_sku: e.target.value }))
                }
                className="w-full rounded-xl bg-slate-950 border border-white/10 px-3 py-2 text-sm text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                required
              />
              <input
                type="text"
                placeholder="Nome"
                value={novoProduto.nome}
                onChange={(e) =>
                  setNovoProduto((prev) => ({ ...prev, nome: e.target.value }))
                }
                className="w-full rounded-xl bg-slate-950 border border-white/10 px-3 py-2 text-sm text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                required
              />
              <input
                type="number"
                placeholder="Quantidade"
                value={novoProduto.quantidade}
                onChange={(e) =>
                  setNovoProduto((prev) => ({ ...prev, quantidade: Number(e.target.value) }))
                }
                className="w-full rounded-xl bg-slate-950 border border-white/10 px-3 py-2 text-sm text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                required
              />
              <input
                type="number"
                step="0.01"
                placeholder="Preço de venda"
                value={novoProduto.vl_venda}
                onChange={(e) =>
                  setNovoProduto((prev) => ({ ...prev, vl_venda: Number(e.target.value) }))
                }
                className="w-full rounded-xl bg-slate-950 border border-white/10 px-3 py-2 text-sm text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                required
              />
              <div className="flex justify-end gap-2 mt-2">
                <button
                  type="button"
                  onClick={() => setModalOpen(false)}
                  className="px-4 py-2 rounded bg-gray-600 hover:bg-gray-500"
                >
                  Cancelar
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 rounded bg-indigo-600 hover:bg-indigo-500"
                >
                  Criar
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
