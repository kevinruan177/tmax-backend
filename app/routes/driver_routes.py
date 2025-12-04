from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.models.schemas import (
    DriverUpdate, Driver as DriverSchema,
    MotorcycleCreate, MotorcycleUpdate, Motorcycle as MotorcycleSchema
)
from app.controllers import DriverController, MotorcycleController
from app.auth import verificar_token
import base64
from io import BytesIO

router = APIRouter(prefix="/driver", tags=["driver"])

# ===== DRIVER ENDPOINTS =====

@router.get("/me", response_model=DriverSchema)
def obter_meu_perfil(email: str = Depends(verificar_token), db: Session = Depends(get_db)):
    """Obter dados do driver logado"""
    driver = DriverController.buscar_driver_por_email(db, email=email)
    if not driver:
        raise HTTPException(status_code=404, detail="Driver não encontrado")
    return driver

@router.get("/{driver_id}", response_model=DriverSchema)
def obter_driver(driver_id: int, db: Session = Depends(get_db)):
    """Obter dados de um driver específico"""
    driver = DriverController.buscar_driver_por_id(db, driver_id=driver_id)
    if not driver:
        raise HTTPException(status_code=404, detail="Driver não encontrado")
    return driver

@router.put("/{driver_id}", response_model=DriverSchema)
def atualizar_driver(
    driver_id: int,
    driver_update: DriverUpdate,
    email: str = Depends(verificar_token),
    db: Session = Depends(get_db)
):
    """Atualizar dados do driver"""
    # Verificar se o driver logado é o mesmo que está sendo atualizado
    driver_logado = DriverController.buscar_driver_por_email(db, email=email)
    if not driver_logado or driver_logado.id != driver_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você não tem permissão para atualizar este driver"
        )
    
    driver = DriverController.atualizar_driver(db, driver_id, driver_update)
    if not driver:
        raise HTTPException(status_code=404, detail="Driver não encontrado")
    return driver

@router.post("/upload/profile")
async def upload_foto_perfil(
    driver_id: int,
    file: UploadFile = File(...),
    email: str = Depends(verificar_token),
    db: Session = Depends(get_db)
):
    """Upload da foto de perfil do driver"""
    
    # Verificar se o driver logado é o mesmo
    driver = DriverController.buscar_driver_por_id(db, driver_id)
    if not driver or driver.email != email:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você não tem permissão para atualizar este driver"
        )
    
    # Ler arquivo e converter para base64
    contents = await file.read()
    file_base64 = base64.b64encode(contents).decode('utf-8')
    
    # Atualizar driver
    driver_update = DriverUpdate(profile_image=file_base64)
    updated_driver = DriverController.atualizar_driver(db, driver_id, driver_update)
    
    return {
        "message": "Foto de perfil atualizada com sucesso",
        "driver_id": updated_driver.id,
        "profile_image": updated_driver.profile_image[:100] + "..." if updated_driver.profile_image else None
    }

@router.post("/upload/rg")
async def upload_rg(
    driver_id: int,
    files: list[UploadFile] = File(...),
    email: str = Depends(verificar_token),
    db: Session = Depends(get_db)
):
    """Upload das fotos de RG do driver"""
    
    # Verificar se o driver logado é o mesmo
    driver = DriverController.buscar_driver_por_id(db, driver_id)
    if not driver or driver.email != email:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você não tem permissão para atualizar este driver"
        )
    
    # Converter arquivo para base64
    rg_images = []
    for file in files[:2]:  # Máximo 2 imagens
        contents = await file.read()
        file_base64 = base64.b64encode(contents).decode('utf-8')
        rg_images.append(file_base64)
    
    # Atualizar driver
    import json
    driver_update = DriverUpdate(rg_images=json.dumps(rg_images))
    updated_driver = DriverController.atualizar_driver(db, driver_id, driver_update)
    
    return {
        "message": "Fotos de RG atualizadas com sucesso",
        "driver_id": updated_driver.id,
        "rg_count": len(rg_images)
    }


# ===== MOTORCYCLE ENDPOINTS =====

@router.post("/vehicle", response_model=dict)
async def upload_imagem_moto(
    file: UploadFile = File(...),
    driver_id: int = None,
    email: str = Depends(verificar_token),
    db: Session = Depends(get_db)
):
    """Upload da imagem da motocicleta do driver"""
    
    # Se não informou driver_id, buscar do token
    if not driver_id:
        driver = DriverController.buscar_driver_por_email(db, email=email)
        if not driver:
            raise HTTPException(status_code=404, detail="Driver não encontrado")
        driver_id = driver.id
    
    # Verificar se o driver logado é o mesmo
    driver = DriverController.buscar_driver_por_id(db, driver_id)
    if not driver or driver.email != email:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você não tem permissão para atualizar este driver"
        )
    
    # Ler arquivo e converter para base64
    contents = await file.read()
    file_base64 = base64.b64encode(contents).decode('utf-8')
    
    # Buscar ou criar motocicleta
    motorcycle = MotorcycleController.buscar_motorcycle_por_driver(db, driver_id)
    
    if not motorcycle:
        # Criar nova motocicleta
        motorcycle_create = MotorcycleCreate(driver_id=driver_id)
        motorcycle = MotorcycleController.criar_motorcycle(db, motorcycle_create)
    
    # Atualizar imagem
    motorcycle_update = MotorcycleUpdate(image=file_base64)
    updated_motorcycle = MotorcycleController.atualizar_motorcycle(db, motorcycle.id, motorcycle_update)
    
    return {
        "message": "Imagem da motocicleta atualizada com sucesso",
        "motorcycle_id": updated_motorcycle.id,
        "driver_id": driver_id
    }

@router.get("/vehicle/{driver_id}", response_model=MotorcycleSchema)
def obter_moto_driver(driver_id: int, db: Session = Depends(get_db)):
    """Obter dados da motocicleta do driver"""
    motorcycle = MotorcycleController.buscar_motorcycle_por_driver(db, driver_id)
    if not motorcycle:
        raise HTTPException(status_code=404, detail="Motocicleta não encontrada")
    return motorcycle

@router.put("/vehicle/{motorcycle_id}", response_model=MotorcycleSchema)
def atualizar_moto(
    motorcycle_id: int,
    motorcycle_update: MotorcycleUpdate,
    email: str = Depends(verificar_token),
    db: Session = Depends(get_db)
):
    """Atualizar dados da motocicleta"""
    motorcycle = MotorcycleController.buscar_motorcycle_por_id(db, motorcycle_id)
    if not motorcycle:
        raise HTTPException(status_code=404, detail="Motocicleta não encontrada")
    
    # Verificar se o driver logado é o proprietário
    driver = DriverController.buscar_driver_por_id(db, motorcycle.driver_id)
    if not driver or driver.email != email:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você não tem permissão para atualizar esta motocicleta"
        )
    
    updated = MotorcycleController.atualizar_motorcycle(db, motorcycle_id, motorcycle_update)
    return updated
