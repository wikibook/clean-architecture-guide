from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from mangum import Mangum

from .config.database import get_db
from .config.dependencies import Dependencies


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    # Startup: Register routes
    db = next(get_db())
    menu_controller, order_controller, customer_controller = Dependencies.configure(db)
    app.include_router(menu_controller.register_routes())
    app.include_router(order_controller.register_routes())
    app.include_router(customer_controller.register_routes())
    yield
    # Shutdown: Clean up resources
    db.close()


app = FastAPI(
    title="Coffee Order API",
    lifespan=lifespan,
)

# AWS Lambda handler
handler = Mangum(app)
