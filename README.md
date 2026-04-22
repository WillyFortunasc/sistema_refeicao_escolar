# 🍽️ Sistema de Refeição Escolar

Sistema de gestão de refeições escolares com autenticação via JWT e Google OAuth2, desenvolvido com Django REST Framework no backend e React + Vite no frontend.

---
## 1. Backend

### 📋 Índice

1. [Configuração do ambiente no Windows com VSCode](#1-configuração-do-ambiente-no-windows-com-vscode)
2. [Estrutura do projeto e bibliotecas utilizadas](#2-estrutura-do-projeto-e-bibliotecas-utilizadas)
3. [Como rodar o projeto localmente](#3-como-rodar-o-projeto-localmente)
4. [Como testar os endpoints](#4-como-testar-os-endpoints)
5. [Autenticação — como funciona e como testar](#5-autenticação--como-funciona-e-como-testar)
6. [CRUD de Estudantes](#6-crud-de-estudantes)

---

### 1. Configuração do ambiente no Windows com VSCode

#### Pré-requisitos

Instale as ferramentas abaixo antes de começar:

| Ferramenta | Link | Versão recomendada |
|---|---|---|
| Python | https://www.python.org/downloads/ | 3.11 ou superior |
| Node.js | https://nodejs.org/ | 18 LTS ou superior |
| Git | https://git-scm.com/download/win | Última versão |
| VSCode | https://code.visualstudio.com/ | Última versão |

> **Atenção durante a instalação do Python:** marque a opção **"Add Python to PATH"** na primeira tela do instalador.

#### Extensões recomendadas do VSCode

Abra o VSCode, vá em **Extensions** (`Ctrl+Shift+X`) e instale:

- `Python` (Microsoft)
- `Pylance` (Microsoft)
- `ES7+ React/Redux/React-Native snippets`
- `Tailwind CSS IntelliSense`
- `Thunder Client` (para testar endpoints diretamente no editor)
- `GitLens`

#### Clonar o repositório

Abra o terminal integrado do VSCode (`Ctrl+`` `):

```bash
git clone <URL_DO_REPOSITORIO>
cd sistema-refeicao-escolar
```

#### Configurar o ambiente virtual Python

```bash
# Criar o ambiente virtual
python -m venv venv

# Ativar o ambiente virtual (Windows)
venv\Scripts\activate

# Confirmar que está ativo — o terminal deve exibir (venv) no início
```

> Se o PowerShell bloquear a execução de scripts, execute primeiro:
> `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

#### Instalar dependências Python

```bash
pip install -r requirements.txt
```

#### Configurar as variáveis de ambiente

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

#### Configurar o banco de dados

```bash
python manage.py migrate
```

O ambiente está configurado. Prossiga para a seção 3 para rodar o projeto.

---

### 2. Estrutura do projeto e bibliotecas utilizadas

#### Estrutura de diretórios

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

#### Backend — bibliotecas Python

| Biblioteca | Versão | Finalidade |
|---|---|---|
| **Django** | 6.0.3 | Framework web principal — ORM, autenticação, admin, migrations |
| **djangorestframework** | 3.17.0 | Construção da API REST — views, serializers, permissions, autenticação JWT |
| **django-cors-headers** | 4.9.0 | Permite requisições cross-origin do frontend React (`localhost:5173`) |
| **python-dotenv** | 1.2.2 | Leitura das variáveis de ambiente do arquivo `.env` |
| **psycopg2-binary** | 2.9.11 | Driver PostgreSQL (usado apenas em produção; em dev usa SQLite) |
| **PyJWT** | — | Geração e validação de tokens JWT para autenticação stateless |


#### Modelo de usuário e papéis

O sistema utiliza um modelo `Usuario` customizado (substituindo o `User` padrão do Django) com os seguintes papéis:

| Papel | Descrição |
|---|---|
| `admin` | Acesso total — pode criar, listar, editar e deletar usuários |
| `gestor` | Acesso gerencial |
| `fiscal` | Acesso de fiscalização |
| `empresa` | Acesso da empresa fornecedora |
| `operador` | Acesso operacional básico |

---

### 3. Como rodar o projeto localmente

#### Backend (Django)

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

### Resumo dos endereços

| Serviço | URL |
|---|---|
| API Django | http://localhost:8000/api/ |
| Admin Django | http://localhost:8000/admin/ |

---

### 4. Como testar os endpoints

Você pode testar os endpoints com qualquer ferramenta de sua preferência. Abaixo estão as instruções para as mais comuns.

#### Opção A — Thunder Client (VSCode)

O **Thunder Client** é uma extensão leve do VSCode para testar APIs REST, sem precisar sair do editor.

**Instalação**

1. Abra o VSCode e vá em **Extensions** (`Ctrl+Shift+X`)
2. Pesquise por `Thunder Client`
3. Clique em **Install** na extensão de autoria de *Ranga Vadhineni*
4. Após instalar, um ícone de raio (⚡) aparecerá na barra lateral esquerda

**Como fazer uma requisição**

1. Clique no ícone ⚡ na barra lateral para abrir o Thunder Client
2. Clique em **New Request** no topo do painel
3. Escolha o método HTTP (`GET`, `POST`, `PATCH`, `DELETE`) no seletor à esquerda da URL
4. Digite a URL desejada (ex: `http://localhost:8000/api/health/`)
5. Clique em **Send**

**Configurando headers e body**

- Para enviar JSON no corpo da requisição: clique na aba **Body** → selecione **JSON** → insira o payload
- Para enviar o token JWT: clique na aba **Headers** → adicione o header:
  - Nome: `Authorization`
  - Valor: `Bearer <SEU_TOKEN_AQUI>`

**Exemplos de requisições**

Abaixo estão as requisições para testar os principais endpoints do sistema:

---

🔵 **Health check**
- Método: `GET`
- URL: `http://localhost:8000/api/health/`

---

🔵 **Login**
- Método: `POST`
- URL: `http://localhost:8000/api/login/`
- Aba **Headers**: `Content-Type: application/json`
- Aba **Body** (JSON):
```json
{
  "email": "admin@sistema.com",
  "senha": "Admin@123"
}
```

---

🔵 **Registro de novo usuário** *(requer token de admin)*
- Método: `POST`
- URL: `http://localhost:8000/api/registro/`
- Aba **Headers**:
  - `Content-Type: application/json`
  - `Authorization: Bearer <COLE_O_TOKEN_AQUI>`
- Aba **Body** (JSON):
```json
{
  "nome": "Novo Fiscal",
  "email": "novo.fiscal@sistema.com",
  "papel": "fiscal",
  "senha": "Fiscal@123",
  "confirmar_senha": "Fiscal@123"
}
```

---

🔵 **Dados do usuário autenticado**
- Método: `GET`
- URL: `http://localhost:8000/api/auth/me/`
- Aba **Headers**: `Authorization: Bearer <COLE_O_TOKEN_AQUI>`

---

🔵 **Listar todos os usuários** *(somente admin)*
- Método: `GET`
- URL: `http://localhost:8000/api/usuarios/`
- Aba **Headers**: `Authorization: Bearer <COLE_O_TOKEN_AQUI>`

---

🔵 **Detalhe de um usuário específico**
- Método: `GET`
- URL: `http://localhost:8000/api/usuarios/1/`
- Aba **Headers**: `Authorization: Bearer <COLE_O_TOKEN_AQUI>`

---

🔵 **Editar papel de um usuário**
- Método: `PATCH`
- URL: `http://localhost:8000/api/usuarios/1/`
- Aba **Headers**:
  - `Content-Type: application/json`
  - `Authorization: Bearer <COLE_O_TOKEN_AQUI>`
- Aba **Body** (JSON):
```json
{
  "papel": "gestor"
}
```

---

🔵 **Desativar um usuário**
- Método: `PATCH`
- URL: `http://localhost:8000/api/usuarios/1/`
- Aba **Headers**:
  - `Content-Type: application/json`
  - `Authorization: Bearer <COLE_O_TOKEN_AQUI>`
- Aba **Body** (JSON):
```json
{
  "ativo": false
}
```

---

🔵 **Deletar um usuário**
- Método: `DELETE`
- URL: `http://localhost:8000/api/usuarios/1/`
- Aba **Headers**: `Authorization: Bearer <COLE_O_TOKEN_AQUI>`

---

🔵 **Renovar token (refresh)**
- Método: `POST`
- URL: `http://localhost:8000/api/auth/refresh/`
- Aba **Headers**: `Content-Type: application/json`
- Aba **Body** (JSON):
```json
{
  "refresh": "<COLE_O_REFRESH_TOKEN_AQUI>"
}
```

---

> 💡 **Dica — Salvar requisições em coleções:** No Thunder Client, clique em **Collections** → **New Collection** para criar uma coleção chamada, por exemplo, `Sistema Refeição Escolar`. Salve cada requisição na coleção clicando em **Save** após criá-la. Isso permite reutilizá-las facilmente sem precisar redigitar URLs e headers toda vez.

> 💡 **Dica — Variáveis de ambiente:** Acesse **Env** no painel lateral → **New Environment** → crie uma variável `base_url` com valor `http://localhost:8000` e uma variável `token` onde você cola o JWT após o login. Nas requisições, use `{{base_url}}/api/login/` e `Bearer {{token}}` para não precisar repetir os valores manualmente.


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

### 5. Autenticação — como funciona e como testar

#### Como funciona

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

#### Papéis e controle de acesso

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

#### Passo a passo para testar a autenticação

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

**Passo 2 — Fazer login e obter o token (Thunder Client)**

1. Clique em **New Request**
2. Configure:
   - **Método:** `POST`
   - **URL:** `http://localhost:8000/api/login/`
   - **Aba Headers:** `Content-Type: application/json`
   - **Aba Body** → JSON:

```json
{
  "email": "admin@sistema.com",
  "senha": "Admin@123"
}
```

3. Clique **Send**

**Resposta esperada (200 OK):**

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

> 💡 **Dica:** Copie o valor de `access` — você usará isso nas próximas requisições no header `Authorization: Bearer <TOKEN>`

**Passo 3 — Usar o token em uma requisição protegida (Thunder Client)**

1. Clique em **New Request**
2. Configure:
   - **Método:** `GET`
   - **URL:** `http://localhost:8000/api/usuarios/`
   - **Aba Headers:**
     - `Authorization: Bearer <COLE_O_TOKEN_ACCESS_AQUI>`

3. Clique **Send**

**Resposta esperada (200 OK):** Lista de todos os usuários

**Passo 4 — Testar rejeição por papel insuficiente (Thunder Client)**

Faça login como operador e tente acessar listagem de usuários (apenas admin):

**4a. Login como operador:**

1. Nova requisição POST
2. URL: `http://localhost:8000/api/login/`
3. Body (JSON):
```json
{
  "email": "operador@sistema.com",
  "senha": "Oper@123"
}
```
4. Copie o `access` token

**4b. Tente acessar listagem com token de operador:**

1. Nova requisição GET
2. URL: `http://localhost:8000/api/usuarios/`
3. Header: `Authorization: Bearer <TOKEN_DO_OPERADOR>`
4. Clique **Send**

**Resposta esperada: `403 Forbidden`**

```json
{
  "detail": "Você não tem permissão para acessar esse recurso."
}
```

**Passo 5 — Testar conta inativa (Thunder Client)**

**5a. Desativar o operador (com token de admin):**

1. Nova requisição PATCH
2. URL: `http://localhost:8000/api/usuarios/2/`
3. Headers:
   - `Content-Type: application/json`
   - `Authorization: Bearer <TOKEN_DO_ADMIN>`
4. Body (JSON):
```json
{
  "ativo": false
}
```
5. Clique **Send**

**5b. Tente fazer login com a conta desativada:**

1. Nova requisição POST
2. URL: `http://localhost:8000/api/login/`
3. Body (JSON):
```json
{
  "email": "operador@sistema.com",
  "senha": "Oper@123"
}
```
4. Clique **Send**

**Resposta esperada: `401 Unauthorized`**

```json
{
  "detail": "Usuário inativo ou credenciais inválidas."
}
```

**Passo 6 — Renovar o token expirado (Thunder Client)**

Quando o `access` token expirar, use o `refresh` token para obter um novo:

1. Nova requisição POST
2. URL: `http://localhost:8000/api/auth/refresh/`
3. Headers: `Content-Type: application/json`
4. Body (JSON):
```json
{
  "refresh": "<COLE_O_REFRESH_TOKEN_AQUI>"
}
```
5. Clique **Send**

**Resposta esperada (200 OK):**

```json
{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

> ✅ Use o novo `access` token nas próximas requisições

#### Testando com Django Shell (alternativa ao Thunder Client)

Se preferir testar a autenticação via Django Shell (console Python), execute:

```bash
python manage.py shell
```

Então dentro do shell:

```python
from api.models import Usuario
from django.contrib.auth import authenticate

# Criar um usuário de teste
user = Usuario.objects.create_user(
    email='teste@sistema.com',
    nome='Usuário Teste',
    senha='Teste@123',
    papel='admin'
)

# Fazer login (simular POST /api/login/)
user = authenticate(email='teste@sistema.com', password='Teste@123')
print(f"Usuário autenticado: {user.email}")
print(f"Papel: {user.papel}")
print(f"Ativo: {user.ativo}")

# Listar todos os usuários
todos = Usuario.objects.all()
for u in todos:
    print(f"{u.email} ({u.papel}) - Ativo: {u.ativo}")

# Desativar um usuário
user.ativo = False
user.save()
print(f"Usuário desativado: {user.email}")

# Tentar login com usuário inativo
user_inativo = authenticate(email='teste@sistema.com', password='Teste@123')
print(f"Resultado do login com inativo: {user_inativo}")  # Será None

# Sair do shell
exit()
```

#### Rodando os testes automatizados de autenticação

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

#### Configurar Google OAuth2 (opcional)

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


### 6. CRUD de Estudantes

O sistema inclui um módulo completo para gerenciar estudantes com as seguintes funcionalidades:

✅ **Criar** novo estudante com foto (obrigatória)  
✅ **Listar** todos os estudantes com filtros por ativo, curso e turma  
✅ **Visualizar** detalhe completo de um estudante  
✅ **Editar** dados do estudante (nome, curso, turma, foto)  
✅ **Desativar** estudante (soft-delete — não deleta fisicamente)  
✅ **Gerenciar** impressões digitais (até 3 dedos por aluno)  

**📖 Leia a documentação completa em:** [`ESTUDANTE.md`](./ESTUDANTE.md)

A documentação inclui:
- Visão geral do módulo de estudantes
- Tabela de todos os endpoints disponíveis
- Exemplos de requisições com **Thunder Client** (interface visual, não curl)
- Estrutura de campos e validações
- Troubleshooting de erros comuns
- Casos de uso reais

---

## 2. Frontend

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
```

🌐 Acesso

http://localhost:5173/
