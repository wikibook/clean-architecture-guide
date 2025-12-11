from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict


@dataclass
class Order:
    order_id: str
    customer_id: str
    menu_id: str
    quantity: int
    status: str
    options: Dict[str, str]
    created_at: datetime
    
    @classmethod
    def create(cls, order_id: str, customer_id: str, menu_id: str, 
              quantity: int, options: Dict[str, str]) -> 'Order':
        return cls(
            order_id=order_id,
            customer_id=customer_id,
            menu_id=menu_id,
            quantity=quantity,
            status="created",
            options=options,
            created_at=datetime.utcnow()
        )
        
    def update_status(self, new_status: str) -> None:
        self.status = new_status