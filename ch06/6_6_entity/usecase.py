from dataclasses import dataclass
from abc import ABC, abstractmethod

from .repository import ScoreRepository
from .presenter import OutputBoundary
from .entity import Student, Scores, StandardScoreValidationPolicy


# 입력 DTO
@dataclass
class ScoreInputDTO:
    student_id: str


# 출력 DTO
@dataclass
class ScoreOutputDTO:
    student_id: str
    average: float
    status: str


# 유스케이스 인터페이스
class InputBoundary(ABC):
    @abstractmethod
    def execute(self, input_dto: ScoreInputDTO) -> None:
        pass


# 유스케이스 구현 (Entity 활용)
class CalculateAverageUseCase(InputBoundary):
    def __init__(self, repository: ScoreRepository, presenter: OutputBoundary):
        self.repository = repository
        self.presenter = presenter

    def execute(self, input_dto: ScoreInputDTO) -> None:
        try:
            # 저장소에서 성적 데이터 조회
            raw_scores = self.repository.get_scores(input_dto.student_id)

            # Entity 생성 및 비즈니스 로직 적용
            validation_policy = StandardScoreValidationPolicy()
            scores_entity = Scores(values=raw_scores, validation_policy=validation_policy)

            # Student Entity 생성
            student = Student(student_id=input_dto.student_id, scores=scores_entity)

            # Entity를 통한 유효성 검증
            student.validate_scores()

            # Entity를 통한 평균 계산
            average = student.get_average_score()

            # 출력 DTO 생성
            output_dto = ScoreOutputDTO(student_id=input_dto.student_id, average=average, status="success")

            # 프레젠터로 결과 전달
            self.presenter.set_result(output_dto)

        except ValueError as e:
            output_dto = ScoreOutputDTO(student_id=input_dto.student_id, average=0.0, status=f"error: {str(e)}")
            self.presenter.set_result(output_dto)
