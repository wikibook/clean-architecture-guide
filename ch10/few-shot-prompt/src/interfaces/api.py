from fastapi import FastAPI, HTTPException
from mangum import Mangum

from src.application.exceptions import (
    MenuNotFoundError,
    InsufficientStockError,
    OrderNotFoundError,
    DatabaseError,
)
from src.application.usecases import (
    GetMenuListUseCase,
    CreateOrderUseCase,
    GetOrderStatusUseCase,
)
from src.infrastructure.repositories import (
    DynamoDBMenuRepository,
    DynamoDBOrderRepository,
)
from .schemas import (
    MenuResponse,
    CreateOrderRequest,
    OrderResponse,
    APIResponse,
)

app = FastAPI(title="Coffee Order API")

# 리포지토리 인스턴스 생성
menu_repository = DynamoDBMenuRepository()
order_repository = DynamoDBOrderRepository()

# 유스케이스 인스턴스 생성
get_menu_list_usecase = GetMenuListUseCase(menu_repository)
create_order_usecase = CreateOrderUseCase(menu_repository, order_repository)
get_order_status_usecase = GetOrderStatusUseCase(order_repository)


@app.get("/menu", response_model=APIResponse)
async def get_menu_list():
    try:
        menus = await get_menu_list_usecase.execute()
        return APIResponse(
            status="success",
            data=[
                MenuResponse(
                    menu_id=menu.menu_id,
                    name=menu.name,
                    price=menu.price,
                    category=menu.category.value,
                ).__dict__
                for menu in menus
            ],
            message="Menus retrieved successfully",
        )
    except DatabaseError as e:
        raise HTTPException(
            status_code=500,
            detail=str(e),
        )


@app.post("/order", response_model=APIResponse, status_code=201)
async def create_order(request: CreateOrderRequest):
    try:
        order = await create_order_usecase.execute(
            customer_id=request.customer_id,
            menu_id=request.menu_id,
            quantity=request.quantity,
            options=request.options.dict(),
        )
        return APIResponse(
            status="success",
            data=OrderResponse(
                order_id=order.order_id,
                status=order.status.value,
                created_at=order.created_at,
            ).__dict__,
            message="Order created successfully",
        )
    except MenuNotFoundError:
        raise HTTPException(
            status_code=404,
            detail="Invalid menu ID",
        )
    except InsufficientStockError:
        raise HTTPException(
            status_code=400,
            detail="Insufficient stock",
        )
    except DatabaseError as e:
        raise HTTPException(
            status_code=500,
            detail=str(e),
        )


@app.get("/order/{order_id}", response_model=APIResponse)
async def get_order_status(order_id: str):
    try:
        order = await get_order_status_usecase.execute(order_id)
        return APIResponse(
            status="success",
            data=OrderResponse(
                order_id=order.order_id,
                status=order.status.value,
                created_at=order.created_at,
            ).__dict__,
            message="Order status retrieved successfully",
        )
    except OrderNotFoundError:
        raise HTTPException(
            status_code=404,
            detail="Order not found",
        )
    except DatabaseError as e:
        raise HTTPException(
            status_code=500,
            detail=str(e),
        )


# AWS Lambda 핸들러
handler = Mangum(app)