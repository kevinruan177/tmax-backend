from sqlalchemy.orm import Session
from app.models.driver import Driver, Motorcycle
from app.models.schemas import DriverCreate, DriverUpdate, MotorcycleCreate, MotorcycleUpdate
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class DriverController:
    
    @staticmethod
    def hash_senha(senha: str) -> str:
        return pwd_context.hash(senha)
    
    @staticmethod
    def verificar_senha(senha_plana: str, senha_hash: str) -> bool:
        return pwd_context.verify(senha_plana, senha_hash)
    
    @staticmethod
    def criar_driver(db: Session, driver: DriverCreate):
        db_driver = Driver(
            nome=driver.nome,
            email=driver.email,
            cpf=driver.cpf,
            phone=driver.phone,
            password=DriverController.hash_senha(driver.password)
        )
        db.add(db_driver)
        db.commit()
        db.refresh(db_driver)
        return db_driver
    
    @staticmethod
    def buscar_driver_por_email(db: Session, email: str):
        return db.query(Driver).filter(Driver.email == email).first()
    
    @staticmethod
    def buscar_driver_por_id(db: Session, driver_id: int):
        return db.query(Driver).filter(Driver.id == driver_id).first()
    
    @staticmethod
    def buscar_driver_por_cpf(db: Session, cpf: str):
        return db.query(Driver).filter(Driver.cpf == cpf).first()
    
    @staticmethod
    def listar_drivers(db: Session):
        return db.query(Driver).filter(Driver.is_active == True).all()
    
    @staticmethod
    def atualizar_driver(db: Session, driver_id: int, driver_update: DriverUpdate):
        driver = db.query(Driver).filter(Driver.id == driver_id).first()
        if not driver:
            return None
        
        if driver_update.nome:
            driver.nome = driver_update.nome
        if driver_update.email:
            driver.email = driver_update.email
        if driver_update.phone:
            driver.phone = driver_update.phone
        if driver_update.address_proof:
            driver.address_proof = driver_update.address_proof
        if driver_update.profile_image:
            driver.profile_image = driver_update.profile_image
        if driver_update.rg_images:
            driver.rg_images = driver_update.rg_images
        
        db.commit()
        db.refresh(driver)
        return driver
    
    @staticmethod
    def deletar_driver(db: Session, driver_id: int):
        driver = db.query(Driver).filter(Driver.id == driver_id).first()
        if not driver:
            return None
        
        driver.is_active = False
        db.commit()
        return driver


class MotorcycleController:
    
    @staticmethod
    def criar_motorcycle(db: Session, motorcycle: MotorcycleCreate):
        db_motorcycle = Motorcycle(
            driver_id=motorcycle.driver_id,
            brand=motorcycle.brand,
            model=motorcycle.model,
            year=motorcycle.year,
            plate=motorcycle.plate
        )
        db.add(db_motorcycle)
        db.commit()
        db.refresh(db_motorcycle)
        return db_motorcycle
    
    @staticmethod
    def buscar_motorcycle_por_driver(db: Session, driver_id: int):
        return db.query(Motorcycle).filter(Motorcycle.driver_id == driver_id).first()
    
    @staticmethod
    def buscar_motorcycle_por_id(db: Session, motorcycle_id: int):
        return db.query(Motorcycle).filter(Motorcycle.id == motorcycle_id).first()
    
    @staticmethod
    def atualizar_motorcycle(db: Session, motorcycle_id: int, motorcycle_update: MotorcycleUpdate):
        motorcycle = db.query(Motorcycle).filter(Motorcycle.id == motorcycle_id).first()
        if not motorcycle:
            return None
        
        if motorcycle_update.brand:
            motorcycle.brand = motorcycle_update.brand
        if motorcycle_update.model:
            motorcycle.model = motorcycle_update.model
        if motorcycle_update.year:
            motorcycle.year = motorcycle_update.year
        if motorcycle_update.plate:
            motorcycle.plate = motorcycle_update.plate
        if motorcycle_update.image:
            motorcycle.image = motorcycle_update.image
        
        db.commit()
        db.refresh(motorcycle)
        return motorcycle
    
    @staticmethod
    def deletar_motorcycle(db: Session, motorcycle_id: int):
        motorcycle = db.query(Motorcycle).filter(Motorcycle.id == motorcycle_id).first()
        if not motorcycle:
            return None
        
        motorcycle.is_active = False
        db.commit()
        return motorcycle
    
    @staticmethod
    def atualizar_imagem_moto(db: Session, motorcycle_id: int, image_base64: str):
        motorcycle = db.query(Motorcycle).filter(Motorcycle.id == motorcycle_id).first()
        if not motorcycle:
            return None
        
        motorcycle.image = image_base64
        db.commit()
        db.refresh(motorcycle)
        return motorcycle
