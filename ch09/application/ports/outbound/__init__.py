from abc import ABCMeta, abstractmethod, ABC

from application.dtos import OutputDto
from domain.shared.aggregate_root import DomainEvent


class OutputBoundary(metaclass=ABCMeta):
    @abstractmethod
    def set_result(self, output_dto: OutputDto) -> None:
        pass

    @abstractmethod
    def present(self) -> dict:
        pass


class DomainEventPublisher(ABC):
    """도메인 이벤트를 버스/구독자에게 발행하기 위한 아웃바운드 포트입니다."""

    @abstractmethod
    def publish(self, event: DomainEvent) -> None:
        pass

    @abstractmethod
    def publish_all(self, events: list[DomainEvent]) -> None:
        pass


class PaymentGateway(ABC):
    """외부 결제 게이트웨이 연동을 위한 아웃바운드 포트입니다."""

    @abstractmethod
    def approve(self, order_id: str, amount: int, currency: str) -> bool:
        """결제 승인 시도. 성공 여부를 반환합니다."""
        pass
