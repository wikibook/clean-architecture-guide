## 실행 방법

### 1. FastAPI 서버 실행
```bash
cd /Users/alphahacker/clean-architecture-with-python-test-3
python -m uvicorn ch06.6_5_external.fastapi:app --reload --port 8000
```

### 2. API 테스트
```bash
curl -X POST "http://localhost:8000/calculate" \
     -H "Content-Type: application/json" \
     -d '{"student_id": "student001", "calculation_type": "average"}'
```