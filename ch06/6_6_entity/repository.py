# Interface Adapters Layer
from abc import ABC, abstractmethod
from typing import List
from .infrastructure import DynamoDBClient


class ScoreRepository(ABC):
    @abstractmethod
    def get_scores(self, student_id: str) -> List[float]:
        pass


class DdbScoreRepository(ScoreRepository):
    def __init__(self, dynamodb_client: DynamoDBClient):
        self.dynamodb_client = dynamodb_client
        self.table_name = "scores"

    def get_scores(self, student_id: str) -> List[float]:
        response = self.dynamodb_client.get_item(table_name=self.table_name, key={"student_id": student_id})
        if "Item" in response and "scores" in response["Item"]:
            return [float(score) for score in response["Item"]["scores"]["L"]]
        return []
