from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from .usecases import CalculateAverageUseCase  # CalculateAverageUseCase 클래스가 존재한다고 가정

app = FastAPI()


class ScoreRequest(BaseModel):
    student_id: str
    calculation_type: str


@app.post("/calculate")
async def calculate_score(request: ScoreRequest):
    try:
        if request.calculation_type != "average":
            raise HTTPException(status_code=400, detail="Unsupported calculation type")

        # 유스케이스 직접 호출
        usecase = CalculateAverageUseCase()
        average = usecase.execute(request.student_id)

        # 응답 변환
        return {"student_id": request.student_id, "result": average, "status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
