from dataclasses import Field
from typing import Generic, TypeVar
from pydantic import BaseModel

SuccessResponse = TypeVar("SuccessResponse")


class Error(BaseModel):
    error_code: int
    error_message: str
    error_field: list[str] = []

    @staticmethod
    def of(message: str, code: int | None = 0):
        return Error(error_code=code, error_message=message, error_field=[])

    @staticmethod
    def field(message: str, field: list[str]):
        return Error(error_code=1, error_message=message, error_field=field)


class Response(BaseModel, Generic[SuccessResponse]):
    error: Error | None = None
    success: SuccessResponse | None = None

    def is_error(self) -> bool:
        return self.error is not None

    def is_success(self) -> bool:
        return self.success is not None

    @staticmethod
    def fail(message: str, code : int | None = 0) -> 'Response[SuccessResponse]':
        return Response(error=Error.of(message, code=code), success=None)

    @staticmethod
    def field_fail(message: str, field: list[str]) -> 'Response[SuccessResponse]':
        return Response(error=Error.field(message, field), success=None)

    @staticmethod
    def ok(payload: SuccessResponse) -> 'Response[SuccessResponse]':
        return Response(success=payload, error=None)
