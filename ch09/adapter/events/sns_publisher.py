import json
import os
from typing import List

import boto3

from application.ports.outbound import DomainEventPublisher
from domain.shared.aggregate_root import DomainEvent


class SnsDomainEventPublisher(DomainEventPublisher):
    """AWS SNS로 도메인 이벤트를 발행하는 어댑터.

    환경 변수 `SNS_TOPIC_ARN`에서 토픽 ARN을 읽습니다.
    """

    def __init__(self) -> None:
        topic_arn = os.getenv("SNS_TOPIC_ARN")
        if not topic_arn:
            raise RuntimeError("SNS_TOPIC_ARN 환경 변수가 설정되어 있지 않습니다")
        self._topic_arn = topic_arn
        self._client = boto3.client("sns")

    def publish(self, event: DomainEvent) -> None:
        message = {
            "name": event.name,
            "occurred_on": event.occurred_on.isoformat(),
            "payload": event.payload,
        }
        self._client.publish(TopicArn=self._topic_arn, Message=json.dumps(message))

    def publish_all(self, events: List[DomainEvent]) -> None:
        for e in events:
            self.publish(e)

