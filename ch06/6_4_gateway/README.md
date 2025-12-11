### FastAPI 실행
cd /Users/alphahacker/clean-architecture-with-python-test-3 && python -m uvicorn ch06.6_4_gateway.fastapi:app --reload --host 0.0.0.0 --port 8000


### 호출 테스트
curl -X POST "http://localhost:8000/calculate" \
     -H "Content-Type: application/json" \
     -d '{
       "student_id": "student123",
       "calculation_type": "average"
     }'


### 응답 예시
{
  "student_id": "student001",
  "result": 85.5,
  "status": "success"
}