from typing import Optional

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
    item: str
    quantity: int = 1
    operator_id: Optional[int] = None


class OrderCreate(OrderBase):
    pass


class OrderUpdate(BaseModel):
    item: Optional[str] = None
    quantity: Optional[int] = None
    operator_id: Optional[int] = None


class Order(OrderBase):
    id: int
    operator: Optional[Operator] = None

    class Config:
        orm_mode = True
