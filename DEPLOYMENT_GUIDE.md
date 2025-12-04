# 🚀 Deployment Guide - TMAX Backend

## Produção vs Desenvolvimento

### 🔧 Desenvolvimento (Atual)
```bash
uvicorn main:app --reload
```
- ✅ Hot reload ativo
- ✅ Debug mode ativo
- ✅ Logs detalhados
- ❌ Não é seguro para produção

### 🏢 Produção (Recomendado)
```bash
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:8000
```
- ✅ Multiple workers
- ✅ Production grade
- ✅ Melhor performance

---

## 1️⃣ Configuração Pré-Deployment

### 1.1 Variáveis de Ambiente

Criar arquivo `.env` na raiz do projeto:

```bash
# app/auth.py - MUDE ISSO!
SECRET_KEY=sua-chave-super-secreta-aleatorias-e-longa

# app/config/database.py
DATABASE_URL=postgresql://user:password@localhost/tmax_db

# main.py
DEBUG=false
ENVIRONMENT=production

# CORS
ALLOWED_ORIGINS=https://seu-dominio.com,https://www.seu-dominio.com

# Email
SMTP_SERVER=smtp.seuservidor.com
SMTP_PORT=587
SMTP_USER=seu-email@empresa.com
SMTP_PASSWORD=sua-senha-segura
```

### 1.2 Usar Variáveis de Ambiente

Atualizar `app/auth.py`:
```python
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "default-insecure-key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
```

Atualizar `app/config/database.py`:
```python
import os

SQLALCHEMY_DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "sqlite:///./tmax.db"
)

if "postgresql" in SQLALCHEMY_DATABASE_URL:
    # PostgreSQL
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
else:
    # SQLite
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, 
        connect_args={"check_same_thread": False}
    )
```

Atualizar `main.py`:
```python
import os
from fastapi.middleware.cors import CORSMiddleware

DEBUG = os.getenv("DEBUG", "true").lower() == "true"
ALLOWED_ORIGINS = os.getenv(
    "ALLOWED_ORIGINS", 
    "*"
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS if not DEBUG else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 1.3 Instalar Dependências de Produção

```bash
pip install gunicorn python-dotenv psycopg2-binary
```

---

## 2️⃣ Deploy em Servidor Linux (Ubuntu)

### 2.1 Preparar Servidor
```bash
# Atualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar Python e pip
sudo apt install python3.11 python3.11-venv python3-pip -y

# Instalar PostgreSQL (opcional)
sudo apt install postgresql postgresql-contrib -y

# Instalar Nginx (proxy reverso)
sudo apt install nginx -y
```

### 2.2 Clonar Projeto
```bash
cd /var/www
sudo git clone https://github.com/seu-repo/tmax-backend.git
sudo chown -R $USER:$USER tmax-backend
cd tmax-backend
```

### 2.3 Criar Virtual Environment
```bash
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2.4 Configurar Banco de Dados (PostgreSQL)
```bash
# Como root do PostgreSQL
sudo -u postgres psql

# Dentro do psql
CREATE DATABASE tmax_db;
CREATE USER tmax_user WITH PASSWORD 'senha-segura-aqui';
ALTER ROLE tmax_user SET client_encoding TO 'utf8';
ALTER ROLE tmax_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE tmax_user SET default_transaction_deferrable TO on;
ALTER ROLE tmax_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE tmax_db TO tmax_user;
\q
```

### 2.5 Criar Arquivo `.env`
```bash
nano .env
```

Adicionar:
```
SECRET_KEY=seu-super-secreto-aleatorio-key-aqui-com-muitos-caracteres
DATABASE_URL=postgresql://tmax_user:senha-segura-aqui@localhost/tmax_db
DEBUG=false
ENVIRONMENT=production
ALLOWED_ORIGINS=https://seu-dominio.com,https://www.seu-dominio.com
```

### 2.6 Configurar Systemd Service

Criar arquivo `/etc/systemd/system/tmax-backend.service`:
```bash
sudo nano /etc/systemd/system/tmax-backend.service
```

