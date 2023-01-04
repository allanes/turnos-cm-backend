from pydantic import BaseModel

class RecepcionistaBase(BaseModel):
    dni: int
    nombre: str
    apellido: str
    email: str
    telefono: str
    
class RecepcionistaCreate(RecepcionistaBase):
    pass

class RecepcionistaUpdate(RecepcionistaBase):
    pass
    
class Recepcionista(RecepcionistaBase):
    id: int
    
    class Config:
        orm_mode = True
    
