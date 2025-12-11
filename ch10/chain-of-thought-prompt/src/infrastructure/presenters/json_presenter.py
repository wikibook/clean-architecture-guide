from typing import Any
from ...domain.interfaces.boundaries import OutputBoundary, ResponseDTO

class JSONPresenter(OutputBoundary):
    def present_success(self, data: Any, message: str) -> ResponseDTO:
        """성공 응답 생성"""
        return ResponseDTO(
            status="success",
            data=data,
            message=message
        )

    def present_error(self, message: str) -> ResponseDTO:
        """에러 응답 생성"""
        return ResponseDTO(
            status="error",
            data=None,
            message=message
        )