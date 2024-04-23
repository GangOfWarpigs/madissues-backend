from typing import Generic, TypeVar
from pydantic import BaseModel

SuccessResponse = TypeVar("SuccessResponse")


class Error(BaseModel):
    error_code: int
    error_message: str

    @staticmethod
    def of(message: str):
        return Error(error_code=0, error_message=message)


class Response(BaseModel, Generic[SuccessResponse]):
    error: Error | None = None
    success: SuccessResponse | None = None

    def is_error(self):
        return self.error is not None

    def is_success(self):
        return self.success is not None

    @staticmethod
    def fail(message: str) -> 'Response[SuccessResponse]':
        return Response(error=Error.of(message))

    @staticmethod
    def ok(payload: SuccessResponse) -> 'Response[SuccessResponse]':
        return Response(success=payload)
