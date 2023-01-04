from datetime import datetime

from pydantic import BaseModel
# from sql_app.schemas import Medico, Paciente

# Shared properties
class TurnoBase(BaseModel):
    id_consultorio: int | None
    id_medico: int | None
    motivo_consulta: str | None
    
# Properties to receive on item creation
class TurnoCreate(TurnoBase):
    id_consultorio: int
    id_medico: int    
    
# Properties to receive on item update
class TurnoUpdate(TurnoBase):
    pass

# Properties shared by models stored in DB
class TurnoInDBBase(TurnoBase):
    id: int
    pendiente: bool
    fecha: datetime

    # paciente: Paciente
    # medicos: list[Medico] = []

    class Config:
        orm_mode = True
        
# Properties to return to client
class Turno(TurnoInDBBase):
    pass

# Properties properties stored in DB
class TurnoInDB(TurnoInDBBase):
    pass