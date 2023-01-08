from typing import Optional

from pydantic import BaseModel
from sql_app.schemas import Turno

# Shared properties
class MedicoBase(BaseModel):
    id: int
    nombre: Optional[str]
    apellido: Optional[str]
    email: Optional[str]
    telefono: Optional[str]
    especialidad: Optional[str]
    
# Properties to receive on item creation
class MedicoCreate(MedicoBase):
    nombre: str
    apellido: str
    
# Properties to receive on item update    
class MedicoUpdate(BaseModel):
    nombre: str
    apellido: str
    email: str
    telefono: str
    especialidad: str

# Properties shared by models stored in DB
class MedicoInDBBase(MedicoBase):
    nombre: str
    apellido: str
    email: str
    telefono: str
    especialidad: str
    
    class Config:
        orm_mode = True        

# Properties to return to client
class Medico(MedicoInDBBase):
    consultorio: Optional[str]
    

# Properties stored in DB
class MedicoInDB(MedicoInDBBase):
    activo: bool
    turnos: list[Turno] | None = None
    pass
    