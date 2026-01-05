# OmniServicos

OmniServicos é uma aplicação backend em **Flask** para gerenciamento empresarial, com módulos de **CRM**, **ERP**, **PDV** e suporte a **plugins** personalizados.  
O sistema é projetado para ser modular, escalável e fácil de manter, utilizando **blueprints** e **PostgreSQL** como banco de dados.

---

## 💡 Conceitos dos módulos

### CRM (Customer Relationship Management)
O CRM é responsável por **gerenciar clientes, leads e oportunidades de vendas**, permitindo acompanhar todas as interações e histórico de relacionamento.  

Funcionalidades principais:
- Cadastro de clientes e leads
- Pipeline de vendas
- Lembretes e tarefas automáticas
- Relatórios de performance e conversão

---

### ERP (Enterprise Resource Planning)
O ERP organiza os **processos internos da empresa**, como estoque, finanças e logística.  

Funcionalidades principais:
- Controle financeiro (contas a pagar/receber)
- Gestão de estoque e compras
- Planejamento de produção e logística
- Relatórios detalhados para tomada de decisão

---

### PDV (Ponto de Venda)
O PDV registra **vendas realizadas**, seja em loja física ou online, e atualiza automaticamente o ERP.  

Funcionalidades principais:
- Registro de vendas
- Emissão de cupom fiscal ou nota
- Controle de caixa
- Atualização de estoque

---

### Plugins
Plugins são funcionalidades adicionais que podem ser ativadas por conta, como:
- Vidraçaria
- Borracharia
- Cozinha

Eles se conectam aos módulos principais, podendo gerar dados no **CRM** (cliente), **ERP** (estoque/financeiro) ou **PDV** (vendas).

---

## 🔗 Relação entre módulos

O diagrama abaixo mostra como **CRM, ERP, PDV e plugins** interagem:

![Mapa da arquitetura](A_flowchart-style_digital_illustration_visually_re.png)

**Explicação do fluxo:**
1. **CRM** → gerencia clientes e oportunidades, envia informações para ERP ou PDV.
2. **ERP** → organiza toda a operação da empresa: estoque, finanças, compras. Recebe dados de vendas do PDV e clientes do CRM.
3. **PDV** → registra vendas, atualiza estoque no ERP, pode gerar dados para o CRM.
4. **Plugins** → funcionalidades específicas que se conectam a qualquer módulo principal.

---

## ⚙️ Tecnologias utilizadas
- Python 3.12
- Flask 3.1.2
- Flask-SQLAlchemy
- Flask-Migrate
- PostgreSQL 16
- Docker / Docker Compose

---

## 🚀 Como rodar a aplicação

### 1. Subir containers (App + PostgreSQL)

```bash
docker compose up -d
``` 

## ⚙️ Criar migrations (primeira vez)
Entre no container da app:
##### Inicializa migrations
flask db init

##### Gera a migration inicial
flask db migrate -m "Initial migration"

##### Aplica as migrations no banco
flask db upgrade

> Para alterações futuras nos modelos, basta rodar flask db migrate e flask db upgrade novamente.

## Testar rotas:

CRM: http://localhost:5000/crm/test

ERP: http://localhost:5000/erp/test

PDV: http://localhost:5000/pdv/test

Plugin Vidraçaria: http://localhost:5000/plugin/vidracaria/test