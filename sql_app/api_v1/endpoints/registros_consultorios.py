from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

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
def create_registro_consultorio(
    *,
    db: Session = Depends(deps.get_db),
    registro_in: registro_consultorios.RegistroConsultoriosCreate,
) -> Any:
    """
    Create new registro consultorio.
    """
    db_consultorio = crud.consultorio.get(db=db, id=registro_in.id_consultorio)
    if not db_consultorio:
        raise HTTPException(status_code=404, detail="Consultorio not found")
    
    if registro_in.id_medico:
        db_medico = crud.medico.get(db=db, id=registro_in.id_medico) 
    
        if not db_medico:
            raise HTTPException(status_code=404, detail="Medico not found")
        
    registro_consultorio = crud.registro_consultorios.create(db=db, obj_in=registro_in)
    
    return registro_consultorio
