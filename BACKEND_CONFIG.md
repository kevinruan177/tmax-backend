# 🔧 Configuração do Backend TMAX

## 📋 Status do Backend

- **Versão:** 2.0.0
- **Framework:** FastAPI
- **Banco de Dados:** SQLAlchemy (compatible com PostgreSQL, SQLite, etc)
- **Autenticação:** JWT (JSON Web Token)
- **Deploy:** Render (https://tmax-backend.onrender.com)

---

## 🗂️ Estrutura do Projeto

```
tmax-backend/
├── main.py                 # Arquivo principal da aplicação
├── requirements.txt        # Dependências Python
├── .env.example           # Template de variáveis de ambiente
│
├── app/
│   ├── __init__.py
│   ├── auth.py            # Lógica de autenticação JWT
│   │
│   ├── config/
│   │   ├── __init__.py
│   │   └── database.py    # Configuração do banco de dados
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── usuario.py     # Model de Usuário
│   │   ├── driver.py      # Model de Driver
│   │   └── schemas.py     # Schemas Pydantic para validação
│   │
│   ├── controllers/
│   │   ├── __init__.py
│   │   ├── driver_controller.py    # Lógica de negócio para Driver
│   │   └── usuario_controller.py   # Lógica de negócio para Usuário
│   │
│   └── routes/
│       ├── __init__.py
│       ├── auth_routes.py          # Endpoints de autenticação
│       ├── driver_routes.py        # Endpoints de driver
│       └── usuario_routes.py       # Endpoints de usuário
```

---

## 🔐 Configuração de Variáveis de Ambiente

Criar arquivo `.env` na raiz do projeto com base em `.env.example`:

```bash
# Tipo de ambiente
ENVIRONMENT=production

# Banco de dados
DATABASE_URL=postgresql://usuario:senha@localhost:5432/tmax_db

# JWT
SECRET_KEY=sua-chave-secreta-super-segura-aqui-mude-em-producao
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000,https://tmax-frontend.vercel.app

# API
API_TITLE=TMAX API
API_VERSION=2.0.0
API_DESCRIPTION=API de gerenciamento de usuários e drivers TMAX
```

### ⚠️ Importante para Produção

1. **SECRET_KEY:** Deve ser uma string aleatória forte. Gerar com:
   ```python
   import secrets
   print(secrets.token_urlsafe(32))
   ```

2. **DATABASE_URL:** Usar banco PostgreSQL em produção (não SQLite)

3. **ALLOWED_ORIGINS:** Adicionar URLs dos frontends em produção

---

## 🏃 Rodando o Backend Localmente

### Requisitos
- Python 3.9+
- pip ou conda

### Passos

1. **Criar ambiente virtual:**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   source venv/bin/activate  # macOS/Linux
   ```

2. **Instalar dependências:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Criar arquivo .env:**
   ```bash
   cp .env.example .env
   # Editar .env com suas configurações
   ```

4. **Rodar o servidor:**
   ```bash
   uvicorn main:app --reload
   ```

5. **Acessar:**
   - API: http://localhost:8000
   - Docs (Swagger): http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

---

## 📡 Endpoints Principais

### Health & Info
```
GET /health              # Verificar se API está online
GET /                    # Informações da API
```

### Autenticação
```
POST /auth/register      # Registrar novo driver
POST /auth/login         # Login do driver
```

### Driver
```
GET /driver/me           # Obter dados do driver logado
GET /driver/{id}         # Obter dados de um driver
PUT /driver/{id}         # Atualizar dados do driver
POST /driver/upload/profile  # Upload de foto de perfil
POST /driver/upload/rg   # Upload de RG
```

### Motorcycle
```
POST /driver/vehicle     # Registrar moto
GET /driver/vehicle/{id} # Obter dados da moto
PUT /driver/vehicle/{id} # Atualizar dados da moto
```

---

## 🔒 Autenticação JWT

### Fluxo

1. **Usuário faz login:**
   ```
   POST /auth/login
   Body: { "email": "...", "password": "..." }
   Response: { "access_token": "...", "token_type": "bearer" }
   ```

2. **Cliente armazena token** em localStorage

3. **Cliente envia token** em todas as requisições protegidas:
   ```
   Authorization: Bearer {access_token}
   ```

4. **Backend valida** o token e retorna os dados

### Tokens

- **Tipo:** JWT (HS256)
- **Expiração:** 30 minutos (configurável)
- **Claims:** email do driver

---

## 🗄️ Banco de Dados

### Models Disponíveis

1. **Usuario**
   - id
   - nome
   - email
   - cpf
   - phone
   - password (hash bcrypt)
   - profile_photo
   - created_at
   - updated_at

2. **Driver** (extensão de Usuario)
   - Herda campos de Usuario
   - Relacionado a Motorcycle

3. **Motorcycle**
   - id
   - driver_id (FK)
   - model
   - year
   - color
   - plate
   - vehicle_photo
   - created_at
   - updated_at

### Criação de Tabelas

Tabelas são criadas automaticamente ao iniciar a aplicação (em `main.py`):

```python
Usuario.metadata.create_all(bind=engine)
Driver.metadata.create_all(bind=engine)
Motorcycle.metadata.create_all(bind=engine)
```

---

## 🔧 Deployment em Render

### Já Configurado

- Arquivo `Procfile` pronto para Render
- `runtime.txt` especifica versão do Python
- Variáveis de ambiente configuradas no dashboard Render

### URL de Acesso

- **Produção:** https://tmax-backend.onrender.com
- **Documentação:** https://tmax-backend.onrender.com/docs

### Redeploy

```bash
# Fazer push para GitHub e Render fará deploy automático
git push origin main
```

---

## 🐛 Troubleshooting

### Erro: Database Connection Error
```
Verificar DATABASE_URL em .env
Garantir que banco PostgreSQL está rodando
```

### Erro: Module not found
```
pip install -r requirements.txt
Verificar se venv está ativado
```

### Erro: CORS Error
```
Verificar ALLOWED_ORIGINS em .env
Adicionar domínio do frontend na lista
Fazer redeploy do backend
```

### Erro: 401 Unauthorized
```
Token JWT inválido ou expirado
Fazer novo login para obter novo token
Verificar se header Authorization está correto
```

---

## 📊 Monitoramento

### Logs no Render
- Dashboard: https://dashboard.render.com
- Ver logs em tempo real para debug

### Health Check
```bash
curl https://tmax-backend.onrender.com/health
# Response: {"status": "ok", "version": "2.0.0"}
```

---

## 🚀 Próximos Passos

1. [ ] Adicionar autenticação com email (confirmação de email)
2. [ ] Implementar sistema de ratings/avaliações
3. [ ] Adicionar sistema de notificações
4. [ ] Implementar pagamentos
5. [ ] Adicionar testes automatizados
6. [ ] Documentar webhooks

---

## 📚 Dependências

```
fastapi==0.109.0          # Framework web
uvicorn==0.27.0           # Servidor ASGI
sqlalchemy==2.0.28        # ORM
pydantic==2.7.0           # Validação de dados
passlib[bcrypt]==1.7.4    # Hash de senhas
python-jose==3.3.0        # JWT
python-multipart==0.0.6   # Upload de arquivos
pillow==11.0.0            # Processamento de imagens
requests==2.32.0          # HTTP client
bcrypt==4.1.2             # Criptografia de senhas
```

---

**Última atualização:** 4 de Dezembro de 2024  
**Versão:** 2.0.0
