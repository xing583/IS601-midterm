import pytest

from app.operations import OperationFactory
from app.exceptions import (
    OperationNotSupportedError,
    DivisionByZeroError,
    InvalidInputError,
)


@pytest.mark.parametrize(
    "op,a,b,expected",
    [
        ("add", 1, 2, 3),
        ("subtract", 5, 3, 2),
        ("multiply", 2, 3, 6),
        ("divide", 6, 2, 3),
        ("power", 2, 3, 8),
        ("root", 9, 2, 3),
    ],
)
def test_operations(op, a, b, expected):
    operation = OperationFactory.create(op)
    result = operation.execute(a, b)
    assert result == expected


def test_divide_by_zero():
    op = OperationFactory.create("divide")
    with pytest.raises(DivisionByZeroError):
        op.execute(5, 0)


def test_invalid_operation():
    with pytest.raises(OperationNotSupportedError):
        OperationFactory.create("unknown")


def test_invalid_root():
    op = OperationFactory.create("root")
    with pytest.raises(InvalidInputError):
        op.execute(-1, 2)


def test_root_degree_zero():
    op = OperationFactory.create("root")
    with pytest.raises(InvalidInputError):
        op.execute(9, 0)

def test_base_operation_execute_not_implemented():
    from app.operations import Operation

    op = Operation()
    try:
        op.execute(1, 2)
        assert False, "Expected NotImplementedError"
    except NotImplementedError:
        assert True
