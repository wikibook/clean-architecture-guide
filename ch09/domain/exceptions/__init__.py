import json


class OnlineCafeException(Exception):
    _CODE = "Undefined"
    _STATUS_CODE = 500
    _MESSAGE = "Undefined"
    _DESCRIPTION = "Unknown error"

    def __init__(self, debug_message=None):
        self._debug_message = debug_message
        super(OnlineCafeException, self).__init__(self.get_response_body())

    @classmethod
    def get_error_code(cls):
        return cls._CODE

    @classmethod
    def get_status_code(cls):
        return cls._STATUS_CODE

    def get_debug_message(self):
        return self._debug_message

    def get_error_message(self):
        return self._MESSAGE

    def get_response_body(self) -> str:
        return json.dumps(
            {
                "status": "failure",
                "errorCode": self._CODE,
                "message": self._MESSAGE,
                **({"debugMessage": self.get_debug_message()} if self._debug_message else {}),
            }
        )


# Client Error
class ClientError(OnlineCafeException):
    _MESSAGE = "Bad Request"
    _STATUS_CODE = 400
    _DESCRIPTION = "요청 에러"


class InvalidInputParameter(ClientError):
    _CODE = "1001"
    _DESCRIPTION = "유효하지 않은 입력 파라미터"


class MalformedRequestError(ClientError):
    _CODE = "1002"
    _DESCRIPTION = "요청 형식이 잘못된 경우"


# Server Error
class ServerError(OnlineCafeException):
    """HTTP 5xx Errors"""

    _MESSAGE = "Internal Server Error"
    _STATUS_CODE = 500
    _DESCRIPTION = "서버 에러"


class DatabaseSaveError(ServerError):
    _CODE = "1010"
    _DESCRIPTION = "데이터베이스 저장 실패"
