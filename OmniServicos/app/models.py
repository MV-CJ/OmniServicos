from .extensions import db
from datetime import datetime

class Empresa(db.Model):
    __tablename__ = "empresas"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150), nullable=False)
    cnpj = db.Column(db.String(20), unique=True)
    ativo = db.Column(db.Boolean, default=True)

    criado_em = db.Column(db.DateTime, default=datetime.utcnow)


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    empresa_id = db.Column(db.Integer, db.ForeignKey("empresas.id"), nullable=False)
    empresa = db.relationship("Empresa")

    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)

    role = db.Column(db.String(50), default="USER")
    # ADMIN | USER | GERENTE

    ativo = db.Column(db.Boolean, default=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Produto(db.Model):
    __tablename__ = "produtos"

    id = db.Column(db.Integer, primary_key=True)

    empresa_id = db.Column(db.Integer, db.ForeignKey("empresas.id"), nullable=False)
    empresa = db.relationship("Empresa")

    criado_por = db.Column(db.Integer, db.ForeignKey("users.id"))
    usuario_criacao = db.relationship("User")

    cd_sku = db.Column(db.String(50), nullable=False)
    cd_ean = db.Column(db.String(13))

    nome = db.Column(db.String(150), nullable=False)
    descricao = db.Column(db.Text)
    categoria = db.Column(db.String(100))

    vl_compra = db.Column(db.Float, nullable=False, default=0.0)
    porcent_lucro = db.Column(db.Float, nullable=False, default=0.0)
    vl_venda = db.Column(db.Float, nullable=False, default=0.0)

    quantidade = db.Column(db.Integer, nullable=False, default=0)
    quantidade_minima = db.Column(db.Integer, nullable=False, default=0)
    quantidade_alerta = db.Column(db.Integer, nullable=False, default=0)

    peso_kg = db.Column(db.Float, default=0.0)
    largura_cm = db.Column(db.Float, default=0.0)
    altura_cm = db.Column(db.Float, default=0.0)
    profundidade_cm = db.Column(db.Float, default=0.0)

    foto_url = db.Column(db.String(300))
    ativo = db.Column(db.Boolean, default=True)

    criado_em = db.Column(db.DateTime, default=datetime.utcnow)
    atualizado_em = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    __table_args__ = (
        db.UniqueConstraint("empresa_id", "cd_sku", name="uq_produto_empresa_sku"),
    )

    def to_dict(self):
        return {
            "id": self.id,
            "empresa_id": self.empresa_id,
            "cd_sku": self.cd_sku,
            "cd_ean": self.cd_ean,
            "nome": self.nome,
            "descricao": self.descricao,
            "categoria": self.categoria,
            "vl_compra": self.vl_compra,
            "porcent_lucro": self.porcent_lucro,
            "vl_venda": self.vl_venda,
            "quantidade": self.quantidade,
            "quantidade_minima": self.quantidade_minima,
            "quantidade_alerta": self.quantidade_alerta,
            "ativo": self.ativo,
            "criado_em": self.criado_em.isoformat(),
            "atualizado_em": self.atualizado_em.isoformat(),
        }

class EstoqueMovimentacao(db.Model):
    __tablename__ = "estoque_movimentacoes"

    id = db.Column(db.Integer, primary_key=True)

    empresa_id = db.Column(db.Integer, db.ForeignKey("empresas.id"), nullable=False)
    empresa = db.relationship("Empresa")

    produto_id = db.Column(db.Integer, db.ForeignKey("produtos.id"), nullable=False)
    produto = db.relationship("Produto")

    usuario_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    usuario = db.relationship("User")

    tipo = db.Column(db.String(20), nullable=False)
    # ENTRADA | SAIDA | AJUSTE | DEVOLUCAO

    origem = db.Column(db.String(50))
    # COMPRA | VENDA | INVENTARIO | MANUAL

    quantidade = db.Column(db.Integer, nullable=False)
    saldo_anterior = db.Column(db.Integer, nullable=False)
    saldo_atual = db.Column(db.Integer, nullable=False)

    motivo = db.Column(db.String(255))

    criado_em = db.Column(db.DateTime, default=datetime.utcnow)
