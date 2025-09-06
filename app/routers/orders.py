from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from io import BytesIO
from typing import Set

import pandas as pd
from fastapi import File, UploadFile

from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/orders", tags=["orders"])

REQUIRED_COLUMNS: Set[str] = {"item", "quantity"}


@router.post("/", response_model=schemas.Order, status_code=status.HTTP_201_CREATED)
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    if not order.item.strip():
        raise HTTPException(status_code=400, detail="Item is required")
    if order.quantity <= 0:
        raise HTTPException(status_code=400, detail="Quantity must be positive")
    if order.operator_id is not None:
        operator = (
            db.query(models.Operator)
            .filter(models.Operator.id == order.operator_id)
            .first()
        )
        if operator is None:
            raise HTTPException(status_code=400, detail="Operator not found")

    db_order = models.Order(**order.dict())
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order


@router.get("/", response_model=List[schemas.Order])
def read_orders(db: Session = Depends(get_db)):
    return db.query(models.Order).all()


@router.get("/{order_id}", response_model=schemas.Order)
def read_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@router.put("/{order_id}", response_model=schemas.Order)
def update_order(order_id: int, order: schemas.OrderUpdate, db: Session = Depends(get_db)):
    db_order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")

    updates = order.dict(exclude_unset=True)
    if "item" in updates and not updates["item"].strip():
        raise HTTPException(status_code=400, detail="Item is required")
    if "quantity" in updates and updates["quantity"] is not None:
        if updates["quantity"] <= 0:
            raise HTTPException(status_code=400, detail="Quantity must be positive")
    if "operator_id" in updates and updates["operator_id"] is not None:
        operator = (
            db.query(models.Operator)
            .filter(models.Operator.id == updates["operator_id"])
            .first()
        )
        if operator is None:
            raise HTTPException(status_code=400, detail="Operator not found")

    for key, value in updates.items():
        setattr(db_order, key, value)
    db.commit()
    db.refresh(db_order)
    return db_order


@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    db.delete(order)
    db.commit()
    return None


@router.post("/import-excel")
def import_orders_from_excel(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    try:
        contents = file.file.read()
        df = pd.read_excel(BytesIO(contents))
    except Exception as exc:  # pragma: no cover - error path
        raise HTTPException(status_code=400, detail=f"Invalid Excel file: {exc}")

    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise HTTPException(
            status_code=400, detail=f"Missing columns: {', '.join(sorted(missing))}"
        )

    created = 0
    for _, row in df.iterrows():
        operator_id = None
        operator_name = row.get("operator")
        if isinstance(operator_name, str) and operator_name:
            operator = (
                db.query(models.Operator)
                .filter(models.Operator.name == operator_name)
                .first()
            )
            if operator is None:
                operator = models.Operator(name=operator_name)
                db.add(operator)
                db.flush()
            operator_id = operator.id

        order = models.Order(
            item=row["item"],
            quantity=int(row["quantity"]) if not pd.isna(row["quantity"]) else 1,
            operator_id=operator_id,
        )
        db.add(order)
        created += 1

    db.commit()

    return {"created": created}
