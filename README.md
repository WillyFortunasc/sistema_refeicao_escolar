# 🍽️ Sistema de Refeição Escolar

Sistema de gestão de refeições escolares com autenticação via JWT e Google OAuth2, desenvolvido com Django REST Framework no backend e React + Vite no frontend.

---

## 📋 Índice

1. [Configuração do ambiente no Windows com VSCode](#1-configuração-do-ambiente-no-windows-com-vscode)
2. [Estrutura do projeto e bibliotecas utilizadas](#2-estrutura-do-projeto-e-bibliotecas-utilizadas)
3. [Como rodar o projeto localmente](#3-como-rodar-o-projeto-localmente)
4. [Como testar os endpoints](#4-como-testar-os-endpoints)
5. [Autenticação — como funciona e como testar](#5-autenticação--como-funciona-e-como-testar)

---

## 1. Configuração do ambiente no Windows com VSCode

### Pré-requisitos

Instale as ferramentas abaixo antes de começar:

| Ferramenta | Link | Versão recomendada |
|---|---|---|
| Python | https://www.python.org/downloads/ | 3.11 ou superior |
| Node.js | https://nodejs.org/ | 18 LTS ou superior |
| Git | https://git-scm.com/download/win | Última versão |
| VSCode | https://code.visualstudio.com/ | Última versão |

> **Atenção durante a instalação do Python:** marque a opção **"Add Python to PATH"** na primeira tela do instalador.

### Extensões recomendadas do VSCode

Abra o VSCode, vá em **Extensions** (`Ctrl+Shift+X`) e instale:

- `Python` (Microsoft)
- `Pylance` (Microsoft)
- `ES7+ React/Redux/React-Native snippets`
- `Tailwind CSS IntelliSense`
- `REST Client` (para testar endpoints diretamente no editor)
- `GitLens`

### Clonar o repositório

Abra o terminal integrado do VSCode (`Ctrl+`` `):

```bash
git clone <URL_DO_REPOSITORIO>
cd sistema-refeicao-escolar
```

### Configurar o ambiente virtual Python

```bash
# Criar o ambiente virtual
python -m venv venv

# Ativar o ambiente virtual (Windows)
venv\Scripts\activate

# Confirmar que está ativo — o terminal deve exibir (venv) no início
```

> Se o PowerShell bloquear a execução de scripts, execute primeiro:
> `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

### Instalar dependências Python

```bash
pip install -r requirements.txt
```

### Configurar as variáveis de ambiente

Copie o arquivo de exemplo e edite com suas configurações:

```bash
copy .env.example .env
```

Abra o `.env` no VSCode e preencha:

```env
SECRET_KEY=uma-chave-secreta-longa-e-aleatoria
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0
CORS_ALLOWED_ORIGINS=http://localhost:5173

# Deixe em branco para desenvolvimento
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=
GOOGLE_REDIRECT_URI=http://localhost:8000/api/auth/google/callback/
GOOGLE_ALLOWED_DOMAINS=
```

> Para gerar uma `SECRET_KEY` segura, execute no terminal Python:
> ```python
> python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
> ```

### Configurar o banco de dados

```bash
python manage.py migrate
```

### Instalar dependências do frontend

```bash
cd frontend
npm install
cd ..
```

O ambiente está configurado. Prossiga para a seção 3 para rodar o projeto.

---

## 2. Estrutura do projeto e bibliotecas utilizadas

### Estrutura de diretórios

```
sistema-refeicao-escolar/
│
├── core/                       # App principal Django (configurações, URLs raiz)
│   ├── settings.py             # Configurações do projeto (banco, auth, CORS, etc.)
│   ├── urls.py                 # Roteamento principal
│   ├── models.py               # Modelo de usuário customizado (Usuario)
│   ├── serializers.py          # Serializer base do usuário
│   ├── permissions.py          # Classes de permissão por papel (IsFiscal, IsGestor…)
│   ├── admin.py                # Configuração do painel admin
│   ├── wsgi.py / asgi.py       # Entrypoints de deploy
│   └── apps.py                 # Registro de apps (AUTH_USER_MODEL)
│
├── api/                        # App secundário com views, serializers e testes
│   ├── models.py               # Modelo Usuario com UsuarioManager
│   ├── views.py                # Views: RegistroView, LoginView
│   ├── serializers.py          # UsuarioSerializer, RegistroSerializer, LoginSerializer
│   ├── permissions.py          # Permissões granulares por papel
│   ├── urls.py                 # Rotas do app api
│   └── tests/
│       └── test_auth.py        # Suite completa de testes automatizados
│
├── frontend/                   # Aplicação React
│   ├── src/
│   ├── package.json
│   └── vite.config.js
│
├── manage.py                   # CLI do Django
├── seed.py                     # Script para popular o banco com usuários de teste
├── requirements.txt            # Dependências Python
└── .env.example                # Modelo de variáveis de ambiente
```

### Backend — bibliotecas Python

| Biblioteca | Versão | Finalidade |
|---|---|---|
| **Django** | 6.0.3 | Framework web principal — ORM, autenticação, admin, migrations |
| **djangorestframework** | 3.17.0 | Construção da API REST — views, serializers, permissions, autenticação JWT |
| **django-cors-headers** | 4.9.0 | Permite requisições cross-origin do frontend React (`localhost:5173`) |
| **python-dotenv** | 1.2.2 | Leitura das variáveis de ambiente do arquivo `.env` |
| **psycopg2-binary** | 2.9.11 | Driver PostgreSQL (usado apenas em produção; em dev usa SQLite) |
| **PyJWT** | — | Geração e validação de tokens JWT para autenticação stateless |

### Frontend — bibliotecas JavaScript

| Biblioteca | Finalidade |
|---|---|
| **React** | Biblioteca principal para construção da interface |
| **Vite** | Bundler e servidor de desenvolvimento rápido |
| **TailwindCSS** | Estilização com classes utilitárias |
| **Axios** | Cliente HTTP para comunicação com a API Django |

### Modelo de usuário e papéis

O sistema utiliza um modelo `Usuario` customizado (substituindo o `User` padrão do Django) com os seguintes papéis:

| Papel | Descrição |
|---|---|
| `admin` | Acesso total — pode criar, listar, editar e deletar usuários |
| `gestor` | Acesso gerencial |
| `fiscal` | Acesso de fiscalização |
| `empresa` | Acesso da empresa fornecedora |
| `operador` | Acesso operacional básico |

---

## 3. Como rodar o projeto localmente

### Backend (Django)

Certifique-se de que o ambiente virtual está ativado (`(venv)` no terminal):

```bash
# Ativar venv (caso não esteja ativo)
venv\Scripts\activate

# Aplicar migrations (caso ainda não tenha feito)
python manage.py migrate

# (Opcional) Popular banco com usuários de teste
python seed.py

# Iniciar o servidor de desenvolvimento
python manage.py runserver
```

O backend estará disponível em: **http://localhost:8000**

O painel admin do Django estará em: **http://localhost:8000/admin/**

> Para criar um superusuário para acessar o admin:
> ```bash
> python manage.py createsuperuser
> ```

### Frontend (React + Vite)

Abra um **segundo terminal** no VSCode (`Ctrl+Shift+`` `) e execute:

```bash
cd frontend
npm run dev
```

O frontend estará disponível em: **http://localhost:5173**

### Resumo dos endereços

| Serviço | URL |
|---|---|
| Frontend React | http://localhost:5173 |
| API Django | http://localhost:8000/api/ |
| Admin Django | http://localhost:8000/admin/ |

---

## 4. Como testar os endpoints

Você pode testar os endpoints com qualquer ferramenta de sua preferência. Abaixo estão as instruções para as mais comuns.

### Opção A — REST Client (VSCode)

Instale a extensão **REST Client** no VSCode e crie um arquivo `tests.http` na raiz do projeto:

```http
### Health check
GET http://localhost:8000/api/health/

### Login
POST http://localhost:8000/api/login/
Content-Type: application/json

{
  "email": "admin@sistema.com",
  "senha": "Admin@123"
}

### Registro de novo usuário (requer token de admin)
POST http://localhost:8000/api/registro/
Content-Type: application/json
Authorization: Bearer <COLE_O_TOKEN_AQUI>

{
  "nome": "Novo Fiscal",
  "email": "novo.fiscal@sistema.com",
  "papel": "fiscal",
  "senha": "Fiscal@123",
  "confirmar_senha": "Fiscal@123"
}

### Dados do usuário autenticado
GET http://localhost:8000/api/auth/me/
Authorization: Bearer <COLE_O_TOKEN_AQUI>

### Listar todos os usuários (somente admin)
GET http://localhost:8000/api/usuarios/
Authorization: Bearer <COLE_O_TOKEN_AQUI>

### Detalhe de um usuário específico
GET http://localhost:8000/api/usuarios/1/
Authorization: Bearer <COLE_O_TOKEN_AQUI>

### Editar papel de um usuário
PATCH http://localhost:8000/api/usuarios/1/
Content-Type: application/json
Authorization: Bearer <COLE_O_TOKEN_AQUI>

{
  "papel": "gestor"
}

### Desativar um usuário
PATCH http://localhost:8000/api/usuarios/1/
Content-Type: application/json
Authorization: Bearer <COLE_O_TOKEN_AQUI>

{
  "ativo": false
}

### Deletar um usuário
DELETE http://localhost:8000/api/usuarios/1/
Authorization: Bearer <COLE_O_TOKEN_AQUI>

### Renovar token (refresh)
POST http://localhost:8000/api/auth/refresh/
Content-Type: application/json

{
  "refresh": "<COLE_O_REFRESH_TOKEN_AQUI>"
}
```

Clique em **Send Request** acima de cada bloco para executar.

### Opção B — curl (terminal)

```bash
# Login
curl -X POST http://localhost:8000/api/login/ \
  -H "Content-Type: application/json" \
  -d "{\"email\": \"admin@sistema.com\", \"senha\": \"Admin@123\"}"

# Listar usuários (substitua TOKEN pelo valor recebido no login)
curl http://localhost:8000/api/usuarios/ \
  -H "Authorization: Bearer TOKEN"
```

### Opção C — Postman

1. Baixe e instale o [Postman](https://www.postman.com/downloads/)
2. Crie uma nova **Collection** chamada `Refeição Escolar`
3. Adicione as requisições conforme a tabela abaixo
4. Para endpoints autenticados, vá em **Authorization → Bearer Token** e cole o token obtido no login

### Tabela de endpoints

| Método | Endpoint | Autenticação | Papel mínimo | Descrição |
|---|---|---|---|---|
| GET | `/api/health/` | Não | — | Verificação de saúde da API |
| POST | `/api/login/` | Não | — | Login, retorna tokens JWT |
| POST | `/api/auth/refresh/` | Não | — | Renova o access token |
| GET | `/api/auth/me/` | Sim | Qualquer | Retorna dados do usuário logado |
| POST | `/api/registro/` | Sim | `admin` | Cria novo usuário |
| GET | `/api/usuarios/` | Sim | `admin` | Lista todos os usuários |
| GET | `/api/usuarios/<id>/` | Sim | `admin` | Detalhe de um usuário |
| PATCH | `/api/usuarios/<id>/` | Sim | `admin` | Edita papel ou status |
| DELETE | `/api/usuarios/<id>/` | Sim | `admin` | Remove usuário |

---

## 5. Autenticação — como funciona e como testar

### Como funciona

O sistema utiliza **JWT (JSON Web Token)** para autenticação stateless. O fluxo completo é:

```
1. Cliente envia email + senha para POST /api/login/
2. Backend valida credenciais e verifica se o usuário está ativo
3. Backend registra o último acesso (campo ultimo_acesso)
4. Backend retorna dois tokens:
   - access:  token de curta duração usado nas requisições
   - refresh: token de longa duração usado para renovar o access
5. Cliente inclui o access token no header de cada requisição:
   Authorization: Bearer <access_token>
6. Quando o access token expira, o cliente envia o refresh token para
   POST /api/auth/refresh/ e recebe um novo access token
```

O token JWT contém o payload: `{ "id": ..., "email": "...", "papel": "..." }`, assinado com a `SECRET_KEY` do Django.

### Papéis e controle de acesso

As permissões são verificadas em cada view com base no campo `papel` do usuário:

```
admin   → acesso total (registro, listagem, edição, exclusão de usuários)
gestor  → acesso gerencial (definido nas views específicas)
fiscal  → acesso de fiscalização
empresa → acesso da empresa
operador → acesso básico
```

Qualquer papel autenticado pode acessar `GET /api/auth/me/`.
Apenas `admin` pode acessar `/api/registro/` e `/api/usuarios/`.

### Passo a passo para testar a autenticação

**Passo 1 — Popular o banco com usuários de teste**

```bash
python seed.py
```

Isso cria os seguintes usuários:

| Email | Senha | Papel |
|---|---|---|
| admin@sistema.com | Admin@123 | admin |
| operador@sistema.com | Oper@123 | operador |
| gestor@sistema.com | Gest@123 | gestor |
| empresa@sistema.com | Empr@123 | empresa |
| fiscal@sistema.com | — | fiscal (sem senha — apenas Google) |

**Passo 2 — Fazer login e obter o token**

```bash
curl -X POST http://localhost:8000/api/login/ \
  -H "Content-Type: application/json" \
  -d "{\"email\": \"admin@sistema.com\", \"senha\": \"Admin@123\"}"
```

Resposta esperada:

```json
{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "usuario": {
    "id": 1,
    "email": "admin@sistema.com",
    "papel": "admin"
  }
}
```

**Passo 3 — Usar o token em uma requisição protegida**

```bash
curl http://localhost:8000/api/usuarios/ \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

**Passo 4 — Testar rejeição por papel insuficiente**

Faça login como operador e tente acessar o endpoint de listagem de usuários (apenas admin):

```bash
# Login como operador
curl -X POST http://localhost:8000/api/login/ \
  -H "Content-Type: application/json" \
  -d "{\"email\": \"operador@sistema.com\", \"senha\": \"Oper@123\"}"

# Tente listar usuários com o token do operador
curl http://localhost:8000/api/usuarios/ \
  -H "Authorization: Bearer <TOKEN_DO_OPERADOR>"
```

Resposta esperada: `403 Forbidden`

**Passo 5 — Testar conta inativa**

```bash
# Desative o operador (com token de admin)
curl -X PATCH http://localhost:8000/api/usuarios/2/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <TOKEN_DO_ADMIN>" \
  -d "{\"ativo\": false}"

# Tente fazer login com a conta desativada
curl -X POST http://localhost:8000/api/login/ \
  -H "Content-Type: application/json" \
  -d "{\"email\": \"operador@sistema.com\", \"senha\": \"Oper@123\"}"
```

Resposta esperada: `403 Forbidden`

**Passo 6 — Renovar o token expirado**

```bash
curl -X POST http://localhost:8000/api/auth/refresh/ \
  -H "Content-Type: application/json" \
  -d "{\"refresh\": \"<SEU_REFRESH_TOKEN>\"}"
```

Resposta esperada: novo `access` token.

### Rodando os testes automatizados de autenticação

O projeto inclui uma suite completa de testes em `api/tests/test_auth.py` que cobre todos os cenários descritos acima:

```bash
# Rodar todos os testes
python manage.py test api.tests

# Rodar apenas um conjunto específico
python manage.py test api.tests.test_auth.LoginViewTest
python manage.py test api.tests.test_auth.PermissoesPapelTest
```

Os testes cobrem:

- Criação de usuário e hash de senha
- Login correto e incorreto
- Login com conta inativa
- Atualização do `ultimo_acesso` no login
- Acesso ao endpoint `/me/` com e sem token
- Registro de usuário por admin e por outros papéis
- Validação de senha fraca e e-mail duplicado
- Listagem e detalhe de usuários
- Edição de papel e desativação
- Exclusão de usuário
- Renovação e invalidação de tokens
- Controle de acesso por papel para todos os endpoints protegidos

### Configurar Google OAuth2 (opcional)

Para habilitar o login com Google:

1. Acesse https://console.cloud.google.com/
2. Crie um projeto → **APIs & Services → Credentials → Create Credentials → OAuth 2.0 Client ID**
3. Tipo de aplicação: **Web application**
4. Adicione `http://localhost:8000/api/auth/google/callback/` como URI de redirecionamento autorizado
5. Copie o **Client ID** e o **Client Secret** para o `.env`:

```env
GOOGLE_CLIENT_ID=seu-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=seu-client-secret
GOOGLE_ALLOWED_DOMAINS=suaescola.edu.br
```

> Deixe `GOOGLE_ALLOWED_DOMAINS` vazio em desenvolvimento para aceitar qualquer domínio Google.


# Sistema de Refeição Escolar

## 📌 Frontend

Tecnologias utilizadas:
- React
- Vite
- TailwindCSS
- Axios

## 🚀 Como rodar o projeto

```bash
cd frontend
npm install
npm run dev

🌐 Acesso

http://localhost:5173/