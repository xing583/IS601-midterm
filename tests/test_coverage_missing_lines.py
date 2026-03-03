import builtins
import pandas as pd
import pytest

from app.calculator_repl import Calculator, CalculatorREPL
from app.history import History


def test_calculator_autosave_line_covered(tmp_path, monkeypatch):
    """
    Cover calculator_repl.py line 61:
    if auto_save and autosave_file -> self.save(self.autosave_file)
    """
    monkeypatch.chdir(tmp_path)
    calc = Calculator(autoload=False, autosave_file="history.csv")
    # Ensure autosave is on (default True; but make explicit)
    calc.config.auto_save = True

    result = calc.calculate("add", 1, 2)
    assert result in {3, 3.0}

    # autosave_file should be created
    assert (tmp_path / "history.csv").exists()


def test_repl_run_print_output_branch(monkeypatch, capsys):
    """
    Cover calculator_repl.py lines 190-191:
    if out: print(out)
    We feed: 'help' (prints lots of text) then 'exit'.
    """
    repl = CalculatorREPL(Calculator(autoload=False, autosave_file=None))

    inputs = iter(["help", "exit"])
    monkeypatch.setattr(builtins, "input", lambda _: next(inputs))

    repl.run()
    out = capsys.readouterr().out
    assert "Commands:" in out  # printed help_text
    assert "Bye." in out


def test_history_load_truncation_branch(tmp_path):
    """
    Cover history.py line 101:
    if len(df) > max_size: truncate with iloc[-max_size:]
    """
    p = tmp_path / "history.csv"

    # Create 5 rows but max_size=2 -> should truncate to last 2 rows
    df = pd.DataFrame(
        [
            {"timestamp": "t1", "operation": "add", "a": 1.0, "b": 1.0, "result": 2.0},
            {"timestamp": "t2", "operation": "add", "a": 2.0, "b": 2.0, "result": 4.0},
            {"timestamp": "t3", "operation": "add", "a": 3.0, "b": 3.0, "result": 6.0},
            {"timestamp": "t4", "operation": "add", "a": 4.0, "b": 4.0, "result": 8.0},
            {"timestamp": "t5", "operation": "add", "a": 5.0, "b": 5.0, "result": 10.0},
        ]
    )
    df.to_csv(p, index=False)

    h = History(max_size=2)
    h.load_csv(str(p))

    rows = h.to_list()
    assert len(rows) == 2
    assert rows[0]["timestamp"] == "t4"
    assert rows[1]["timestamp"] == "t5"
