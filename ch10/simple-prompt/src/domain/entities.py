from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional

class OrderStatus(Enum):
    PENDING = "PENDING"
    PREPARING = "PREPARING"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"

@dataclass
class Menu:
    id: str
    name: str
    price: int
    category: str
    stock: int

@dataclass
class Order:
    id: str
    customer_id: str
    menu_id: str
    quantity: int
    status: OrderStatus
    created_at: datetime
    updated_at: Optional[datetime] = None