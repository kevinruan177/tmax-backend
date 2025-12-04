from sqlalchemy import Column, Integer, String, DateTime, LargeBinary, Boolean
from app.config.database import Base
from datetime import datetime

class Driver(Base):
    __tablename__ = "drivers"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, index=True, nullable=False)
    cpf = Column(String(14), unique=True, nullable=False)
    phone = Column(String(20), nullable=False)
    password = Column(String(200), nullable=False)
    
    # Imagem de perfil armazenada como base64 ou URL
    profile_image = Column(String(5000), nullable=True)
    
    # RG
    rg_images = Column(String(10000), nullable=True)  # JSON com URLs/base64
    
    # Endereço
    address_proof = Column(String(500), nullable=True)
    
    # Status
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Motorcycle(Base):
    __tablename__ = "motorcycles"

    id = Column(Integer, primary_key=True, index=True)
    driver_id = Column(Integer, nullable=False)
    
    # Informações da moto
    brand = Column(String(100), nullable=True)
    model = Column(String(100), nullable=True)
    year = Column(String(4), nullable=True)
    plate = Column(String(20), unique=True, nullable=True)
    
    # Imagem da moto armazenada como base64 ou URL
    image = Column(String(5000), nullable=True)
    
    # Status
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
