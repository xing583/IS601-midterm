from __future__ import annotations

from pathlib import Path
from typing import Optional

from app.calculation import Calculation
from app.calculator_config import CalculatorConfig
from app.calculator_memento import HistoryCaretaker
from app.exceptions import CalculatorError, InvalidInputError
from app.history import History
from app.input_validators import validate_number, validate_operation
from app.operations import OperationFactory


class Calculator:
    """
    Facade Pattern:
    A single high-level interface that coordinates config, operations, history (pandas),
    and memento (undo/redo).

    autoload/autosave_file make the class test-friendly (avoid reading/writing real files).
    """

    def __init__(
        self,
        config: Optional[CalculatorConfig] = None,
        *,
        autoload: bool = True,
        autosave_file: Optional[str] = "history.csv",
    ):
        self.config = config or CalculatorConfig.from_env()
        self.history = History(max_size=self.config.max_history_size)
        self.caretaker = HistoryCaretaker()
        self.autosave_file = autosave_file

        # Auto-load existing history upon start (assignment requirement)
        if autoload and self.autosave_file:
            path = Path(self.autosave_file)
            if path.exists():
                try:
                    self.history.load_csv(str(path), encoding=self.config.default_encoding)
                except CalculatorError:  # pragma: no cover
                    # Keep app usable even if file is corrupted
                    pass  # pragma: no cover

    def calculate(self, op_name: str, a: float, b: float) -> float:
        # Save current state for undo before changing history
        self.caretaker.save(self.history.df)

        operation = OperationFactory.create(op_name)
        result = operation.execute(a, b)

        # Apply precision rule
        result = round(float(result), self.config.precision)

        calc = Calculation.create(op_name, float(a), float(b), result)
        self.history.add_record(calc.timestamp, calc.operation, calc.a, calc.b, calc.result)

        # Auto-save if enabled
        if self.config.auto_save and self.autosave_file:
            self.save(self.autosave_file)

        return result

    def clear(self) -> None:
        self.caretaker.save(self.history.df)
        self.history.clear()

    def undo(self) -> None:
        self.history._df = self.caretaker.undo(self.history.df)

    def redo(self) -> None:
        self.history._df = self.caretaker.redo(self.history.df)

    def save(self, filename: str) -> None:
        self.history.save_csv(filename, encoding=self.config.default_encoding)

    def load(self, filename: str) -> None:
        self.caretaker.save(self.history.df)
        self.history.load_csv(filename, encoding=self.config.default_encoding)


class CalculatorREPL:
    """
    REPL Interface:
    - Commands: help/history/clear/undo/redo/save/load/exit
    - Operations: add/subtract/multiply/divide/power/root
    - EAFP style error handling: try/except in run()
    """

    def __init__(self, calculator: Optional[Calculator] = None):
        self.calculator = calculator or Calculator()

    def help_text(self) -> str:
        return (
            "Enhanced Calculator (Module 5)\n"
            "\n"
            "Commands:\n"
            "  help                 Show this help\n"
            "  history              Show calculation history\n"
            "  clear                Clear history\n"
            "  undo                 Undo last change\n"
            "  redo                 Redo last undone change\n"
            "  save <file.csv>      Save history to CSV\n"
            "  load <file.csv>      Load history from CSV\n"
            "  exit                 Exit the calculator\n"
            "\n"
            "Operations:\n"
            "  add a b | subtract a b | multiply a b | divide a b | power a b | root a b\n"
            "\n"
            "Examples:\n"
            "  add 1 2\n"
            "  divide 10 5\n"
            "  power 2 3\n"
            "  root 9 2\n"
        )

    def run_once(self, line: str) -> str:
        """
        Run a single line and return output string.
        This design makes it easy to test (unit tests can call run_once()).
        """
        line = (line or "").strip()
        if not line:
            return ""

        parts = line.split()
        cmd = parts[0].lower()

        # Built-in commands
        if cmd == "help":
            return self.help_text()

        if cmd == "history":
            rows = self.calculator.history.to_list()
            if not rows:
                return "No history."
            return "\n".join(
                f'{r["timestamp"]} {r["operation"]} {r["a"]} {r["b"]} = {r["result"]}'
                for r in rows
            )

        if cmd == "clear":
            self.calculator.clear()
            return "History cleared."

        if cmd == "undo":
            self.calculator.undo()
            return "Undo OK."

        if cmd == "redo":
            self.calculator.redo()
            return "Redo OK."

        if cmd == "save":
            if len(parts) != 2:
                raise InvalidInputError("Usage: save <file.csv>")
            self.calculator.save(parts[1])
            return "Saved."

        if cmd == "load":
            if len(parts) != 2:
                raise InvalidInputError("Usage: load <file.csv>")
            self.calculator.load(parts[1])
            return "Loaded."

        if cmd == "exit":
            return "__EXIT__"

        # Otherwise treat as operation: <op> <a> <b>
        if len(parts) != 3:
            raise InvalidInputError("Usage: <operation> <a> <b>")

        op = validate_operation(parts[0])
        a = validate_number(parts[1], max_value=self.calculator.config.max_input_value)
        b = validate_number(parts[2], max_value=self.calculator.config.max_input_value)

        result = self.calculator.calculate(op, a, b)
        return str(result)

    def run(self) -> None:
        print("Enhanced Calculator. Type 'help' for commands.")
        while True:
            try:
                line = input("> ")
                out = self.run_once(line)
                if out == "__EXIT__":
                    print("Bye.")
                    break
                if out:
                    print(out)
            except CalculatorError as e:
                # EAFP: easier to ask forgiveness than permission
                print(f"Error: {e}")
            except KeyboardInterrupt:  # pragma: no cover
                print("\nBye.")  # pragma: no cover
                break  # pragma: no cover
