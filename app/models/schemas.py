from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# ===== USUARIO =====
class UsuarioBase(BaseModel):
    nome: str 
    email: str
    
class UsuarioCreate(UsuarioBase):
    senha: str

class UsuarioUpdate(BaseModel):
    nome: str | None = None
    email: str | None = None
    senha: str | None = None
    
class Usuario(UsuarioBase):
    id: int
    
    class Config:
        from_attributes = True

# ===== DRIVER =====
class DriverBase(BaseModel):
    nome: str
    email: str
    cpf: str
    phone: str

class DriverCreate(DriverBase):
    password: str

class DriverUpdate(BaseModel):
    nome: str | None = None
    email: str | None = None
    phone: str | None = None
    address_proof: str | None = None
    profile_image: str | None = None
    rg_images: str | None = None

class Driver(DriverBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    profile_image: str | None = None
    rg_images: str | None = None
    address_proof: str | None = None
    
    class Config:
        from_attributes = True

class DriverLogin(BaseModel):
    email: str
    password: str

class DriverRegisterRequest(BaseModel):
    name: str
    email: str
    cpf: str
    phone: str
    password: str
    confirm_password: str

# ===== MOTORCYCLE =====
class MotorcycleBase(BaseModel):
    brand: str | None = None
    model: str | None = None
    year: str | None = None
    plate: str | None = None

class MotorcycleCreate(MotorcycleBase):
    driver_id: int

class MotorcycleUpdate(BaseModel):
    brand: str | None = None
    model: str | None = None
    year: str | None = None
    plate: str | None = None
    image: str | None = None

class Motorcycle(MotorcycleBase):
    id: int
    driver_id: int
    image: str | None = None
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# ===== TOKENS =====
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str | None = None
