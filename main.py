from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config.database import engine
from app.models import Usuario, Driver, Motorcycle
from app.routes import usuario_router, auth_router, driver_router
import os

# Criar tabelas no banco
Usuario.metadata.create_all(bind=engine)
Driver.metadata.create_all(bind=engine)
Motorcycle.metadata.create_all(bind=engine)

app = FastAPI(
    title="TMAX API",
    description="API de gerenciamento de usuários e drivers TMAX",
    version="2.0.0"
)

# Configurar CORS - permitir múltiplas origens
allowed_origins = [
    "http://localhost:5173",  # Desenvolvimento local com Vite
    "http://localhost:3000",  # Desenvolvimento local alternativo
    "http://127.0.0.1:5173",
    "http://127.0.0.1:3000",
    "https://tmax-frontend.vercel.app",  # Frontend em produção (quando estiver em deploy)
    "https://tmax.onrender.com",  # Frontend em Render (quando estiver em deploy)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins if os.getenv("ENVIRONMENT") == "production" else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=3600,
)

# Incluir rotas
app.include_router(usuario_router)
app.include_router(auth_router)
app.include_router(driver_router)

@app.get("/", tags=["root"])
def read_root():
    """Raiz da API"""
    return {
        "mensagem": "Bem-vindo à TMAX API v2.0",
        "versao": "2.0.0",
        "endpoints": {
            "usuarios": "/usuarios/",
            "auth": "/auth/",
            "driver": "/driver/",
            "docs": "/docs"
        }
    }

@app.get("/health", tags=["health"])
def health_check():
    """Verificar se a API está rodando"""
    return {"status": "ok", "version": "2.0.0"}
