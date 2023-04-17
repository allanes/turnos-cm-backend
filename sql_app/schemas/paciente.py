from datetime import date
from pydantic import BaseModel
from sql_app.schemas import Turno

# Shared properties
class PacienteBase(BaseModel):
    id: int
    nombre: str | None
    apellido: str | None
    fecha_nacimiento: date | None
    email: str | None
    telefono: str | None
    
# Properties to receive on item creation
class PacienteCreate(PacienteBase):
    nombre: str
    apellido: str
    
# Properties to receive on item update    
class PacienteUpdate(BaseModel):
    nombre: str
    apellido: str
    fecha_nacimiento: date
    email: str
    telefono: str

# Properties shared by models stored in DB
class PacienteInDBBase(PacienteBase):
    nombre: str
    apellido: str
    email: str
    fecha_nacimiento: date
    telefono: str
    
    class Config:
        orm_mode = True        

# Properties to return to client
class Paciente(PacienteInDBBase):
    pass


# Properties stored in DB
class PacienteInDB(PacienteInDBBase):
    turnos: list[Turno] = []
    pass