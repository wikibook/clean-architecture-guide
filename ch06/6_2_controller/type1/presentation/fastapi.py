from fastapi import FastAPI
from pydantic import BaseModel
from ..controller.calculater_score_controller import CalculateScoreController, ScoreRequestDTO

app = FastAPI()


class ScoreRequest(BaseModel):
    student_id: str
    calculation_type: str


@app.post("/calculate")
async def calculate_score(request: ScoreRequest):
    controller = CalculateScoreController(...)  # 의존성 주입은 별도 모듈에서 처리
    request_dto = ScoreRequestDTO(student_id=request.student_id, calculation_type=request.calculation_type)
    response_dto = controller.execute(request_dto)
    return {"student_id": response_dto.student_id, "result": response_dto.result, "status": response_dto.status}
