from typing import Optional

from pydantic import BaseModel


# Shared properties
class ConsultorioBase(BaseModel):
    numero: Optional[int]
    sala: Optional[int]
    descripcion: Optional[str]
    
# Properties to receive on item creation
class ConsultorioCreate(ConsultorioBase):
    numero: int
    sala: int

# Properties to receive on item update    
class ConsultorioUpdate(ConsultorioBase):
    pass    
    

# Properties shared by models stored in DB
class ConsultorioInDBBase(ConsultorioBase):
    id: int
    numero: int
    sala: int
    descripcion: str
    
    class Config:
        orm_mode = True
        

# Properties to return to client
class Consultorio(ConsultorioInDBBase):
    pass


# Properties properties stored in DB
class ItemInDB(ConsultorioInDBBase):
    pass