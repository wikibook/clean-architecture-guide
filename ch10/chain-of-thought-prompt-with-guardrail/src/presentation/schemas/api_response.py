from datetime import datetime
from typing import Dict, Generic, Optional, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class APIResponse(BaseModel, Generic[T]):
    status: str
    message: str
    data: Optional[T] = None


class MenuResponse(BaseModel):
    menu_id: str
    name: str
    price: int
    category: str


class MenuListResponse(BaseModel):
    menus: list[MenuResponse]


class CreateOrderRequest(BaseModel):
    customer_id: str
    menu_id: str
    quantity: int
    options: Dict[str, str]


class OrderResponse(BaseModel):
    order_id: str
    status: str
    created_at: datetime
    updated_at: Optional[datetime] = None


class CustomerResponse(BaseModel):
    customer_id: str
    name: str
    email: str
    phone: str
    created_at: datetime
    updated_at: Optional[datetime] = None


class DeleteOrderResponse(BaseModel):
    order_id: str
    success: bool
    message: str
