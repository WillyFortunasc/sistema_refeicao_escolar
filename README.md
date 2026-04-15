# 🍽️ Sistema de Refeição Escolar

Sistema backend com Django REST Framework + JWT.

---

## 🚀 Backend

Tecnologias:
- Django 6
- Django REST Framework
- JWT (PyJWT)
- SQLite

---

## 📁 Estrutura do projeto

sistema-refeicao-escolar/
├── core/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│
├── api/
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   ├── urls.py
│   └── tests/
│
├── seed.py
├── manage.py
├── requirements.txt
└── db.sqlite3

---

## ⚙️ Como rodar

python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

python manage.py migrate
python seed.py
python manage.py runserver

---

## 🌐 Acesso

API: http://localhost:8000/api/
LOGIN: http://localhost:8000/api/login/
HEALTH: http://localhost:8000/api/health/
ADMIN: http://localhost:8000/admin/

---

## 🔐 Login

POST http://localhost:8000/api/login/

Body:
{
  "email": "admin@sistema.com",
  "senha": "Admin@123"
}

Resposta:
{
  "token": "JWT_TOKEN",
  "papel": "admin"
}

---

## 🔑 Token

Authorization: Bearer SEU_TOKEN

---

## 👤 Usuários de teste

admin@sistema.com | Admin@123 | admin
operador@sistema.com | Oper@123 | operador
gestor@sistema.com | Gest@123 | gestor
empresa@sistema.com | Empr@123 | empresa

---

## 🔵 Endpoints

GET    /api/health/
POST   /api/login/
POST   /api/registro/
GET    /api/usuarios/
GET    /api/usuarios/<id>/
PATCH  /api/usuarios/<id>/
DELETE /api/usuarios/<id>/

---
