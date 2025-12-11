from pydantic import BaseModel
from typing import List, Optional, Dict
from datetime import datetime


class MenuResponse(BaseModel):
    menu_id: str
    name: str
    price: int
    category: str


class OrderOptions(BaseModel):
    size: str
    temperature: str


class CreateOrderRequest(BaseModel):
    customer_id: str
    menu_id: str
    quantity: int
    options: OrderOptions


class OrderResponse(BaseModel):
    order_id: str
    status: str
    created_at: datetime


class APIResponse(BaseModel):
    status: str
    data: Optional[dict] = None
    message: str