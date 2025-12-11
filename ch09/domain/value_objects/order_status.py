from enum import Enum


class OrderStatus(Enum):
    PENDING = "pending"
    PREPARING = "preparing"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
