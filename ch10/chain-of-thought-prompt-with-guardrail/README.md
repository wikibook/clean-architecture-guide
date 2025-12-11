# Coffee Order API

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
├── domain/           # 엔티티, 유스케이스, 레포지토리 인터페이스
│   ├── entities/     # 도메인 엔티티
│   ├── repositories/ # 레포지토리 인터페이스
│   ├── usecases/    # 비즈니스 로직
│   └── dtos/        # 데이터 전송 객체
├── application/      # 애플리케이션 서비스
├── infrastructure/   # 외부 시스템 통합 (데이터베이스 등)
├── presentation/     # API 엔드포인트, 컨트롤러
└── config/          # 의존성 주입 설정

tests/
├── unit/            # 단위 테스트
└── integration/     # 통합 테스트
```

## 개발 환경 설정

1. 의존성 설치:
```bash
# 프로덕션 의존성 설치
pip install -r requirements.txt

# 개발 의존성 설치
pip install -r requirements-dev.txt

# pre-commit 설치 및 설정
pre-commit install
```

2. 코드 품질 도구:
- Black: 코드 포맷팅
- isort: import 문 정렬
- Ruff: 린팅
- MyPy: 타입 체크
- Bandit: 보안 취약점 검사

각 도구의 설정은 `pyproject.toml`에서 관리됩니다.

## 실행 방법

1. 로컬 실행:
```bash
uvicorn src.main:app --reload
```

2. 테스트 실행:
```bash
python -m pytest tests/
```

3. 코드 품질 검사:
```bash
# 전체 파일 검사
pre-commit run --all-files

# 스테이징된 파일만 검사
git add .
pre-commit run
```

4. 배포:
```bash
serverless deploy
```

## API 엔드포인트

### 메뉴 목록 조회
- GET /menu
- 응답: 메뉴 ID, 이름, 가격, 카테고리 목록

### 주문 생성
- POST /order
- 요청: 고객 ID, 메뉴 ID, 수량, 옵션
- 응답: 주문 ID, 상태

### 주문 상태 확인
- GET /order/{orderId}
- 응답: 주문 ID, 상태, 생성 시간

## 아키텍처 설계

이 프로젝트는 클린 아키텍처 원칙을 따릅니다:

1. 의존성 규칙: 외부에서 내부로 향하는 의존성
2. 계층 분리: 도메인, 애플리케이션, 인프라스트럭처 계층
3. SOLID 원칙 준수
4. 테스트 용이성
5. 프레임워크 독립성

## 코드 품질 관리

이 프로젝트는 다음과 같은 코드 품질 도구들을 사용합니다:

1. Black
   - Python 코드 포맷터
   - 일관된 코드 스타일 유지
   - 줄 길이 88자 제한

2. isort
   - import 문 자동 정렬
   - Black 호환 설정 사용

3. Ruff
   - 빠른 Python 린터
   - 다양한 코드 품질 규칙 검사
   - 자동 수정 기능 제공

4. MyPy
   - 정적 타입 검사기
   - 타입 힌트 검증
   - 타입 관련 버그 예방

5. Bandit
   - 보안 취약점 검사
   - 잠재적인 보안 이슈 식별
   - 테스트 코드 제외 설정