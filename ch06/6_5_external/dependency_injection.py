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


def initialize_test_application() -> CalculateScoreController:
    """테스트용 애플리케이션 초기화 (Mock 사용)"""
    from .test_mocks import MockDynamoDBClient, MockScoreRepository

    # Infrastructure Layer 초기화 (Mock)
    mock_dynamodb_client = MockDynamoDBClient()

    # Interface Adapters Layer 초기화 (Mock)
    mock_repository = MockScoreRepository()
    presenter = ConsolePresenter()

    # Use Cases Layer 초기화
    usecase = CalculateAverageUseCase(mock_repository, presenter)

    # Controllers Layer 초기화
    controller = CalculateScoreController(usecase)
    return controller
