from datetime import datetime

from pydantic import BaseModel, validator,root_validator
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
    nombre_medico: str | None
    nombre_paciente: str | None

    @root_validator(pre=True)
    def calculate_derived_fields(cls, values):
        medico = values.get("medico")
        paciente = values.get("paciente")

        ret = dict(values)
        if medico:
            ret["nombre_medico"] = f"{medico.apellido}, {medico.nombre}"
        if paciente:
            ret["nombre_paciente"] = f"{paciente.apellido}, {paciente.nombre}"

        return ret

    class Config:
        orm_mode = True
        json_encoders = {
            datetime: lambda dt: dt.strftime('%H:%M | %d-%m-%Y')
        }
    

# Properties properties stored in DB
class TurnoInDB(TurnoInDBBase):
    # paciente: Paciente
    # medicos: list[Medico] = []
    pass
