# Entities Layer (Enterprise Business Rules)
from abc import ABC, abstractmethod
from typing import List


class ScoreValidationPolicy(ABC):
    @abstractmethod
    def validate(self, scores: List[float]) -> None:
        pass


class StandardScoreValidationPolicy(ScoreValidationPolicy):
    def validate(self, scores: List[float]) -> None:
        if any(score < 0 for score in scores):
            raise ValueError("음수 점수는 허용되지 않습니다")
        if any(score > 100 for score in scores):
            raise ValueError("100점을 초과하는 점수는 허용되지 않습니다")


class Scores:
    def __init__(self, values: List[float], validation_policy: ScoreValidationPolicy):
        self.values = values
        self.validation_policy = validation_policy

    def validate(self) -> None:
        """유효성 검증 정책을 적용한다."""
        self.validation_policy.validate(self.values)

    def calculate_average(self) -> float:
        """성적의 평균을 계산한다."""
        if not self.values:
            return 0.0
        return sum(self.values) / len(self.values)


class Student:
    def __init__(self, student_id: str, scores: Scores):
        self.student_id = student_id
        self.scores = scores

    def get_average_score(self) -> float:
        """학생의 평균 성적을 계산한다."""
        return self.scores.calculate_average()

    def validate_scores(self) -> None:
        """학생의 성적을 검증한다."""
        self.scores.validate()