Adicionar:
```ini
[Unit]
Description=TMAX Backend API
After=network.target

[Service]
User=seu-usuario
WorkingDirectory=/var/www/tmax-backend
Environment="PATH=/var/www/tmax-backend/venv/bin"
ExecStart=/var/www/tmax-backend/venv/bin/gunicorn \
    -w 4 \
    -k uvicorn.workers.UvicornWorker \
    --bind 127.0.0.1:8000 \
    main:app

Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

### 2.7 Iniciar Serviço
```bash
sudo systemctl daemon-reload
sudo systemctl enable tmax-backend
sudo systemctl start tmax-backend
sudo systemctl status tmax-backend
```

### 2.8 Configurar Nginx (Reverse Proxy)

Criar arquivo `/etc/nginx/sites-available/tmax-backend`:
```bash
sudo nano /etc/nginx/sites-available/tmax-backend
```

Adicionar:
```nginx
server {
    listen 80;
    server_name seu-dominio.com;

    # Redirect HTTP para HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name seu-dominio.com;

    ssl_certificate /etc/letsencrypt/live/seu-dominio.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/seu-dominio.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /docs {
        proxy_pass http://127.0.0.1:8000/docs;
    }

    location /redoc {
        proxy_pass http://127.0.0.1:8000/redoc;
    }
}
```

### 2.9 Ativar Nginx
```bash
sudo ln -s /etc/nginx/sites-available/tmax-backend /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 2.10 Instalar SSL (Let's Encrypt)
```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot certonly --nginx -d seu-dominio.com -d www.seu-dominio.com
```

---

## 3️⃣ Deploy em Heroku

### 3.1 Instalar Heroku CLI
```bash
curl https://cli-assets.heroku.com/install.sh | sh
heroku login
```

### 3.2 Criar Procfile
```bash
echo "web: gunicorn -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT main:app" > Procfile
```

### 3.3 Criar App Heroku
```bash
heroku create tmax-backend
```

### 3.4 Configurar Variáveis de Ambiente
```bash
heroku config:set SECRET_KEY="sua-chave-super-secreta-aqui"
heroku config:set DATABASE_URL="postgresql://..."
heroku config:set DEBUG="false"
```

### 3.5 Deploy
```bash
git push heroku main
```

---

## 4️⃣ Deploy em Docker

### 4.1 Criar Dockerfile
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000", "main:app"]
```

### 4.2 Criar docker-compose.yml
```yaml
version: '3.8'

services:
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: tmax_db
      POSTGRES_USER: tmax_user
      POSTGRES_PASSWORD: senha-segura
    volumes:
      - postgres_data:/var/lib/postgresql/data

  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql://tmax_user:senha-segura@db:5432/tmax_db
      SECRET_KEY: sua-chave-super-secreta
    depends_on:
      - db

volumes:
  postgres_data:
```

### 4.3 Build e Run
```bash
docker-compose build
docker-compose up
```

---

## 5️⃣ Monitoramento e Logs

### 5.1 Ver Logs do Systemd
```bash
sudo journalctl -u tmax-backend -f
```

### 5.2 Ver Status
```bash
sudo systemctl status tmax-backend
```

### 5.3 Integrar com Sentry (Error Tracking)

```bash
pip install sentry-sdk
```

No `main.py`:
```python
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration

sentry_sdk.init(
    dsn="https://seu-sentry-dsn@sentry.io/12345",
    integrations=[FastApiIntegration()],
    traces_sample_rate=1.0
)
```

---

## 6️⃣ Checklist de Deploy

- [ ] `.env` configurado com variáveis seguras
- [ ] `SECRET_KEY` alterado
- [ ] Banco de dados PostgreSQL criado
- [ ] ALLOWED_ORIGINS configurado
- [ ] SSL/HTTPS configurado
- [ ] Nginx proxy reverso configurado
- [ ] Systemd service criado
- [ ] Logs configurados
- [ ] Backups automatizados
- [ ] Monitoramento ativo
- [ ] Health checks funcionando
- [ ] Documentação da API acessível

---

## 7️⃣ Troubleshooting

### Erro 502 Bad Gateway
- Verificar se backend está rodando: `sudo systemctl status tmax-backend`
- Ver logs: `sudo journalctl -u tmax-backend -f`

### Erro de Database
- Verificar conexão: `psql postgresql://user:pass@localhost/tmax_db`
- Criar tabelas: Elas são criadas automaticamente na primeira execução

### Erro de CORS
- Atualizar `ALLOWED_ORIGINS` no `.env`
- Reiniciar backend: `sudo systemctl restart tmax-backend`

### Erro de SSL
- Renovar certificado: `sudo certbot renew`
- Ver status: `sudo certbot certificates`

---

## 📚 Referências

- [FastAPI Production](https://fastapi.tiangolo.com/deployment/)
- [Gunicorn](https://gunicorn.org/)
- [Nginx](https://nginx.org/)
- [PostgreSQL](https://www.postgresql.org/)
- [Docker](https://www.docker.com/)
- [Heroku](https://www.heroku.com/)

---

**Deployment com sucesso! 🎉**
