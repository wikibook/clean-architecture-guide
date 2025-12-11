from .controllers import CalculateScoreController
from .usecase import CalculateAverageUseCase
from .presenter import ConsolePresenter
from .repository import DdbScoreRepository


def initialize_application() -> CalculateScoreController:
    # Repository와 Presenter 초기화
    repository = DdbScoreRepository()
    presenter = ConsolePresenter()

    # 유스케이스 초기화
    usecase = CalculateAverageUseCase(repository, presenter)

    # 컨트롤러 초기화
    controller = CalculateScoreController(usecase)
    return controller
