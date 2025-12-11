from ..domain.usecases.menu_usecases import MenuUseCases
from ..domain.usecases.order_usecases import OrderUseCases
from ..infrastructure.repositories.dynamodb_repositories import (
    DynamoDBMenuRepository,
    DynamoDBOrderRepository
)
from ..infrastructure.presenters.json_presenter import JSONPresenter
from ..application.controllers.menu_controller import MenuController
from ..application.controllers.order_controller import OrderController

class Dependencies:
    """의존성 주입 컨테이너"""
    
    @staticmethod
    def configure():
        """의존성 설정"""
        # 레포지토리 생성
        menu_repository = DynamoDBMenuRepository()
        order_repository = DynamoDBOrderRepository()

        # 프레젠터 생성
        presenter = JSONPresenter()

        # 유스케이스 생성
        menu_usecase = MenuUseCases(menu_repository)
        order_usecase = OrderUseCases(
            order_repository=order_repository,
            menu_repository=menu_repository
        )

        # 컨트롤러 생성
        menu_controller = MenuController(
            menu_usecase=menu_usecase,
            presenter=presenter
        )
        order_controller = OrderController(
            order_usecase=order_usecase,
            presenter=presenter
        )

        return menu_controller, order_controller