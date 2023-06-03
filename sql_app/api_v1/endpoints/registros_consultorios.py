from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sql_app.servidor_socketio import sio

from sql_app.schemas import registro_consultorios
from sql_app import crud, models, schemas
from sql_app import deps

router = APIRouter()


@router.get("/", response_model=List[registro_consultorios.RegistroConsultorios])
def read_registros_consultorios(
    db: Session = Depends(deps.get_db)
) -> Any:
    """
    Retrieve registros consultorios.
    """
    registro_consultorios = crud.registro_consultorios.get_multi(db=db)
    return registro_consultorios


@router.post("/", response_model=registro_consultorios.RegistroConsultorios)
async def create_registro_consultorio(
    *,
    db: Session = Depends(deps.get_db),
    registro_in: registro_consultorios.RegistroConsultoriosCreate,
) -> Any:
    """
    Create new registro consultorio.
    """
    db_consultorio = crud.consultorio.get(db=db, id=registro_in.id_consultorio)
    if not db_consultorio:
        raise HTTPException(status_code=404, detail="Consultorio no encontrado")
    
    if registro_in.id_medico:
        # Caso Medico Entrando (llega el campo id_medico)
        db_medico = crud.medico.get(db=db, id=registro_in.id_medico) 
    
        if not db_medico:
            raise HTTPException(status_code=404, detail="Medico no encontrado")
        
        lista_ids_consults_activos = [consul_activo.id_consultorio for consul_activo in crud.registro_consultorios.get_multi(db=db)]
        if registro_in.id_consultorio in lista_ids_consults_activos:
            raise HTTPException(status_code=404, detail="Ya existe un médico atendiendo ahí. Por favor libere el consultorio primero.")
        
        
    else:
        # Caso medico saliendo (no llega campo id_medico)
        pass
        
    registro_consultorio = crud.registro_consultorios.create(db=db, obj_in=registro_in)
    print('Emitiendo evento new-office')
    await sio.emit('new-office', f'{registro_consultorio.id_consultorio}')
    
    return registro_consultorio

