from __future__ import annotations

from app.exceptions import InvalidInputError, OperationNotSupportedError
from app.operations import OperationFactory


def validate_operation(op: str) -> str:
    """
    LBYL: Look Before You Leap.
    Validate operation name before using it.
    Dynamically checks OperationFactory so new operations are automatically supported.
    """
    if op is None:
        raise OperationNotSupportedError("Operation is required")

    op = str(op).strip().lower()
    if not op:
        raise OperationNotSupportedError("Operation is required")

    if op not in OperationFactory._operations:
        raise OperationNotSupportedError(f"Unsupported operation: {op}")

    return op


def validate_number(value, max_value: float = 1e6) -> float:
    """
    LBYL: Validate the input can be converted to float and within allowed range.
    """
    if value is None:
        raise InvalidInputError("Number is required")

    s = str(value).strip()
    if not s:
        raise InvalidInputError("Number is required")

    try:
        num = float(s)
    except ValueError as e:
        raise InvalidInputError(f"Invalid number: {value}") from e

    if abs(num) > float(max_value):
        raise InvalidInputError(f"Number out of range: {num}")

    return num
