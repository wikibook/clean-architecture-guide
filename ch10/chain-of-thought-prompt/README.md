# 커피 주문 API

클린 아키텍처를 적용한 커피 주문 API 프로젝트입니다.

## 기술 스택

- Python 3.9
- FastAPI
- DynamoDB (pynamodb)
- AWS Lambda
- Serverless Framework

## 프로젝트 구조

```
src/
├── application/          # 애플리케이션 계층
│   └── controllers/      # API 컨트롤러
├── domain/              # 도메인 계층
│   ├── entities/        # 엔티티
│   ├── interfaces/      # 인터페이스
│   └── usecases/        # 유스케이스
├── infrastructure/      # 인프라스트럭처 계층
│   ├── presenters/      # 프레젠터
│   └── repositories/    # 레포지토리 구현체
└── config/             # 설정
    └── dependencies.py  # 의존성 주입

tests/
├── integration/        # 통합 테스트
└── unit/              # 단위 테스트
```

## API 엔드포인트

- GET /menu: 메뉴 목록 조회
- POST /order: 주문 생성
- GET /order/{orderId}: 주문 상태 조회

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

## 테스트 실행

```bash
python -m unittest discover tests
```