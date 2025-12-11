# 커피 주문 API

클린 아키텍처 원칙을 따르는 커피 주문 API 서비스입니다.

## 기술 스택

- Python 3.9
- FastAPI
- DynamoDB (pynamodb)
- AWS Lambda
- Serverless Framework

## 프로젝트 구조

```
src/
├── domain/
│   ├── entities/          # 비즈니스 엔티티
│   ├── interfaces/        # 인터페이스 정의
│   └── usecases/         # 비즈니스 유스케이스
├── infrastructure/
│   ├── repositories/     # 데이터베이스 구현체
│   └── presenters/      # 프레젠터 구현체
├── application/
│   └── controllers/     # API 컨트롤러
└── config/             # 의존성 주입 설정
```

## API 엔드포인트

### GET /menus
- 메뉴 목록 조회
- 응답: 메뉴 ID, 이름, 가격, 카테고리

### POST /orders
- 커피 주문 생성
- 요청: 고객 ID, 커피 ID, 수량, 옵션
- 응답: 주문 ID, 상태

### GET /orders/{orderId}
- 주문 상태 조회
- 응답: 주문 ID, 상태, 생성 시간

## 설치 및 실행

1. 의존성 설치:
```bash
pip install -r requirements.txt
```

2. 로컬 실행:
```bash
uvicorn src.main:app --reload
```

3. 배포:
```bash
serverless deploy
```

## 테스트

단위 테스트 실행:
```bash
python -m pytest tests/unit
```

통합 테스트 실행:
```bash
python -m pytest tests/integration
```