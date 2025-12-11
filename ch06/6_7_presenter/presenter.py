# Presenters Layer
from abc import ABC, abstractmethod
from typing import Any
from .viewmodels import ScoreViewModel


# 출력 인터페이스 (Presenter)
class OutputBoundary(ABC):
    @abstractmethod
    def set_result(self, output_dto) -> None:
        pass

    @abstractmethod
    def present(self) -> Any:
        pass


class ScorePresenter(OutputBoundary):
    def __init__(self, view):
        self.view = view
        self.output_dto = None

    def set_result(self, output_dto):
        self.output_dto = output_dto

    def present(self) -> Any:
        if not self.output_dto:
            raise ValueError("No result to present")

        # 등급 계산
        grade = "A" if self.output_dto.average >= 90 else "B" if self.output_dto.average >= 80 else "C"

        # ViewModel 생성
        view_model = ScoreViewModel(
            student_id=self.output_dto.student_id,
            average=f"{self.output_dto.average:.2f}점",
            status="성공" if self.output_dto.status == "success" else "실패",
            grade=grade,
        )

        # View를 통해 표시
        return self.view.display(view_model)
