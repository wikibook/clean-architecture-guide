from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from mangum import Mangum
from .config.dependencies import create_menu_controller, create_order_controller
from typing import Dict, Any

app = FastAPI()

menu_controller = create_menu_controller()
order_controller = create_order_controller()


@app.get("/menus")
async def get_menus():
    response = await menu_controller.get_menus()
    return JSONResponse(
        status_code=200 if response.status == "success" else 500,
        content=response.__dict__
    )


@app.post("/orders")
async def create_order(request: Request):
    body = await request.json()
    response = await order_controller.create_order(
        customer_id=body["customer_id"],
        menu_id=body["menu_id"],
        quantity=body["quantity"],
        options=body.get("options", {})
    )
    
    status_code = 201 if response.status == "success" else (
        404 if response.message == "Invalid menu ID" else
        400 if response.message == "Insufficient stock" else 500
    )
    
    return JSONResponse(
        status_code=status_code,
        content=response.__dict__
    )


@app.get("/orders/{order_id}")
async def get_order(order_id: str):
    response = await order_controller.get_order(order_id)
    
    status_code = 200 if response.status == "success" else (
        404 if response.message == "Order not found" else 500
    )
    
    return JSONResponse(
        status_code=status_code,
        content=response.__dict__
    )


handler = Mangum(app)