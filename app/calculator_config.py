import os
from dotenv import load_dotenv

from app.exceptions import ConfigError


class CalculatorConfig:
    """Configuration loader using environment variables."""

    def __init__(
        self,
        max_history_size: int = 100,
        auto_save: bool = True,
        default_encoding: str = "utf-8",
        precision: int = 4,
        max_input_value: float = 1e6,
    ):
        self.max_history_size = max_history_size
        self.auto_save = auto_save
        self.default_encoding = default_encoding
        self.precision = precision
        self.max_input_value = max_input_value

    @classmethod
    def from_env(cls):
        """Load configuration from .env file."""
        load_dotenv()

        try:
            max_history_size = int(os.getenv("CALCULATOR_MAX_HISTORY_SIZE", 100))
            auto_save = os.getenv("CALCULATOR_AUTO_SAVE", "true").lower() == "true"
            default_encoding = os.getenv("CALCULATOR_DEFAULT_ENCODING", "utf-8")
            precision = int(os.getenv("CALCULATOR_PRECISION", 4))
            max_input_value = float(os.getenv("CALCULATOR_MAX_INPUT_VALUE", 1e6))

            if max_history_size <= 0:
                raise ConfigError("max_history_size must be positive")

            if precision < 0:
                raise ConfigError("precision must be non-negative")

        except ValueError as e:
            raise ConfigError(f"Invalid configuration value: {e}")

        return cls(
            max_history_size=max_history_size,
            auto_save=auto_save,
            default_encoding=default_encoding,
            precision=precision,
            max_input_value=max_input_value,
        )
