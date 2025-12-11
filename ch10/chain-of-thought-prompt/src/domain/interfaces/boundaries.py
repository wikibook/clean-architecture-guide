from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Dict, Optional
from datetime import datetime
from ..entities.order import OrderStatus

# Input DTOs
@dataclass
class CreateOrderInputDTO:
    customer_id: str
    menu_id: str
    quantity: int
    options: Dict[str, str]

@dataclass
class GetOrderInputDTO:
    order_id: str

# Output DTOs
@dataclass
class MenuOutputDTO:
    menu_id: str
    name: str
    price: int
    category: str

@dataclass
class OrderOutputDTO:
    order_id: str
    status: OrderStatus
    created_at: datetime

@dataclass
class ResponseDTO:
    status: str
    data: Optional[any]
    message: str

# Input Boundaries (Use Cases)
class MenuInputBoundary(ABC):
    @abstractmethod
    def get_all_menus(self) -> List[MenuOutputDTO]:
        pass

class OrderInputBoundary(ABC):
    @abstractmethod
    def create_order(self, input_dto: CreateOrderInputDTO) -> OrderOutputDTO:
        pass

    @abstractmethod
    def get_order(self, input_dto: GetOrderInputDTO) -> OrderOutputDTO:
        pass

# Output Boundaries (Presenters)
class OutputBoundary(ABC):
    @abstractmethod
    def present_success(self, data: any, message: str) -> ResponseDTO:
        pass

    @abstractmethod
    def present_error(self, message: str) -> ResponseDTO:
        pass