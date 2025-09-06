from typing import List

import pandas as pd
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("/", response_model=schemas.Order, status_code=status.HTTP_201_CREATED)
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
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
    for key, value in order.dict(exclude_unset=True).items():
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


@router.post("/import-excel", status_code=status.HTTP_201_CREATED)
def import_orders(
    file: UploadFile = File(...), db: Session = Depends(get_db)
):
    try:
        df = pd.read_excel(file.file)
    except Exception as exc:  # pragma: no cover - depends on pandas/openpyxl
        raise HTTPException(status_code=400, detail="Invalid Excel file") from exc

    required = {"item", "quantity"}
    missing = required - set(df.columns)
    if missing:
        raise HTTPException(
            status_code=400, detail=f"Missing columns: {', '.join(sorted(missing))}"
        )

    orders = [
        models.Order(
            item=row["item"],
            quantity=int(row.get("quantity", 1)),
            operator_id=row.get("operator_id"),
        )
        for _, row in df.iterrows()
    ]
    db.bulk_save_objects(orders)
    db.commit()
    return {"inserted": len(orders)}
