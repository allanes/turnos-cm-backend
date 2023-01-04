from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from sql_app.schemas import registro_consultorios
from sql_app import crud, models, schemas_dep
from sql_app import deps

router = APIRouter()


@router.get("/", response_model=List[registro_consultorios.RegistroConsultorios])
def read_consultorios(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve registros consultorios.
    """
    registro_consultorios = crud.registro_consultorios.get_multi(db, skip=skip, limit=limit)
    return registro_consultorios


@router.post("/", response_model=registro_consultorios.RegistroConsultorios)
def create_consultorio(
    *,
    db: Session = Depends(deps.get_db),
    registro_in: registro_consultorios.RegistroConsultoriosCreate,
) -> Any:
    """
    Create new registro consultorio.
    """
    registro_consultorio = crud.registro_consultorios.create(db=db, obj_in=registro_in)
    return registro_consultorio
