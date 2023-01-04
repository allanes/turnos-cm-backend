from typing import Optional

from pydantic import BaseModel
from sql_app.schemas_dep import Turno

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
    activo = True
    
# Properties to receive on item update    
class MedicoUpdate(MedicoBase):
    pass    

# Properties shared by models stored in DB
class MedicoInDBBase(MedicoBase):
    nombre: str
    apellido: str
    email: str
    telefono: str
    activo: bool
    especialidad: str
    
    turnos: list[Turno] = []
    
    class Config:
        orm_mode = True        

# Properties to return to client
class Medico(MedicoInDBBase):
    consultorio: Optional[str]
    

# Properties stored in DB
class MedicoInDB(MedicoInDBBase):
    pass