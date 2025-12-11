from fastapi import FastAPI, HTTPException
from mangum import Mangum
from src.application.usecases import MenuService, OrderService
from src.infrastructure.repositories import DynamoDBMenuRepository, DynamoDBOrderRepository
from .schemas import MenuResponse, CreateOrderRequest, OrderResponse

app = FastAPI(title="Coffee Order API")

# 의존성 주입
menu_repository = DynamoDBMenuRepository()
order_repository = DynamoDBOrderRepository()
menu_service = MenuService(menu_repository)
order_service = OrderService(order_repository, menu_repository)

@app.get("/menu", response_model=List[MenuResponse])
async def get_menus():
    try:
        menus = await menu_service.get_all_menus()
        return [
            MenuResponse(
                id=menu.id,
                name=menu.name,
                price=menu.price,
                category=menu.category
            )
            for menu in menus
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail="메뉴 목록을 가져오는데 실패했습니다.")

@app.post("/order", response_model=OrderResponse)
async def create_order(request: CreateOrderRequest):
    order = await order_service.create_order(
        customer_id=request.customer_id,
        menu_id=request.menu_id,
        quantity=request.quantity
    )
    
    if not order:
        raise HTTPException(
            status_code=400,
            detail="주문 생성에 실패했습니다. 메뉴가 존재하지 않거나 재고가 부족합니다."
        )
    
    return OrderResponse(
        id=order.id,
        status=order.status.value,
        created_at=order.created_at,
        updated_at=order.updated_at
    )

@app.get("/order/{order_id}", response_model=OrderResponse)
async def get_order(order_id: str):
    order = await order_service.get_order(order_id)
    if not order:
        raise HTTPException(
            status_code=404,
            detail="주문을 찾을 수 없습니다."
        )
    
    return OrderResponse(
        id=order.id,
        status=order.status.value,
        created_at=order.created_at,
        updated_at=order.updated_at
    )

handler = Mangum(app)