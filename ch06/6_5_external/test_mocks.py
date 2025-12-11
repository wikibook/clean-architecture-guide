# Test Mocks for Clean Architecture
from typing import Dict, Any, List
from .infrastructure import DynamoDBClient
from .repository import ScoreRepository


class MockDynamoDBClient(DynamoDBClient):
    """테스트용 Mock DynamoDB 클라이언트"""

    def __init__(self):
        self.mock_data = {
            "student001": {"Item": {"student_id": "student001", "scores": {"L": [85.5, 92.0, 78.5, 88.0]}}},
            "student002": {"Item": {"student_id": "student002", "scores": {"L": [95.0, 87.5, 91.0]}}},
        }

    def get_item(self, table_name: str, key: Dict[str, Any]) -> Dict[str, Any]:
        student_id = key.get("student_id")
        if student_id in self.mock_data:
            return self.mock_data[student_id]
        return {}


class MockScoreRepository(ScoreRepository):
    """테스트용 Mock Repository"""

    def __init__(self):
        self.mock_scores = {
            "student001": [85.5, 92.0, 78.5, 88.0],
            "student002": [95.0, 87.5, 91.0],
            "student003": [76.0, 82.5, 79.0, 85.0],
        }

    def get_scores(self, student_id: str) -> List[float]:
        return self.mock_scores.get(student_id, [])
