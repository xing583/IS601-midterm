"""
Custom exception hierarchy for the calculator application.
"""


class CalculatorError(Exception):
    """Base exception for all calculator-related errors."""


class InvalidInputError(CalculatorError):
    """Raised when user input cannot be parsed or violates validation rules."""


class OperationNotSupportedError(CalculatorError):
    """Raised when an unknown/unsupported operation is requested."""


class DivisionByZeroError(CalculatorError):
    """Raised when attempting to divide by zero."""


class ConfigError(CalculatorError):
    """Raised when configuration is invalid or cannot be loaded."""


class HistoryError(CalculatorError):
    """Raised when history operations fail (e.g., undo/redo empty)."""
