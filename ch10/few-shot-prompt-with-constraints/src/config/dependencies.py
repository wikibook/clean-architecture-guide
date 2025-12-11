from ..domain.usecases.menu_usecases import GetMenusUseCase
from ..domain.usecases.order_usecases import CreateOrderUseCase, GetOrderUseCase
from ..infrastructure.repositories.dynamodb_repositories import (
    DynamoDBMenuRepository, DynamoDBOrderRepository
)
from ..infrastructure.presenters.json_presenter import JSONPresenter
from ..application.controllers.menu_controller import MenuController
from ..application.controllers.order_controller import OrderController


def create_menu_controller() -> MenuController:
    menu_repository = DynamoDBMenuRepository()
    presenter = JSONPresenter()
    get_menus_usecase = GetMenusUseCase(menu_repository)
    
    return MenuController(
        get_menus_usecase=get_menus_usecase,
        presenter=presenter
    )


def create_order_controller() -> OrderController:
    menu_repository = DynamoDBMenuRepository()
    order_repository = DynamoDBOrderRepository()
    presenter = JSONPresenter()
    
    create_order_usecase = CreateOrderUseCase(
        order_repository=order_repository,
        menu_repository=menu_repository
    )
    get_order_usecase = GetOrderUseCase(
        order_repository=order_repository
    )
    
    return OrderController(
        create_order_usecase=create_order_usecase,
        get_order_usecase=get_order_usecase,
        presenter=presenter
    )