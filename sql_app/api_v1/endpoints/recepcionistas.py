from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from sql_app.schemas import recepcionista
from sql_app.crud import crud_recepcionista
from sql_app import crud, models, schemas
from sql_app import deps

router = APIRouter()

@router.get("/", response_model=List[recepcionista.Recepcionista])
def read_recepcionistas(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve recepcionistas.
    """
    recepcionistas = crud_recepcionista.recepcionista.get_multi(db, skip=skip, limit=limit)
    return recepcionistas


@router.post("/", response_model=recepcionista.Recepcionista)
def create_recepcionista(
    *,
    db: Session = Depends(deps.get_db),
    recepcionista_in: recepcionista.RecepcionistaCreate,
) -> Any:
    """
    Create new recepcionista.
    """
    recepcionista = crud_recepcionista.recepcionista.get(db=db, id=recepcionista_in.id)
    if recepcionista:
        raise HTTPException(status_code=409, detail="Recepcionist already exists")
    recepcionista = crud_recepcionista.recepcionista.create(db=db, obj_in=recepcionista_in)
    return recepcionista


@router.put("/{id}", response_model=recepcionista.Recepcionista)
def update_recepcionista(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    recepcionista_in: recepcionista.RecepcionistaUpdate,
) -> Any:
    """
    Update an recepcionista.
    """
    recepcionista = crud_recepcionista.recepcionista.get(db=db, id=id)
    if not recepcionista:
        raise HTTPException(status_code=404, detail="Recepcionista not found")
    recepcionista = crud_recepcionista.recepcionista.update(db=db, db_obj=recepcionista, obj_in=recepcionista_in)
    return recepcionista


@router.get("/{id}", response_model=recepcionista.Recepcionista)
def read_recepcionista(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
) -> Any:
    """
    Get recepcionista by ID.
    """
    recepcionista = crud_recepcionista.recepcionista.get(db=db, id=id)
    if not recepcionista:
        raise HTTPException(status_code=404, detail="Recepcionista not found")
    return recepcionista


@router.delete("/{id}", response_model=recepcionista.Recepcionista)
def delete_recepcionista(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
) -> Any:
    """
    Delete an recepcionista.
    """
    recepcionista = crud_recepcionista.recepcionista.get(db=db, id=id)
    if not recepcionista:
        raise HTTPException(status_code=404, detail="Recepcionista not found")
    recepcionista = crud_recepcionista.recepcionista.remove(db=db, id=id)
    return recepcionista
