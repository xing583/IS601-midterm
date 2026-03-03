import os
import pytest

from app.calculator_config import CalculatorConfig
from app.exceptions import ConfigError


def test_default_config():
    config = CalculatorConfig.from_env()
    assert config.max_history_size > 0
    assert isinstance(config.auto_save, bool)
    assert config.default_encoding == "utf-8"


def test_custom_env(monkeypatch):
    monkeypatch.setenv("CALCULATOR_MAX_HISTORY_SIZE", "50")
    monkeypatch.setenv("CALCULATOR_AUTO_SAVE", "false")
    monkeypatch.setenv("CALCULATOR_PRECISION", "2")

    config = CalculatorConfig.from_env()

    assert config.max_history_size == 50
    assert config.auto_save is False
    assert config.precision == 2


def test_invalid_int(monkeypatch):
    monkeypatch.setenv("CALCULATOR_MAX_HISTORY_SIZE", "abc")

    with pytest.raises(ConfigError):
        CalculatorConfig.from_env()


def test_negative_history(monkeypatch):
    monkeypatch.setenv("CALCULATOR_MAX_HISTORY_SIZE", "-1")

    with pytest.raises(ConfigError):
        CalculatorConfig.from_env()


def test_negative_precision(monkeypatch):
    monkeypatch.setenv("CALCULATOR_PRECISION", "-5")

    with pytest.raises(ConfigError):
        CalculatorConfig.from_env()
