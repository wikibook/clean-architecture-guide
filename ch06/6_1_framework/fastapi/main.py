from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class ScoreRequest(BaseModel):
    student_id: str
    calculation_type: str  # 예: "average", "total"


@app.post("/calculate")
async def calculate_score(request: ScoreRequest):
    # 컨트롤러로 요청 전달 (6.2 섹션에서 구현)
    result = {"student_id": request.student_id, "calculation_type": request.calculation_type}
    return {"status": "success", "data": result}


# 실행 방법
# root에서 uvicorn ch06.framework:app --reload

# 호출 예시
# curl -X POST "http://127.0.0.1:8000/calculate" -H "Content-Type: application/json" -d '{"student_id": "test_id", "calculation_type": "total"}'

# 호출할때 경로는 project root에서
