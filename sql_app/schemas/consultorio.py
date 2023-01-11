from typing import Optional

from pydantic import BaseModel


# Shared properties
class ConsultorioBase(BaseModel):
    numero: Optional[int]
    sala: Optional[int]
        
# Properties to receive on item creation
class ConsultorioCreate(ConsultorioBase):
    sala: int

# Properties to receive on item update    
class ConsultorioUpdate(ConsultorioBase):
    pass    
    

# Properties shared by models stored in DB
class ConsultorioInDBBase(ConsultorioBase):
    id: int
    numero: int
    sala: int
    
    class Config:
        orm_mode = True
    
# Properties to return to client
class Consultorio(ConsultorioInDBBase):
    descripcion: Optional[str]
    
# Properties to return to client
class ConsultorioDetallado(ConsultorioInDBBase):
    medico: str | None
    pacientes: list[str] | None


# Properties properties stored in DB
class ConsultorioInDB(ConsultorioInDBBase):
    pass