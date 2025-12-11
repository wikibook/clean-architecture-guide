from dataclasses import dataclass
from typing import Dict, Any
from .usecases import UseCase  # UseCase라는 추상클래스가 존재한다고 가정


@dataclass
class ScoreRequestDTO:
    student_id: str
    calculation_type: str


@dataclass
class ScoreResponseDTO:
    student_id: str
    result: float
    status: str


class CalculateScoreController:
    def __init__(self, calculate_average_usecase: UseCase):
        self.calculate_average_usecase = calculate_average_usecase

    def execute(self, request: ScoreRequestDTO) -> ScoreResponseDTO:
        try:
            if request.calculation_type != "average":
                raise ValueError("Unsupported calculation type")

            # 입력 DTO를 유스케이스에 전달
            average = self.calculate_average_usecase.execute(request.student_id)

            # 출력 DTO로 변환
            return ScoreResponseDTO(student_id=request.student_id, result=average, status="success")
        except Exception as e:
            return ScoreResponseDTO(student_id=request.student_id, result=0.0, status=f"error: {str(e)}")
