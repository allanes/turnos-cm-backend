from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from sql_app.crud.base import CRUDBase
from sql_app.models import Paciente
from sql_app.schemas.paciente import PacienteCreate, PacienteUpdate

class CRUDPaciente(CRUDBase[Paciente, PacienteCreate, PacienteUpdate]):
    pass

paciente = CRUDPaciente(Paciente)