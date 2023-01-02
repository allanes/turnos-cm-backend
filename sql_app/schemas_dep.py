from datetime import datetime
from pydantic import BaseModel

class TurnoBase(BaseModel):
    id_paciente: int
    id_medico: int
    motivo_consulta: str
    fecha: datetime
        
class TurnoCreate(TurnoBase):
    pendiente = False
        
class TurnoUpdate(TurnoBase):
    pass    
    
class Turno(TurnoBase):
    id: int
    
    # paciente: Paciente
    # medico: Medico
    
    class Config:
        orm_mode = True


class PacienteBase(BaseModel):
    dni: int
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
    
    turnos: list[Turno] = []
    
    class Config:
        orm_mode = True


class MedicoBase(BaseModel):
    dni: int
    nombre: str
    apellido: str
    email: str
    telefono: str
    especialidad: str
    
class MedicoCreate(MedicoBase):
    activo = True
    
class MedicoUpdate(MedicoBase):
    pass
    
class Medico(MedicoBase):
    id: int
    activo:bool
    consultorio: str | None
    turnos: list[Turno] = []
    
    class Config:
        orm_mode = True
        
class RegistroConsultoriosBase(BaseModel):
    id_consultorio: int
    id_medico: int
    fecha: datetime

class RegistroConsultoriosCreate(RegistroConsultoriosBase):
    pass

class RegistroConsultoriosUpdate(RegistroConsultoriosBase):
    pass

class RegistroConsultorios(RegistroConsultoriosBase):
    id: int

    class Config:
        orm_mode = True

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
    
