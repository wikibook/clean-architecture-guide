from typing import Optional, List
import datetime

from application.ports.repository import CoffeeRepository, OrderRepository
from domain.entities.order import Order, OrderStatus
from domain.entities.coffee import Coffee
from domain.entities.order_item import OrderItem
from domain.value_objects.money import Money
from infrastructure.persistence.tables import CoffeeModel, OrderModel, OrderItemModel


class DynamoDBCoffeeRepository(CoffeeRepository):
    def find_by_id(self, coffee_id: str) -> Optional[Coffee]:
        try:
            model = CoffeeModel.get(coffee_id)
            price = Money(amount=model.price, currency=model.currency)
            return Coffee(id=model.id, name=model.name, price=price, description=model.description, stock=model.stock)
        except CoffeeModel.DoesNotExist:
            return None

    def find_all_available(self) -> List[Coffee]:
        coffees = []
        for model in CoffeeModel.scan():
            if model.stock > 0:
                price = Money(amount=model.price, currency=model.currency)
                coffee = Coffee(
                    id=model.id, name=model.name, price=price, description=model.description, stock=model.stock
                )
                coffees.append(coffee)
        return coffees

    def save(self, coffee: Coffee) -> None:
        model = CoffeeModel(
            id=coffee.id,
            name=coffee.name,
            price=coffee.price.amount,
            currency=coffee.price.currency,
            description=coffee.description,
            stock=coffee.stock,
        )
        model.save()


class DynamoDBOrderRepository(OrderRepository):
    def find_by_id(self, order_id: str) -> Optional[Order]:
        try:
            model = OrderModel.get(order_id)
            order = Order(id=model.id, customer_id=model.customer_id)
            # 상태와 생성 시간 설정
            order.status = OrderStatus(model.status)
            order.created_at = datetime.datetime.fromisoformat(model.created_at)
            # 총액 설정
            order.total_amount = Money(amount=model.total_amount, currency=model.currency)

            # OrderItem들을 찾아서 추가
            for item_model in OrderItemModel.scan(order_id__eq=order_id):
                item = OrderItem(
                    id=item_model.id,
                    order_id=item_model.order_id,
                    coffee_id=item_model.coffee_id,
                    quantity=item_model.quantity,
                    unit_price=Money(amount=item_model.unit_price, currency=item_model.currency),
                )
                order.items.append(item)

            return order
        except OrderModel.DoesNotExist:
            return None

    def save(self, order: Order) -> None:
        # Order 저장
        model = OrderModel(
            id=order.id,
            customer_id=order.customer_id,
            total_amount=order.total_amount.amount,
            currency=order.total_amount.currency,
            status=order.status.value,
            created_at=order.created_at.isoformat(),
        )
        model.save()

        # OrderItem들 저장
        for item in order.items:
            item_model = OrderItemModel(
                id=item.id,
                order_id=item.order_id,
                coffee_id=item.coffee_id,
                quantity=item.quantity,
                unit_price=item.unit_price.amount,
                currency=item.unit_price.currency,
            )
            item_model.save()
