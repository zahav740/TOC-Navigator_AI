from io import BytesIO
from typing import Set

import pandas as pd
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from .. import models
from ..database import get_db

router = APIRouter(prefix="/import", tags=["import"])

REQUIRED_COLUMNS: Set[str] = {"item", "quantity"}


@router.post("/excel")
def import_orders_from_excel(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    try:
        contents = file.file.read()
        df = pd.read_excel(BytesIO(contents))
    except Exception as exc:
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
                db.commit()
                db.refresh(operator)
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
