from dataclasses import dataclass
from typing import List


@dataclass
class InputDto:
    pass


@dataclass
class OutputDto:
    pass


@dataclass
class CreateOrderInputDto(InputDto):
    customer_id: str
    coffee_id: str
    quantity: int


@dataclass
class CreateOrderOutputDto(OutputDto):
    order_id: str
    customer_id: str
    total_amount: int
    currency: str
    status: str
    items: List[dict]


@dataclass
class GetOrderInputDto(InputDto):
    order_id: str


@dataclass
class GetOrderOutputDto(OutputDto):
    order_id: str
    customer_id: str
    total_amount: int
    currency: str
    status: str
    items: List[dict]
    created_at: str
