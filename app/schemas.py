from typing import Optional
from datetime import date as Date
from pydantic import BaseModel


class OperatorBase(BaseModel):
    name: str


class OperatorCreate(OperatorBase):
    pass


class OperatorUpdate(BaseModel):
    name: Optional[str] = None


class Operator(OperatorBase):
    id: int

    class Config:
        orm_mode = True


class OrderBase(BaseModel):
    item: Optional[str] = None
    quantity: int = 1
    operator_id: Optional[int] = None
    client: Optional[str] = None
    date: Optional[Date] = None
    status: Optional[str] = None
    manager: Optional[str] = None


class OrderCreate(OrderBase):
    pass


class OrderUpdate(BaseModel):
    item: Optional[str] = None
    quantity: Optional[int] = None
    operator_id: Optional[int] = None
    client: Optional[str] = None
    date: Optional[Date] = None
    status: Optional[str] = None
    manager: Optional[str] = None


class Order(OrderBase):
    id: int
    operator: Optional[Operator] = None

    class Config:
        orm_mode = True


class EventLog(BaseModel):
    """Payload for logging an event related to an order."""

    text: str
