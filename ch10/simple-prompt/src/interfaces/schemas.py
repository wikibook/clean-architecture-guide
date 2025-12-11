from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class MenuResponse(BaseModel):
    id: str
    name: str
    price: int
    category: str

class CreateOrderRequest(BaseModel):
    customer_id: str
    menu_id: str
    quantity: int

class OrderResponse(BaseModel):
    id: str
    status: str
    created_at: datetime
    updated_at: Optional[datetime] = None