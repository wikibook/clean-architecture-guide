from abc import ABC, abstractmethod
from typing import Any


# 출력 인터페이스 (Presenter)
class OutputBoundary(ABC):
    @abstractmethod
    def set_result(self, output_dto) -> None:
        pass

    @abstractmethod
    def present(self) -> Any:
        pass


class ConsolePresenter(OutputBoundary):
    def __init__(self):
        self.contents = {}

    def set_result(self, output_dto: "ScoreOutputDTO"):
        self.contents = {
            "student_id": output_dto.student_id,
            "average": output_dto.average,
            "status": output_dto.status,
        }

    def present(self) -> Any:
        return self.contents
