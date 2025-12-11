from unittest.mock import Mock
from calculate_average_usecase import (
    ScoreRepository,
    OutputBoundary,
    CalculateAverageUseCase,
    ScoreInputDTO,
    ScoreOutputDTO,
)

# 테스트용 모의 객체
mock_repository = Mock(spec=ScoreRepository)
mock_repository.get_scores.return_value = [90.0, 85.0, 95.0]
mock_presenter = Mock(spec=OutputBoundary)

# 유스케이스 테스트
usecase = CalculateAverageUseCase(mock_repository, mock_presenter)
usecase.execute(ScoreInputDTO(student_id="123"))

# 결과 검증
mock_presenter.set_result.assert_called_with(ScoreOutputDTO(student_id="123", average=90.00, status="success"))
