from dataclasses import dataclass
from typing import List
from abc import ABC, abstractmethod


# 저장소 인터페이스
class ScoreRepository(ABC):
    @abstractmethod
    def get_scores(self, student_id: str) -> List[float]:
        pass


# 출력 인터페이스 (Presenter)
class OutputBoundary(ABC):
    @abstractmethod
    def set_result(self, output_dto: "ScoreOutputDTO") -> None:
        pass

    @abstractmethod
    def present(self) -> None:
        pass


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


# 유스케이스 구현
class CalculateAverageUseCase(InputBoundary):
    def __init__(self, repository: ScoreRepository, presenter: OutputBoundary):
        self.repository = repository
        self.presenter = presenter

    def execute(self, input_dto: ScoreInputDTO) -> None:
        try:
            # 저장소에서 성적 데이터 조회
            scores = self.repository.get_scores(input_dto.student_id)

            # 비즈니스 로직: 평균 계산
            average = sum(scores) / len(scores) if scores else 0.0

            # 출력 DTO 생성
            output_dto = ScoreOutputDTO(student_id=input_dto.student_id, average=average, status="success")

            # 프레젠터로 결과 전달
            self.presenter.set_result(output_dto)

        except ValueError as e:
            output_dto = ScoreOutputDTO(student_id=input_dto.student_id, average=0.0, status=f"error: {str(e)}")
            self.presenter.set_result(output_dto)
