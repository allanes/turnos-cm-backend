from datetime import datetime

from pydantic import BaseModel
# from sql_app.schemas import Medico, Paciente

# Shared properties
class TurnoBase(BaseModel):
    id_medico: int | None
    id_paciente: int | None
    motivo_consulta: str | None
    
# Properties to receive on item creation
class TurnoCreate(TurnoBase):
    id_medico: int
    id_paciente: int
    
# Properties to receive on item update
class TurnoUpdate(TurnoBase):
    pass

# Properties shared by models stored in DB
class TurnoInDBBase(TurnoBase):
    id: int
    pendiente: bool
    fecha: datetime

    class Config:
        orm_mode = True
        
# Properties to return to client
class Turno(TurnoInDBBase):
    pass

# Properties properties stored in DB
class TurnoInDB(TurnoInDBBase):
    # paciente: Paciente
    # medicos: list[Medico] = []
    pass
