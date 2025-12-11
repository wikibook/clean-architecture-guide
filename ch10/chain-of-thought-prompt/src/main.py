from fastapi import FastAPI
from mangum import Mangum
from .config.dependencies import Dependencies

# FastAPI 애플리케이션 생성
app = FastAPI(
    title="Coffee Shop API",
    description="Clean Architecture를 적용한 커피 주문 API",
    version="1.0.0"
)

# 의존성 설정
menu_controller, order_controller = Dependencies.configure()

# 라우터 등록
menu_controller.register_routes(app)
order_controller.register_routes(app)

# AWS Lambda 핸들러
handler = Mangum(app)