from abc import ABCMeta, abstractmethod

from application.dtos import InputDto


class InputBoundary(metaclass=ABCMeta):
    @abstractmethod
    def execute(self, input_dto: InputDto) -> None:
        pass


class CreateOrderInputBoundary(InputBoundary):
    pass
