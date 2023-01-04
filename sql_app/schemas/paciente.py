from typing import Optional

from pydantic import BaseModel
from sql_app.schemas_dep import Turno

# Shared properties
class PacienteBase(BaseModel):
    id: int
    nombre: Optional[str]
    apellido: Optional[str]
    email: Optional[str]
    telefono: Optional[str]
    
# Properties to receive on item creation
class PacienteCreate(PacienteBase):
    nombre: str
    apellido: str
    
# Properties to receive on item update    
class PacienteUpdate(PacienteBase):
    pass    

# Properties shared by models stored in DB
class PacienteInDBBase(PacienteBase):
    nombre: str
    apellido: str
    email: str
    telefono: str
    
    turnos: list[Turno] = []
    
    class Config:
        orm_mode = True        

# Properties to return to client
class Paciente(PacienteInDBBase):
    pass


# Properties stored in DB
class PacienteInDB(PacienteInDBBase):
    pass