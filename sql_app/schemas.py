from enum import Enum
from datetime import datetime
from pydantic import BaseModel, Field

class TurnoBase(BaseModel):
    id_paciente: int
    id_medico: int
    motivo_consulta: str
    fecha: datetime
    estado: str
    
    
class TurnoCreate(TurnoBase):
    pass
    
    
class TurnoUpdate(TurnoBase):
    pass
    
    
class Turno(TurnoBase):
    id: int    

    class Config:
        orm_mode = True

        
class PacienteBase(BaseModel):
    nombre: str
    apellido: str
    email: str
    telefono: str
    
class PacienteCreate(PacienteBase):
    pass
    
class PacienteUpdate(PacienteBase):
    pass
    
class Paciente(PacienteBase):
    id: int
    
    # turnos: list[Turno] = []
    
    class Config:
        orm_mode = True

class MedicoBase(BaseModel):
    nombre: str
    apellido: str
    email: str
    telefono: str
    especialidad: str
    
class MedicoCreate(MedicoBase):
    pass
    
class MedicoUpdate(MedicoBase):
    pass
    
class Medico(MedicoBase):
    id: int
    
    # turnos: list[Turno] = []
    
    class Config:
        orm_mode = True


class RecepcionistaBase(BaseModel):
    nombre: str
    apellido: str
    email: str
    telefono: str
    pass
    
class RecepcionistaCreate(RecepcionistaBase):
    pass

class RecepcionistaUpdate(RecepcionistaBase):
    pass
    
class Recepcionista(RecepcionistaBase):
    id: int
    
    class Config:
        orm_mode = True
    

class ConsultorioBase(BaseModel):
    numero: int
    sala: int
    descripcion: str
    estado: str
    
class ConsultorioCreate(ConsultorioBase):
    pass    
    
class ConsultorioUpdate(ConsultorioBase):
    pass    
    
class Consultorio(ConsultorioBase):
    id: int
    
    class Config:
        orm_mode = True
    
        