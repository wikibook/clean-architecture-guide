from typing import Callable, Dict, List, DefaultDict
from collections import defaultdict

from application.ports.outbound import DomainEventPublisher
from domain.shared.aggregate_root import DomainEvent


class InMemoryEventBus(DomainEventPublisher):
    """데모/테스트를 위한 최소한의 인메모리 퍼브/섭(pub/sub) 버스입니다.

    프로덕션 용도는 아니며, 이벤트 드리븐 흐름을 설명하기 위한 간단한 구현입니다.
    """

    def __init__(self) -> None:
        self._subscribers: DefaultDict[str, List[Callable[[DomainEvent], None]]] = defaultdict(list)

    def subscribe(self, event_name: str, handler: Callable[[DomainEvent], None]) -> None:
        self._subscribers[event_name].append(handler)

    def publish(self, event: DomainEvent) -> None:
        for handler in list(self._subscribers.get(event.name, [])):
            handler(event)

    def publish_all(self, events: List[DomainEvent]) -> None:
        for event in events:
            self.publish(event)

