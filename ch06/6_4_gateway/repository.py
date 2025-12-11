from abc import ABC, abstractmethod
from typing import List
import boto3
from botocore.exceptions import ClientError
import requests


# 게이트웨이 인터페이스 (응용 계층)
class ScoreRepository(ABC):
    @abstractmethod
    def get_scores(self, student_id: str) -> List[float]:
        pass


# DynamoDB 구현체 (인터페이스 어댑터 계층)
class DdbScoreRepository(ScoreRepository):
    def __init__(self):
        self.client = boto3.resource("dynamodb")
        self.table = self.client.Table("scores")

    def get_scores(self, student_id: str) -> List[float]:
        try:
            response = self.table.get_item(Key={"student_id": student_id})
            if "Item" in response and "scores" in response["Item"]:
                # DynamoDB 응답에서 성적 데이터 추출 및 변환
                return [float(score) for score in response["Item"]["scores"]["L"]]
            return []
        except ClientError as e:
            raise ValueError(f"Failed to retrieve scores: {str(e)}")


# 외부 저장소 구현체 (인터페이스 어댑터 계층)
class ApiScoreRepository(ScoreRepository):
    def __init__(self, api_url: str):
        self.api_url = api_url

    def get_scores(self, student_id: str) -> List[float]:
        response = requests.get(f"{self.api_url}/students/{student_id}/scores")
        if response.status_code == 200:
            return [float(score) for score in response.json().get("scores", [])]
        return []
