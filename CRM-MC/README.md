
# CRM Full Stack Application

Este projeto é um sistema CRM completo com:

- Backend em **FastAPI**
- Frontend em **React**
- Base de dados **PostgreSQL**
- Autenticação com **JWT**
- Deploy com **Docker Compose**

---

## 📁 Estrutura do Projeto

crm_project/
├── docker-compose.yml
├── README.md
├── crm_backend/
│   ├── Dockerfile
│   ├── main.py
│   ├── requirements.txt
│   ├── create_tables.py
│   ├── db/
│   │   └── database.py
│   ├── auth/
│   │   ├── auth_routes.py
│   │   └── dependencies.py
│   ├── models/
│   │   ├── user.py
│   │   ├── client.py
│   │   ├── equipment.py
│   │   ├── proposal.py
│   │   ├── assistance.py
│   │   └── calendar.py
│   ├── schemas/
│   │   ├── user.py
│   │   ├── client.py
│   │   ├── equipment.py
│   │   ├── proposal.py
│   │   ├── assistance.py
│   │   └── calendar.py
│   └── api/
│       ├── clients.py
│       ├── equipments.py
│       ├── proposals.py
│       ├── assistances.py
│       └── calendar.py
├── crm_frontend/
│   ├── package.json
│   └── src/
│       ├── index.js
│       ├── App.js
│       ├── axiosConfig.js
│       ├── components/
│       │   └── Navbar.js
│       └── pages/
│           ├── LoginPage.js
│           ├── Dashboard.js
│           ├── ClientsPage.js
│           ├── EquipmentsPage.js
│           ├── ProposalsPage.js
│           ├── AssistancesPage.js
│           └── CalendarPage.js

---

## 🚀 Como executar o projeto

### 1. Pré-requisitos

- Docker e Docker Compose instalados
- Node.js (se quiseres correr o frontend fora do Docker)

---

### 2. Executar com Docker

docker-compose up --build

- A API estará disponível em: http://localhost:8000/docs
- O frontend estará em: http://localhost:3000

---

### 3. Executar manualmente (sem Docker)

#### Backend

cd crm_backend
python -m venv venv
source venv/bin/activate  # ou venv\Scripts\activate no Windows
pip install -r requirements.txt
python create_tables.py
uvicorn main:app --reload

#### Frontend

cd crm_frontend
npm install
npm start

---

## 🔐 Autenticação

- Registo e login com JWT
- Proteção de rotas por tipo de utilizador (admin, tecnico, comercial)
- O token deve ser enviado no header Authorization: Bearer <token>

---

## 📌 Funcionalidades

- Gestão de clientes
- Gestão de equipamentos
- Gestão de propostas
- Assistências técnicas
- Calendário de eventos
- Autenticação e permissões

---

## 📦 Tecnologias

- FastAPI
- SQLAlchemy
- PostgreSQL
- React
- Axios
- Docker

---

## 📬 Contacto

Este projeto foi desenvolvido como base para personalização. Para dúvidas ou melhorias, entre em contacto com o autor.
