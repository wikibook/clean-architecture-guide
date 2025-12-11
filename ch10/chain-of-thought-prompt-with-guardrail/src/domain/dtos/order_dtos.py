from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Optional


@dataclass
class CreateOrderRequestDTO:
    customer_id: str
    menu_id: str
    quantity: int
    options: Dict[str, str]


@dataclass
class OrderResponseDTO:
    order_id: str
    status: str
    created_at: datetime
    updated_at: Optional[datetime] = None


@dataclass
class DeleteOrderResponseDTO:
    order_id: str
    success: bool
    message: str
