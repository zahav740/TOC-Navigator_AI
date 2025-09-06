from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/operators", tags=["operators"])


@router.post("/", response_model=schemas.Operator, status_code=status.HTTP_201_CREATED)
def create_operator(operator: schemas.OperatorCreate, db: Session = Depends(get_db)):
    if not operator.name.strip():
        raise HTTPException(status_code=400, detail="Name is required")

    existing = (
        db.query(models.Operator).filter(models.Operator.name == operator.name).first()
    )
    if existing:
        raise HTTPException(status_code=400, detail="Operator already exists")

    db_operator = models.Operator(**operator.dict())
    db.add(db_operator)
    db.commit()
    db.refresh(db_operator)
    return db_operator


@router.get("/", response_model=List[schemas.Operator])
def read_operators(db: Session = Depends(get_db)):
    return db.query(models.Operator).all()


@router.get("/{operator_id}", response_model=schemas.Operator)
def read_operator(operator_id: int, db: Session = Depends(get_db)):
    operator = (
        db.query(models.Operator).filter(models.Operator.id == operator_id).first()
    )
    if operator is None:
        raise HTTPException(status_code=404, detail="Operator not found")
    return operator


@router.put("/{operator_id}", response_model=schemas.Operator)
def update_operator(
    operator_id: int, operator: schemas.OperatorUpdate, db: Session = Depends(get_db)
):
    db_operator = (
        db.query(models.Operator).filter(models.Operator.id == operator_id).first()
    )
    if db_operator is None:
        raise HTTPException(status_code=404, detail="Operator not found")

    updates = operator.dict(exclude_unset=True)
    if "name" in updates and not updates["name"].strip():
        raise HTTPException(status_code=400, detail="Name is required")

    if "name" in updates:
        existing = (
            db.query(models.Operator)
            .filter(models.Operator.name == updates["name"])
            .first()
        )
        if existing and existing.id != operator_id:
            raise HTTPException(status_code=400, detail="Operator already exists")

    for key, value in updates.items():
        setattr(db_operator, key, value)
    db.commit()
    db.refresh(db_operator)
    return db_operator


@router.delete("/{operator_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_operator(operator_id: int, db: Session = Depends(get_db)):
    operator = (
        db.query(models.Operator).filter(models.Operator.id == operator_id).first()
    )
    if operator is None:
        raise HTTPException(status_code=404, detail="Operator not found")
    db.delete(operator)
    db.commit()
    return None
