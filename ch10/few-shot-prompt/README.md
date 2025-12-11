# Coffee Order API

클린 아키텍처를 적용한 온라인 커피 주문 API 서비스입니다.

## 기술 스택
- Python 3.9+
- FastAPI
- DynamoDB (pynamodb)
- AWS Lambda
- Serverless Framework

## 프로젝트 구조
```
src/
├── domain/           # 엔티티와 리포지토리 인터페이스
├── infrastructure/   # 리포지토리 구현체
├── application/     # 유스케이스
└── interfaces/      # API 엔드포인트와 스키마
tests/
├── unit/           # 단위 테스트
└── integration/    # 통합 테스트
```

## 설치 및 실행

1. 의존성 설치:
```bash
pip install -r requirements.txt
```

2. 환경 변수 설정:
```bash
cp .env.example .env
# .env 파일을 적절히 수정
```

3. 로컬 실행:
```bash
uvicorn src.interfaces.api:app --reload
```

4. 배포:
```bash
serverless deploy
```

## API 엔드포인트

- GET /menu - 메뉴 목록 조회
- POST /order - 커피 주문 생성
- GET /order/{orderId} - 주문 상태 확인

## 테스트 실행

```bash
pytest tests/
```