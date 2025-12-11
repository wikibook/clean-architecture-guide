from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Dict, Optional


class OrderStatus(Enum):
    CREATED = "created"
    PREPARING = "preparing"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class MenuCategory(Enum):
    COFFEE = "coffee"
    TEA = "tea"
    DESSERT = "dessert"


@dataclass
class Menu:
    menu_id: str
    name: str
    price: int
    category: MenuCategory
    stock: int


@dataclass
class OrderOptions:
    size: str
    temperature: str


@dataclass
class Order:
    order_id: str
    customer_id: str
    menu_id: str
    quantity: int
    options: OrderOptions
    status: OrderStatus
    created_at: datetime

    @classmethod
    def create(
        cls,
        order_id: str,
        customer_id: str,
        menu_id: str,
        quantity: int,
        options: Dict[str, str],
    ) -> "Order":
        return cls(
            order_id=order_id,
            customer_id=customer_id,
            menu_id=menu_id,
            quantity=quantity,
            options=OrderOptions(**options),
            status=OrderStatus.CREATED,
            created_at=datetime.utcnow(),
        )