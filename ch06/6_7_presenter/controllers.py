from dataclasses import dataclass
from .usecase import ScoreInputDTO


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
    def __init__(self, calculate_average_usecase: "CalculateAverageUseCase"):
        self.calculate_average_usecase = calculate_average_usecase

    def execute(self, request):
        try:
            if request.calculation_type != "average":
                raise ValueError("Unsupported calculation type")

            # 입력 DTO를 유스케이스에 전달
            input_dto = ScoreInputDTO(student_id=request.student_id)
            self.calculate_average_usecase.execute(input_dto)

            # 프레젠터에서 결과 가져와서 응답
            return self.calculate_average_usecase.presenter.present()

        except Exception:
            import traceback

            print(traceback.format_exc())
            return {"error": "Internal server error"}
