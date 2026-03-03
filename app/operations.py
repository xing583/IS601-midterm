from app.exceptions import (
    OperationNotSupportedError,
    DivisionByZeroError,
    InvalidInputError,
)


class Operation:
    """Base class for all operations."""

    name = ""

    def execute(self, a, b):
        raise NotImplementedError


class AddOperation(Operation):
    name = "add"

    def execute(self, a, b):
        return a + b


class SubtractOperation(Operation):
    name = "subtract"

    def execute(self, a, b):
        return a - b


class MultiplyOperation(Operation):
    name = "multiply"

    def execute(self, a, b):
        return a * b


class DivideOperation(Operation):
    name = "divide"

    def execute(self, a, b):
        if b == 0:
            raise DivisionByZeroError("Cannot divide by zero")
        return a / b


class PowerOperation(Operation):
    name = "power"

    def execute(self, a, b):
        return a ** b


class RootOperation(Operation):
    name = "root"

    def execute(self, a, b):
        if b == 0:
            raise InvalidInputError("Root degree cannot be zero")
        if a < 0:
            raise InvalidInputError("Cannot take root of negative number")
        return a ** (1 / b)


# Factory Pattern
class OperationFactory:
    """Factory to create operation instances."""

    _operations = {
        "add": AddOperation,
        "subtract": SubtractOperation,
        "multiply": MultiplyOperation,
        "divide": DivideOperation,
        "power": PowerOperation,
        "root": RootOperation,
    }

    @classmethod
    def create(cls, operation_name: str) -> Operation:
        operation_name = operation_name.lower()

        if operation_name not in cls._operations:
            raise OperationNotSupportedError(
                f"Operation '{operation_name}' is not supported"
            )

        return cls._operations[operation_name]()
