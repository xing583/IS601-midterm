import builtins
from pathlib import Path

import pandas as pd
import pytest

from app.calculator_repl import Calculator, CalculatorREPL
from app.exceptions import HistoryError


def test_calculator_autoload_success(tmp_path, monkeypatch):
    # create a valid history.csv
    p = tmp_path / "history.csv"
    df = pd.DataFrame(
        [{"timestamp": "t1", "operation": "add", "a": 1.0, "b": 2.0, "result": 3.0}]
    )
    df.to_csv(p, index=False)

    # run calculator in tmp_path so "history.csv" exists
    monkeypatch.chdir(tmp_path)

    c = Calculator(autoload=True, autosave_file="history.csv")
    assert len(c.history) == 1
    assert c.history.to_list()[0]["operation"] == "add"


def test_calculator_autoload_failure_is_ignored(tmp_path, monkeypatch):
    # create a bad history.csv (missing required columns) so load_csv raises HistoryError
    p = tmp_path / "history.csv"
    pd.DataFrame([{"bad": 1}]).to_csv(p, index=False)

    monkeypatch.chdir(tmp_path)

    # should NOT raise; the exception is swallowed in __init__
    c = Calculator(autoload=True, autosave_file="history.csv")
    # history remains empty because load failed
    assert len(c.history) == 0


def test_repl_run_exit(monkeypatch, capsys):
    # Make input() return "exit" then stop loop
    repl = CalculatorREPL(Calculator(autoload=False, autosave_file=None))

    inputs = iter(["exit"])
    monkeypatch.setattr(builtins, "input", lambda _: next(inputs))

    repl.run()
    out = capsys.readouterr().out
    assert "Enhanced Calculator" in out
    assert "Bye." in out


def test_repl_run_keyboard_interrupt(monkeypatch, capsys):
    repl = CalculatorREPL(Calculator(autoload=False, autosave_file=None))

    def raise_kb(_prompt):
        raise KeyboardInterrupt

    monkeypatch.setattr(builtins, "input", raise_kb)

    repl.run()
    out = capsys.readouterr().out
    assert "Enhanced Calculator" in out
    assert "Bye." in out


def test_repl_run_handles_calculator_error(monkeypatch, capsys):
    repl = CalculatorREPL(Calculator(autoload=False, autosave_file=None))

    # feed invalid line then exit
    inputs = iter(["unknown 1 2", "exit"])
    monkeypatch.setattr(builtins, "input", lambda _: next(inputs))

    repl.run()
    out = capsys.readouterr().out
    assert "Error:" in out
    assert "Bye." in out
