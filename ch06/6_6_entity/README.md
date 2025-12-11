## 실행 방법

### 1. FastAPI 서버 실행
```bash
cd /Users/alphahacker/clean-architecture-with-python-test-3
python -m uvicorn ch06.6_6_entity.fastapi:app --reload --port 8000
```

### 2. API 테스트
```bash
curl -X POST "http://localhost:8000/calculate" \
     -H "Content-Type: application/json" \
     -d '{"student_id": "student001", "calculation_type": "average"}'

# 유효하지 않은 점수 (음수)
curl -X POST "http://localhost:8000/calculate" \
     -H "Content-Type: application/json" \
     -d '{"student_id": "student_invalid", "calculation_type": "average"}'

# 유효하지 않은 점수 (100점 초과)
curl -X POST "http://localhost:8000/calculate" \
     -H "Content-Type: application/json" \
     -d '{"student_id": "student_over100", "calculation_type": "average"}'

# 빈 데이터
curl -X POST "http://localhost:8000/calculate" \
     -H "Content-Type: application/json" \
     -d '{"student_id": "student_empty", "calculation_type": "average"}'
```