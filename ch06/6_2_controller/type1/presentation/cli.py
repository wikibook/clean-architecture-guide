import click
from ..controller.calculater_score_controller import CalculateScoreController, ScoreRequestDTO


@click.command()
@click.option("--student-id", required=True, type=str, help="Student ID")
@click.option("--calculation-type", required=True, type=str, help="Calculation type (average)")
def calculate_score(student_id: str, calculation_type: str):
    controller = CalculateScoreController(...)  # 의존성 주입은 별도 모듈에서 처리
    request_dto = ScoreRequestDTO(student_id=student_id, calculation_type=calculation_type)
    response_dto = controller.execute(request_dto)
    print(f"Student ID: {response_dto.student_id}, Result: {response_dto.result}, Status: {response_dto.status}")
