from typing import List, Set
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from io import BytesIO

import pandas as pd
from fastapi import File, UploadFile
from pydantic import BaseModel, ValidationError
from datetime import date

from .. import models, schemas
from ..database import get_db
from ..qdrant import log_event as log_event_to_qdrant

router = APIRouter(prefix="/orders", tags=["orders"])

REQUIRED_COLUMNS: Set[str] = {"client", "date", "status", "manager"}


class OrderExcelRow(BaseModel):
    client: str
    date: date
    status: str
    manager: str


@router.post("/", response_model=schemas.Order, status_code=status.HTTP_201_CREATED)
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    if not order.item or not order.item.strip():
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
    if "item" in updates:
        if not updates["item"] or not updates["item"].strip():
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


@router.post("/{order_id}/log-event", status_code=status.HTTP_201_CREATED)
def log_event(order_id: int, event: schemas.EventLog, db: Session = Depends(get_db)):
    """Log a textual event for an order and store it in Qdrant."""
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    try:
        log_event_to_qdrant(order_id, event.text)
    except Exception as exc:  # pragma: no cover - external service errors
        raise HTTPException(status_code=500, detail=f"Failed to log event: {exc}")
    return {"status": "logged"}


@router.post("/import-excel")
def import_orders_from_excel(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    """Import orders from an uploaded Excel file.

    Each row is validated against ``OrderExcelRow`` and only valid rows
    are persisted. Rows failing validation are returned in the ``errors``
    list along with details about the failure.
    """
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
    errors = []
    for idx, row in df.iterrows():
        try:
            data = OrderExcelRow(**row.to_dict())
        except ValidationError as e:  # pragma: no cover - depends on data
            errors.append({"row": idx, "errors": e.errors()})
            continue

        order = models.Order(
            client=data.client,
            date=data.date,
            status=data.status,
            manager=data.manager,
        )
        db.add(order)
        created += 1

    db.commit()

    return {"created": created, "errors": errors}
