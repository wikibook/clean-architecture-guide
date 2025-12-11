from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class CustomerResponseDTO:
    customer_id: str
    name: str
    email: str
    phone: str
    created_at: datetime
    updated_at: Optional[datetime] = None
