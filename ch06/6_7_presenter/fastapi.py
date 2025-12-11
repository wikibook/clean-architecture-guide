from fastapi import FastAPI
from pydantic import BaseModel
from .dependency_injection import initialize_application, initialize_web_application
from .controllers import ScoreRequestDTO

app = FastAPI()

# 각 형식별로 별도의 컨트롤러 초기화
api_controller = initialize_application()
web_controller = initialize_web_application()


class ScoreRequest(BaseModel):
    student_id: str
    calculation_type: str


@app.post("/calculate/api")
async def calculate_score_api(request: ScoreRequest):
    """API 형식으로 응답"""
    request_dto = ScoreRequestDTO(student_id=request.student_id, calculation_type=request.calculation_type)
    return api_controller.execute(request_dto)


@app.post("/calculate/web")
async def calculate_score_web(request: ScoreRequest):
    """HTML 형식으로 응답"""
    request_dto = ScoreRequestDTO(student_id=request.student_id, calculation_type=request.calculation_type)
    return web_controller.execute(request_dto)
