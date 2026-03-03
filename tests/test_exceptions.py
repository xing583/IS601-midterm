import pytest

from app.exceptions import (
    CalculatorError,
    InvalidInputError,
    OperationNotSupportedError,
    DivisionByZeroError,
    ConfigError,
    HistoryError,
)


@pytest.mark.parametrize(
    "exc_type",
    [
        CalculatorError,
        InvalidInputError,
        OperationNotSupportedError,
        DivisionByZeroError,
        ConfigError,
        HistoryError,
    ],
)
def test_exceptions_are_exceptions(exc_type):
    assert issubclass(exc_type, Exception)


@pytest.mark.parametrize(
    "child",
    [
        InvalidInputError,
        OperationNotSupportedError,
        DivisionByZeroError,
        ConfigError,
        HistoryError,
    ],
)
def test_exceptions_inherit_from_calculator_error(child):
    assert issubclass(child, CalculatorError)


def test_raise_and_catch_custom_exception():
    with pytest.raises(InvalidInputError):
        raise InvalidInputError("bad input")
