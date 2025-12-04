from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from app.config.database import get_db
from app.models.schemas import (
    DriverCreate, DriverUpdate, Driver as DriverSchema,
    DriverLogin, DriverRegisterRequest, Token
)
from app.controllers import DriverController
from app.auth import criar_access_token, ACCESS_TOKEN_EXPIRE_MINUTES, verificar_token

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=DriverSchema)
def registrar_driver(driver_data: DriverRegisterRequest, db: Session = Depends(get_db)):
    """Registrar um novo driver (motorista)"""
    
    # Validar senhas
    if driver_data.password != driver_data.confirm_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="As senhas não coincidem"
        )
    
    # Verificar se email já existe
    db_driver_email = DriverController.buscar_driver_por_email(db, email=driver_data.email)
    if db_driver_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email já registrado"
        )
    
    # Verificar se CPF já existe
    db_driver_cpf = DriverController.buscar_driver_por_cpf(db, cpf=driver_data.cpf)
    if db_driver_cpf:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="CPF já registrado"
        )
    
    # Criar driver
    driver_create = DriverCreate(
        nome=driver_data.name,
        email=driver_data.email,
        cpf=driver_data.cpf,
        phone=driver_data.phone,
        password=driver_data.password
    )
    
    return DriverController.criar_driver(db=db, driver=driver_create)


@router.post("/login", response_model=Token)
def login_driver(credentials: DriverLogin, db: Session = Depends(get_db)):
    """Fazer login do driver"""
    
    # Buscar driver por email
    driver = DriverController.buscar_driver_por_email(db, email=credentials.email)
    if not driver:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Verificar senha
    if not DriverController.verificar_senha(credentials.password, driver.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Criar token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = criar_access_token(
        data={"sub": driver.email}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}
