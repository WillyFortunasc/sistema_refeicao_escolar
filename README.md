# 🍽️ Sistema de Refeição Escolar

Sistema backend de gestão de refeições escolares com autenticação JWT, desenvolvido com Django REST Framework.

---

## 🚀 Backend

### 📦 Tecnologias
- Django 6
- Django REST Framework
- JWT (PyJWT)
- SQLite (desenvolvimento)

---

## 📁 Estrutura do projeto

sistema-refeicao-escolar/
│
├── core/                 # Configurações principais do Django
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│
├── api/                  # Regras do sistema (views, models, serializers)
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   ├── urls.py
│   └── tests/
│
├── seed.py               # Usuários de teste
├── manage.py             # Comando principal Django
├── requirements.txt      # Dependências
└── db.sqlite3            # Banco local

---

## ⚙️ Como rodar o projeto

python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

python manage.py migrate
python seed.py
python manage.py runserver

---

## 🌐 Acesso

API: http://localhost:8000/api/
Login: http://localhost:8000/api/login/
Health: http://localhost:8000/api/health/
Admin: http://localhost:8000/admin/

---

## 🔐 Autenticação

### Login (POST)
http://localhost:8000/api/login/

{
  "email": "admin@sistema.com",
  "senha": "Admin@123"
}

### Resposta

{
  "token": "JWT_TOKEN",
  "papel": "admin"
}

---

### Usando o token

Authorization: Bearer SEU_TOKEN

---

## 👤 Usuários de teste

Email | Senha | Papel
admin@sistema.com | Admin@123 | admin
operador@sistema.com | Oper@123 | operador
gestor@sistema.com | Gest@123 | gestor
empresa@sistema.com | Empr@123 | empresa

---

## 🔵 Endpoints principais

Método | Endpoint | Descrição
GET | /api/health/ | Status da API
POST | /api/login/ | Login
POST | /api/registro/ | Criar usuário (admin)
GET | /api/usuarios/ | Listar usuários
GET | /api/usuarios/<id>/ | Detalhe usuário
PATCH | /api/usuarios/<id>/ | Editar usuário
DELETE | /api/usuarios/<id>/ | Remover usuário

---