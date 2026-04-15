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

```bash
sistema-refeicao-escolar/
│
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
```

---

## ⚙️ Como rodar o projeto

```bash
python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt

python manage.py migrate
python seed.py
python manage.py runserver
```

---

## 🌐 Acesso

- API: http://localhost:8000/api/
- Login: http://localhost:8000/api/login/
- Health: http://localhost:8000/api/health/
- Admin: http://localhost:8000/admin/

---

## 🔐 Autenticação

### Login (POST)

` POST http://localhost:8000/api/login/ `

` Body: 
{
  "email": "admin@sistema.com",

  "senha": "Admin@123"
}  `

`
### Resposta
{
  "token": "JWT_TOKEN",
  "papel": "admin"
}
`


### Usando token
` Authorization: Bearer SEU_TOKEN `

## 👤 Usuários de teste

| Email | Senha | Papel |
|------|------|------|
| admin@sistema.com | Admin@123 | admin |
| operador@sistema.com | Oper@123 | operador |
| gestor@sistema.com | Gest@123 | gestor |
| empresa@sistema.com | Empr@123 | empresa |

---

## 🔵 Endpoints principais

| Método | Endpoint | Descrição |
|--------|----------|------------|
| GET | /api/health/ | Status da API |
| POST | /api/login/ | Login |
| POST | /api/registro/ | Criar usuário (admin) |
| GET | /api/usuarios/ | Listar usuários |
| GET | /api/usuarios/<id>/ | Detalhe usuário |
| PATCH | /api/usuarios/<id>/ | Editar usuário |
| DELETE | /api/usuarios/<id>/ | Remover usuário |
```