from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.models.schemas import (
    UsuarioCreate, UsuarioUpdate, Usuario as UsuarioSchema
)
from app.controllers.usuario_controller import UsuarioController

router = APIRouter(prefix="/usuarios", tags=["usuarios"])


@router.post("/", response_model=UsuarioSchema)
def criar_usuario(usuario_data: UsuarioCreate, db: Session = Depends(get_db)):
    """Criar um novo usuário"""
    
    # Verificar se email já existe
    db_usuario = UsuarioController.obter_usuario_por_email(db, email=usuario_data.email)
    if db_usuario:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email já registrado"
        )
    
    return UsuarioController.criar_usuario(db, usuario_data)


@router.get("/{usuario_id}", response_model=UsuarioSchema)
def obter_usuario(usuario_id: int, db: Session = Depends(get_db)):
    """Obter um usuário por ID"""
    db_usuario = UsuarioController.obter_usuario_por_id(db, usuario_id)
    
    if not db_usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )
    
    return db_usuario


@router.get("/", response_model=list[UsuarioSchema])
def listar_usuarios(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """Listar todos os usuários com paginação"""
    return UsuarioController.listar_usuarios(db, skip=skip, limit=limit)


@router.put("/{usuario_id}", response_model=UsuarioSchema)
def atualizar_usuario(usuario_id: int, usuario_data: UsuarioUpdate, db: Session = Depends(get_db)):
    """Atualizar um usuário"""
    db_usuario = UsuarioController.atualizar_usuario(db, usuario_id, usuario_data)
    
    if not db_usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )
    
    return db_usuario


@router.delete("/{usuario_id}")
def deletar_usuario(usuario_id: int, db: Session = Depends(get_db)):
    """Deletar um usuário"""
    success = UsuarioController.deletar_usuario(db, usuario_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )
    
    return {"message": "Usuário deletado com sucesso"}
