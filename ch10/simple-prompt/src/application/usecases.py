from datetime import datetime
import uuid
from typing import List, Optional
from src.domain.entities import Menu, Order, OrderStatus
from src.domain.repositories import MenuRepository, OrderRepository

class MenuService:
    def __init__(self, menu_repository: MenuRepository):
        self.menu_repository = menu_repository

    async def get_all_menus(self) -> List[Menu]:
        return await self.menu_repository.get_all()

class OrderService:
    def __init__(
        self,
        order_repository: OrderRepository,
        menu_repository: MenuRepository
    ):
        self.order_repository = order_repository
        self.menu_repository = menu_repository

    async def create_order(
        self,
        customer_id: str,
        menu_id: str,
        quantity: int
    ) -> Optional[Order]:
        menu = await self.menu_repository.get_by_id(menu_id)
        if not menu:
            return None

        if not await self.menu_repository.update_stock(menu_id, quantity):
            return None

        order = Order(
            id=str(uuid.uuid4()),
            customer_id=customer_id,
            menu_id=menu_id,
            quantity=quantity,
            status=OrderStatus.PENDING,
            created_at=datetime.utcnow()
        )
        
        return await self.order_repository.create(order)

    async def get_order(self, order_id: str) -> Optional[Order]:
        return await self.order_repository.get_by_id(order_id)