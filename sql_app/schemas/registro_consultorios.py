from typing import Optional
from datetime import datetime

from pydantic import BaseModel

# Shared properties
class RegistroConsultoriosBase(BaseModel):
    id_consultorio: int | None
    id_medico: int | None
    
# Properties to receive on item creation
class RegistroConsultoriosCreate(RegistroConsultoriosBase):
    id_consultorio: int
    id_medico: int    
    
# Properties to receive on item update
class RegistroConsultoriosUpdate(RegistroConsultoriosBase):
    pass

# Properties shared by models stored in DB
class RegistroConsultoriosInDBBase(RegistroConsultoriosBase):
    id: int
    id_consultorio: int
    id_medico: int
    fecha: datetime

    class Config:
        orm_mode = True
        
# Properties to return to client
class RegistroConsultorios(RegistroConsultoriosInDBBase):
    pass

# Properties properties stored in DB
class RegistroConsultoriosInDB(RegistroConsultoriosInDBBase):
    pass