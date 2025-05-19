# utils/json_response.py
from typing import Any, Mapping, MutableMapping, Optional

from django.http import JsonResponse


class ApiResponse(JsonResponse):
    """
    Standardized JSON wrapper.

    Usage:
        return ApiResponse.ok(data={"id": 123}, message="Created")
        return ApiResponse.error(message="Invalid ID", errors={"id": "Not found"}, status=404)
    """

    def __init__(
        self,
        *,
        success: bool,
        message: str,
        data: Optional[Mapping[str, Any]] = None,
        errors: Optional[Mapping[str, Any]] = None,
        status: int = 200,
        **kwargs,
    ):
        payload: MutableMapping[str, Any] = {
            "success": success,
            "message": message,
        }
        if data is not None:
            payload["data"] = data
        if errors is not None:
            payload["errors"] = errors

        super().__init__(payload, status=status, **kwargs)

    # -------- Convenience constructors ----------------------------------
    @classmethod
    def ok(
        cls,
        *,
        data: Optional[Mapping[str, Any]] = None,
        message: str = "Success",
        status: int = 200,
    ) -> "ApiResponse":
        return cls(success=True, message=message, data=data, status=status)

    @classmethod
    def error(
        cls,
        *,
        message: str = "Error",
        errors: Optional[Mapping[str, Any]] = None,
        status: int = 400,
    ) -> "ApiResponse":
        return cls(success=False, message=message, errors=errors, status=status)
