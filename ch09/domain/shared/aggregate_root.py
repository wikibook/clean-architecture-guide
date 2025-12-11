from typing import List, Any
from datetime import datetime, UTC


class DomainEvent:
    """DDD 도메인 이벤트의 기본 타입.

    의도적으로 단순하게 유지합니다: 이벤트 이름, 발생 시각(UTC), 임의의 페이로드.
    """

    def __init__(self, name: str, payload: Any):
        self.name = name
        self.payload = payload
        self.occurred_on = datetime.now(UTC)

    def __repr__(self) -> str:
        return f"DomainEvent(name={self.name}, occurred_on={self.occurred_on.isoformat()}, payload={self.payload})"


class AggregateRoot:
    """도메인 이벤트를 수집하는 애그리게이트 루트 기본 클래스.

    애플리케이션 계층에서 `pull_domain_events()`를 호출해 이벤트를 발행/전달할 수 있습니다.
    """

    def __init__(self) -> None:
        self._domain_events: List[DomainEvent] = []

    def _record_event(self, event: DomainEvent) -> None:
        self._domain_events.append(event)

    def pull_domain_events(self) -> List[DomainEvent]:
        events = list(self._domain_events)
        self._domain_events.clear()
        return events

