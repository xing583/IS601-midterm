# IS601 Midterm – Enhanced Calculator

## Project Overview

This project is an enhanced command-line calculator developed for the IS601 Midterm.
It extends the baseline calculator with advanced features, design patterns, persistent history, logging, and CI integration.

The application follows clean Object-Oriented Programming (OOP) principles and enforces high test coverage through automated GitHub Actions.

---

## Architecture & Design Patterns

The system implements multiple design patterns:

### Factory Pattern
`OperationFactory` dynamically creates operation instances based on user input.

### Facade Pattern
`Calculator` serves as a unified interface coordinating:
- Operations
- History management
- Logging
- Configuration
- Memento handling

### Memento Pattern
Undo/Redo functionality is implemented using `HistoryCaretaker`, storing DataFrame snapshots.

### Observer Pattern
Observers respond to calculation events (e.g., logging operations).

---

## Supported Operations

### Basic Operations
- `add`
- `subtract`
- `multiply`
- `divide`
- `power`
- `root`

### Additional Midterm Operations
- `modulus`
- `int_divide`
- `percent`
- `abs_diff`

### Example Usage
```
add 1 2
modulus 10 3
percent 50 200
abs_diff 10 25
```

---

## Project Structure

```
IS601-midterm/
│
├── app/
│   ├── __init__.py
│   ├── calculation.py
│   ├── calculator.py
│   ├── calculator_config.py
│   ├── calculator_memento.py
│   ├── exceptions.py
│   ├── history.py
│   ├── input_validators.py
│   ├── logger.py
│   ├── observers.py
│   └── operations.py
│
├── tests/
│   ├── test_calculations.py
│   ├── test_calculator_config.py
│   ├── test_calculator_memento.py
│   ├── test_calculator_repl_run_and_a...
│   ├── test_calculator_repl.py
│   ├── test_coverage_missing_lines.py
│   ├── test_exceptions.py
│   ├── test_history.py
│   ├── test_input_validators.py
│   └── test_operations.py
│
├── .github/
│   └── workflows/
│       └── python-app.yml
│
├── history/
├── logs/
├── venv/
├── .coverage
├── .env
├── .gitignore
├── history.csv
├── main.py
├── pytest.ini
├── README.md
└── requirements.txt
```

---

## Installation

Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate
```

Install dependencies:
```bash
pip install -r requirements.txt
```

---

## Configuration

The application uses environment-based configuration.

Create a `.env` file (or copy from `.env.example`):
```
MAX_HISTORY_SIZE=100
PRECISION=2
AUTO_SAVE=True
LOG_LEVEL=INFO
```

---

## Running the Application

Start the calculator:
```bash
python main.py
```

Available commands:
```
help
history
clear
undo
redo
save <file.csv>
load <file.csv>
exit
```

---

## Running Tests

Run unit tests with coverage enforcement:
```bash
pytest --cov=app --cov-fail-under=90
```

- Minimum required coverage: **90%**
- Current coverage: ≥ 90%
- All tests pass successfully

---

## GitHub Actions (CI)

GitHub Actions automatically:

- Installs dependencies
- Runs unit tests
- Enforces coverage ≥ 90%
- Fails the build if requirements are not met

---

## Error Handling

The application gracefully handles:

- Invalid numeric inputs
- Unsupported operations
- Division by zero
- Invalid file paths
- Undo/Redo edge cases

Custom exception classes ensure robust error management.

---

## Logging

The logging system records:

- Operation name
- Input values
- Calculation results
- Errors
- Timestamps

Logging level is configurable via environment variables.

---

## Optional Enhancements Implemented

- Observer-based logging
- Color-coded CLI output
- Dynamic help menu
- Configurable precision and history size
- Persistent CSV history with autosave

---

## Author

Xing Li
IS601 – Midterm Project
