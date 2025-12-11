from typing import List, Dict
import uuid
from datetime import datetime

from src.domain.entities import Menu, Order
from src.domain.repositories import MenuRepository, OrderRepository
from .exceptions import (
    MenuNotFoundError,
    InsufficientStockError,
    OrderNotFoundError,
    DatabaseError,
)


class GetMenuListUseCase:
    def __init__(self, menu_repository: MenuRepository):
        self.menu_repository = menu_repository

    async def execute(self) -> List[Menu]:
        try:
            return await self.menu_repository.get_all()
        except Exception as e:
            raise DatabaseError(f"메뉴 목록 조회 중 오류 발생: {str(e)}")


class CreateOrderUseCase:
    def __init__(
        self,
        menu_repository: MenuRepository,
        order_repository: OrderRepository,
    ):
        self.menu_repository = menu_repository
        self.order_repository = order_repository

    async def execute(
        self,
        customer_id: str,
        menu_id: str,
        quantity: int,
        options: Dict[str, str],
    ) -> Order:
        try:
            # 메뉴 존재 여부 확인
            menu = await self.menu_repository.get_by_id(menu_id)
            if not menu:
                raise MenuNotFoundError(f"메뉴를 찾을 수 없습니다: {menu_id}")

            # 재고 확인
            if menu.stock < quantity:
                raise InsufficientStockError(
                    f"재고가 부족합니다. 현재 재고: {menu.stock}, 주문 수량: {quantity}"
                )

            # 주문 생성
            order = Order.create(
                order_id=f"order-{uuid.uuid4()}",
                customer_id=customer_id,
                menu_id=menu_id,
                quantity=quantity,
                options=options,
            )

            # 재고 감소
            stock_updated = await self.menu_repository.update_stock(
                menu_id, -quantity
            )
            if not stock_updated:
                raise DatabaseError("재고 업데이트 실패")

            # 주문 저장
            return await self.order_repository.create(order)

        except (MenuNotFoundError, InsufficientStockError) as e:
            raise e
        except Exception as e:
            raise DatabaseError(f"주문 생성 중 오류 발생: {str(e)}")


class GetOrderStatusUseCase:
    def __init__(self, order_repository: OrderRepository):
        self.order_repository = order_repository

    async def execute(self, order_id: str) -> Order:
        try:
            order = await self.order_repository.get_by_id(order_id)
            if not order:
                raise OrderNotFoundError(f"주문을 찾을 수 없습니다: {order_id}")
            return order
        except OrderNotFoundError as e:
            raise e
        except Exception as e:
            raise DatabaseError(f"주문 상태 조회 중 오류 발생: {str(e)}")