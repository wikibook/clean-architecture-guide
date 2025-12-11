from typing import Tuple

from sqlalchemy.orm import Session

from ..domain.repositories.customer_repository import CustomerRepository
from ..domain.repositories.menu_repository import MenuRepository
from ..domain.repositories.order_repository import OrderRepository
from ..domain.usecases.customer_usecases import (
    GetCustomerUseCase,
    GetCustomerUseCaseImpl,
)
from ..domain.usecases.menu_usecases import GetMenuListUseCase, GetMenuListUseCaseImpl
from ..domain.usecases.order_usecases import (
    CreateOrderUseCase,
    CreateOrderUseCaseImpl,
    DeleteOrderUseCase,
    DeleteOrderUseCaseImpl,
    GetOrderStatusUseCase,
    GetOrderStatusUseCaseImpl,
)
from ..infrastructure.repositories.mysql_customer_repository import (
    MySQLCustomerRepository,
)
from ..infrastructure.repositories.mysql_menu_repository import MySQLMenuRepository
from ..infrastructure.repositories.mysql_order_repository import MySQLOrderRepository
from ..presentation.controllers.customer_controller import CustomerController
from ..presentation.controllers.menu_controller import MenuController
from ..presentation.controllers.order_controller import OrderController


class Dependencies:
    @staticmethod
    def configure(
        db: Session,
    ) -> Tuple[MenuController, OrderController, CustomerController]:
        # Repositories
        menu_repository: MenuRepository = MySQLMenuRepository(db)
        order_repository: OrderRepository = MySQLOrderRepository(db)
        customer_repository: CustomerRepository = MySQLCustomerRepository(db)

        # Usecases
        get_menu_list_usecase: GetMenuListUseCase = GetMenuListUseCaseImpl(
            menu_repository=menu_repository
        )
        create_order_usecase: CreateOrderUseCase = CreateOrderUseCaseImpl(
            order_repository=order_repository,
            menu_repository=menu_repository,
        )
        get_order_status_usecase: GetOrderStatusUseCase = GetOrderStatusUseCaseImpl(
            order_repository=order_repository
        )
        delete_order_usecase: DeleteOrderUseCase = DeleteOrderUseCaseImpl(
            order_repository=order_repository
        )
        get_customer_usecase: GetCustomerUseCase = GetCustomerUseCaseImpl(
            customer_repository=customer_repository
        )

        # Controllers
        menu_controller = MenuController(get_menu_list_usecase=get_menu_list_usecase)
        order_controller = OrderController(
            create_order_usecase=create_order_usecase,
            get_order_status_usecase=get_order_status_usecase,
            delete_order_usecase=delete_order_usecase,
        )
        customer_controller = CustomerController(
            get_customer_usecase=get_customer_usecase
        )

        return menu_controller, order_controller, customer_controller
