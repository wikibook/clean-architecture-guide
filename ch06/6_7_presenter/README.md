## 실행 방법

### 1. FastAPI 서버 실행
```bash
cd /Users/alphahacker/clean-architecture-with-python-test-3
python -m uvicorn ch06.6_7_presenter.fastapi:app --reload --port 8000
```

### 2. API 테스트

#### POST 요청 (각 형식별 엔드포인트)
```bash
# API 형식
curl -X POST "http://localhost:8000/calculate/api" \
     -H "Content-Type: application/json" \
     -d '{"student_id": "student001", "calculation_type": "average"}'

# Web 형식 (HTML)
curl -X POST "http://localhost:8000/calculate/web" \
     -H "Content-Type: application/json" \
     -d '{"student_id": "student001", "calculation_type": "average"}'
```
