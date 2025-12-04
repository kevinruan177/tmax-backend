from sqlalchemy.orm import Session
from app.models.usuario import Usuario
from app.models.schemas import UsuarioCreate, UsuarioUpdate
from passlib.context import CryptContext

# Configurar hash de senha
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UsuarioController:
    """Controlador para operações relacionadas a usuários"""
    
    @staticmethod
    def criar_usuario(db: Session, usuario_data: UsuarioCreate) -> Usuario:
        """Criar um novo usuário"""
        # Hash da senha
        hashed_password = pwd_context.hash(usuario_data.senha)
        
        db_usuario = Usuario(
            nome=usuario_data.nome,
            email=usuario_data.email,
            senha=hashed_password
        )
        
        db.add(db_usuario)
        db.commit()
        db.refresh(db_usuario)
        return db_usuario
    
    @staticmethod
    def obter_usuario_por_id(db: Session, usuario_id: int) -> Usuario | None:
        """Obter usuário por ID"""
        return db.query(Usuario).filter(Usuario.id == usuario_id).first()
    
    @staticmethod
    def obter_usuario_por_email(db: Session, email: str) -> Usuario | None:
        """Obter usuário por email"""
        return db.query(Usuario).filter(Usuario.email == email).first()
    
    @staticmethod
    def listar_usuarios(db: Session, skip: int = 0, limit: int = 10) -> list[Usuario]:
        """Listar todos os usuários com paginação"""
        return db.query(Usuario).offset(skip).limit(limit).all()
    
    @staticmethod
    def atualizar_usuario(db: Session, usuario_id: int, usuario_data: UsuarioUpdate) -> Usuario | None:
        """Atualizar um usuário"""
        db_usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
        
        if not db_usuario:
            return None
        
        if usuario_data.nome:
            db_usuario.nome = usuario_data.nome
        if usuario_data.email:
            db_usuario.email = usuario_data.email
        if usuario_data.senha:
            db_usuario.senha = pwd_context.hash(usuario_data.senha)
        
        db.commit()
        db.refresh(db_usuario)
        return db_usuario
    
    @staticmethod
    def deletar_usuario(db: Session, usuario_id: int) -> bool:
        """Deletar um usuário"""
        db_usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
        
        if not db_usuario:
            return False
        
        db.delete(db_usuario)
        db.commit()
        return True
    
    @staticmethod
    def verificar_senha(senha: str, hashed_password: str) -> bool:
        """Verificar se a senha está correta"""
        return pwd_context.verify(senha, hashed_password)
