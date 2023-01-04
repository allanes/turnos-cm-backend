from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from sql_app.schemas import paciente
from sql_app.crud import crud_paciente
from sql_app import crud, models, schemas
from sql_app import deps

router = APIRouter()

@router.get("/", response_model=List[paciente.Paciente])
def read_pacientes(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve pacientes.
    """
    pacientes = crud_paciente.paciente.get_multi(db, skip=skip, limit=limit)
    return pacientes


@router.post("/", response_model=paciente.Paciente)
def create_paciente(
    *,
    db: Session = Depends(deps.get_db),
    paciente_in: paciente.PacienteCreate,
) -> Any:
    """
    Create new paciente.
    """
    paciente = crud_paciente.paciente.create(db=db, obj_in=paciente_in)
    return paciente


@router.put("/{id}", response_model=paciente.Paciente)
def update_paciente(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    paciente_in: paciente.PacienteUpdate,
) -> Any:
    """
    Update an paciente.
    """
    paciente = crud_paciente.paciente.get(db=db, id=id)
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente not found")
    paciente = crud_paciente.paciente.update(db=db, db_obj=paciente, obj_in=paciente_in)
    return paciente


@router.get("/{id}", response_model=paciente.Paciente)
def read_paciente(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
) -> Any:
    """
    Get paciente by ID.
    """
    paciente = crud_paciente.paciente.get(db=db, id=id)
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente not found")
    return paciente


@router.delete("/{id}", response_model=paciente.Paciente)
def delete_paciente(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
) -> Any:
    """
    Delete an paciente.
    """
    paciente = crud_paciente.paciente.get(db=db, id=id)
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente not found")
    paciente = crud_paciente.paciente.remove(db=db, id=id)
    return paciente
