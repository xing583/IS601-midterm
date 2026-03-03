import pytest

from app.calculator_repl import Calculator, CalculatorREPL
from app.exceptions import InvalidInputError, CalculatorError


def make_repl():
    # IMPORTANT: isolate tests from real history.csv on disk
    calc = Calculator(autoload=False, autosave_file=None)
    return CalculatorREPL(calc)


def test_help_text():
    repl = make_repl()
    out = repl.run_once("help")
    assert "Commands:" in out
    assert "Operations:" in out


def test_empty_input_returns_empty_string():
    repl = make_repl()
    assert repl.run_once("") == ""
    assert repl.run_once("   ") == ""


def test_history_empty():
    repl = make_repl()
    assert repl.run_once("history") == "No history."


def test_calculation_and_history():
    repl = make_repl()
    out = repl.run_once("add 1 2")
    assert out in {"3", "3.0"}
    hist = repl.run_once("history")
    assert "add" in hist


def test_clear_history():
    repl = make_repl()
    repl.run_once("add 1 2")
    assert "add" in repl.run_once("history")
    assert repl.run_once("clear") == "History cleared."
    assert repl.run_once("history") == "No history."


def test_undo_redo_messages_and_effect():
    repl = make_repl()

    repl.run_once("add 1 2")
    assert "add" in repl.run_once("history")

    # undo should remove last record (restore prior df)
    assert repl.run_once("undo") == "Undo OK."
    assert repl.run_once("history") == "No history."

    # redo should bring it back
    assert repl.run_once("redo") == "Redo OK."
    assert "add" in repl.run_once("history")


def test_save_and_load(tmp_path):
    repl = make_repl()
    repl.run_once("add 1 2")

    p = tmp_path / "h.csv"
    assert repl.run_once(f"save {p}") == "Saved."

    repl.run_once("clear")
    assert repl.run_once("history") == "No history."

    assert repl.run_once(f"load {p}") == "Loaded."
    assert "add" in repl.run_once("history")


@pytest.mark.parametrize("line", ["save", "save a b", "load", "load a b", "add 1", "add 1 2 3"])
def test_usage_errors(line):
    repl = make_repl()
    with pytest.raises(InvalidInputError):
        repl.run_once(line)


def test_exit_marker():
    repl = make_repl()
    assert repl.run_once("exit") == "__EXIT__"


def test_unknown_operation_is_error():
    repl = make_repl()
    with pytest.raises(CalculatorError):
        repl.run_once("unknown 1 2")
