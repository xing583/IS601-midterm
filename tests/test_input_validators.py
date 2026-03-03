import pytest

from app.input_validators import validate_number, validate_operation
from app.exceptions import InvalidInputError, OperationNotSupportedError


@pytest.mark.parametrize("op", ["add", "Subtract", " MULTIPLY ", "divide", "power", "root"])
def test_validate_operation_success(op):
    assert validate_operation(op) in {"add", "subtract", "multiply", "divide", "power", "root"}


@pytest.mark.parametrize("op", ["", "   ", "mod", "sqrt", None])
def test_validate_operation_fail(op):
    with pytest.raises(OperationNotSupportedError):
        validate_operation(op)


@pytest.mark.parametrize("value,expected", [("3", 3.0), ("3.5", 3.5), ("-2", -2.0), (5, 5.0)])
def test_validate_number_success(value, expected):
    assert validate_number(value, max_value=1e6) == expected


@pytest.mark.parametrize("value", ["", "   ", "abc", None])
def test_validate_number_fail_invalid(value):
    with pytest.raises(InvalidInputError):
        validate_number(value, max_value=1e6)


def test_validate_number_out_of_range():
    with pytest.raises(InvalidInputError):
        validate_number("10000000", max_value=10)
