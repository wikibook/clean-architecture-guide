from abc import ABCMeta, abstractmethod

from application.dtos import OutputDto


class OutputBoundary(metaclass=ABCMeta):
    @abstractmethod
    def set_result(self, output_dto: OutputDto) -> None:
        pass

    @abstractmethod
    def present(self) -> dict:
        pass
