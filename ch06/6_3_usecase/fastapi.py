from fastapi import FastAPI
from pydantic import BaseModel
from .calculate_average_usecase import CalculateAverageUseCase, ScoreInputDTO

app = FastAPI()


class ScoreRequest(BaseModel):
    student_id: str
    calculation_type: str


@app.post("/calculate")
async def calculate_score(request: ScoreRequest):
    input_dto = ScoreInputDTO(student_id=request.student_id)

    usecase = CalculateAverageUseCase()
    result = usecase.execute(input_dto)  # 유스케이스 호출

    # 응답 변환
    return result.present()
