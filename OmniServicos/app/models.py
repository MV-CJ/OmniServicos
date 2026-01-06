from .extensions import db
from datetime import datetime

# --- Modelos base ---
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Produto(db.Model):
    __tablename__ = "produtos"

    id = db.Column(db.Integer, primary_key=True)
    cd_sku = db.Column(db.String(50), unique=True, nullable=False)
    cd_ean = db.Column(db.String(13), unique=True, nullable=True)
    nome = db.Column(db.String(150), nullable=False)
    descricao = db.Column(db.Text)
    categoria = db.Column(db.String(100))
    vl_compra = db.Column(db.Float, nullable=False, default=0.0)     
    porcent_lucro = db.Column(db.Float, nullable=False, default=0.0)  
    vl_venda = db.Column(db.Float, nullable=False, default=0.0)       
    quantidade = db.Column(db.Integer, nullable=False, default=0)
    quantidade_minima = db.Column(db.Integer, nullable=False, default=0)
    peso_kg = db.Column(db.Float, default=0.0)
    largura_cm = db.Column(db.Float, default=0.0)
    altura_cm = db.Column(db.Float, default=0.0)
    profundidade_cm = db.Column(db.Float, default=0.0)
    foto_url = db.Column(db.String(300))
    ativo = db.Column(db.Boolean, default=True)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)
    atualizado_em = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "cd_sku": self.cd_sku,
            "cd_ean": self.cd_ean,
            "nome": self.nome,
            "descricao": self.descricao,
            "categoria": self.categoria,
            "vl_compra": self.vl_compra,
            "porcent_lucro": self.porcent_lucro,
            "vl_venda": self.vl_venda,
            "quantidade": self.quantidade,
            "peso_kg": self.peso_kg,
            "largura_cm": self.largura_cm,
            "altura_cm": self.altura_cm,
            "profundidade_cm": self.profundidade_cm,
            "foto_url": self.foto_url,
            "ativo": self.ativo,
            "criado_em": self.criado_em.isoformat(),
            "atualizado_em": self.atualizado_em.isoformat()
        }


# --- Módulos ---
class Customer(db.Model):  # CRM
    __tablename__ = "customers"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120))

# --- Plugins ---
class VidracariaOrder(db.Model):
    __tablename__ = "vidracaria_orders"
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
