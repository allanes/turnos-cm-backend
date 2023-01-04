from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from sql_app.schemas import medico
from sql_app.crud import crud_medico
from sql_app import crud, models, schemas
from sql_app import deps

router = APIRouter()

@router.get("/", response_model=List[medico.Medico])
def read_medicos(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve medicos.
    """
    medicos = crud_medico.medico.get_multi_with_consultory(db, skip=skip, limit=limit)
    return medicos


@router.post("/", response_model=medico.Medico)
def create_medico(
    *,
    db: Session = Depends(deps.get_db),
    medico_in: medico.MedicoCreate,
) -> Any:
    """
    Create new medico.
    """
    medico = crud_medico.medico.create(db=db, obj_in=medico_in)
    return medico


@router.put("/{id}", response_model=medico.Medico)
def update_medico(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    medico_in: medico.MedicoUpdate,
) -> Any:
    """
    Update an medico.
    """
    medico = crud_medico.medico.get(db=db, id=id)
    if not medico:
        raise HTTPException(status_code=404, detail="Medico not found")
    medico = crud_medico.medico.update(db=db, db_obj=medico, obj_in=medico_in)
    return medico


@router.get("/{id}", response_model=medico.Medico)
def read_medico(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
) -> Any:
    """
    Get medico by ID.
    """
    medico = crud_medico.medico.get(db=db, id=id)
    if not medico:
        raise HTTPException(status_code=404, detail="Medico not found")
    return medico


@router.delete("/{id}", response_model=medico.Medico)
def delete_medico(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
) -> Any:
    """
    Delete an medico.
    """
    medico = crud_medico.medico.get(db=db, id=id)
    if not medico:
        raise HTTPException(status_code=404, detail="Medico not found")
    medico = crud_medico.medico.remove(db=db, id=id)
    return medico
