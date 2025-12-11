from .controllers import CalculateScoreController
from .usecase import CalculateAverageUseCase
from .presenter import ScorePresenter
from .views import WebScoreView, ApiScoreView
from .repository import DdbScoreRepository
from .infrastructure import DynamoDBClient


def initialize_application() -> CalculateScoreController:
    """기본 API 형식(JSON) 응답용 애플리케이션 초기화"""
    # 인프라스트럭쳐 초기화
    dynamodb_client = DynamoDBClient(region="ap-northeast-2")

    # 인터페이스 어댑터 초기화
    repository = DdbScoreRepository(dynamodb_client)
    presenter = ScorePresenter(ApiScoreView())  # 기본 API 형식

    # 유스케이스 초기화
    usecase = CalculateAverageUseCase(repository, presenter)

    # 컨트롤러 초기화
    controller = CalculateScoreController(usecase)
    return controller


def initialize_web_application() -> CalculateScoreController:
    """Web 형식 응답용 애플리케이션 초기화"""
    # 인프라스트럭쳐 초기화
    dynamodb_client = DynamoDBClient(region="ap-northeast-2")

    # 인터페이스 어댑터 초기화
    repository = DdbScoreRepository(dynamodb_client)
    presenter = ScorePresenter(WebScoreView())  # Web 형식

    # 유스케이스 초기화
    usecase = CalculateAverageUseCase(repository, presenter)

    # 컨트롤러 초기화
    controller = CalculateScoreController(usecase)
    return controller
