from .controllers import CalculateScoreController
from .usecase import CalculateAverageUseCase
from .presenter import ConsolePresenter
from .repository import DdbScoreRepository
from .infrastructure import DynamoDBClient


def initialize_application() -> CalculateScoreController:
    # 인프라스트럭쳐 초기화
    dynamodb_client = DynamoDBClient(region="ap-northeast-2")

    # 인터페이스 어댑터 초기화
    repository = DdbScoreRepository(dynamodb_client)
    presenter = ConsolePresenter()

    # 유스케이스 초기화
    usecase = CalculateAverageUseCase(repository, presenter)

    # 컨트롤러 초기화
    controller = CalculateScoreController(usecase)
    return controller
