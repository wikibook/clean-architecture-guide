from fastapi import FastAPI
from pydantic import BaseModel
from .dependency_injection import initialize_application
from .controllers import ScoreRequestDTO

app = FastAPI()

# 애플리케이션 초기화
controller = initialize_application()


class ScoreRequest(BaseModel):
    student_id: str
    calculation_type: str


@app.post("/calculate")
async def calculate_score(request: ScoreRequest):
    # 요청을 DTO로 변환
    request_dto = ScoreRequestDTO(student_id=request.student_id, calculation_type=request.calculation_type)

    # 컨트롤러를 통해 유스케이스 실행 및 응답
    return controller.execute(request_dto)
