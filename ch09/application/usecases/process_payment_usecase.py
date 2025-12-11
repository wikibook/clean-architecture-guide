from application.ports.repository import OrderRepository
from application.ports.outbound import PaymentGateway
from domain.entities.order import OrderStatus


class ProcessPaymentUseCase:
    """주문 생성 이벤트를 받아 결제를 시도하고 주문 상태를 갱신하는 애플리케이션 서비스."""

    def __init__(self, order_repo: OrderRepository, payment_gateway: PaymentGateway) -> None:
        self.order_repo = order_repo
        self.payment_gateway = payment_gateway

    def execute(self, order_id: str) -> None:
        order = self.order_repo.find_by_id(order_id)
        if order is None:
            return

        approved = self.payment_gateway.approve(
            order_id=order.id,
            amount=order.total_amount.amount,
            currency=order.total_amount.currency,
        )

        if approved and order.status == OrderStatus.PENDING:
            order.change_status(OrderStatus.PREPARING)
            self.order_repo.save(order)
        elif not approved and order.status == OrderStatus.PENDING:
            order.change_status(OrderStatus.CANCELLED)
            self.order_repo.save(order)

