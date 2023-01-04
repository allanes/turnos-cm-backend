from .crud_consultorio import consultorio
from .crud_paciente import paciente
from .crud_recepcionista import recepcionista
from .crud_medico import medico
from .crud_registro_consultorios import registro_consultorios
from .crud_turno import turno
from .load_data import init_db

# For a new basic set of CRUD operations you could just do

# from .base import CRUDBase
# from app.models.item import Item
# from app.schemas.item import ItemCreate, ItemUpdate

# item = CRUDBase[Item, ItemCreate, ItemUpdate](Item)
