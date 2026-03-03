# Enhanced Calculator (Module 5)

## Overview

This project implements an enhanced command-line calculator using Python.
It demonstrates object-oriented design, multiple design patterns, data persistence with pandas, and automated testing with 100% coverage.

---

## Features

* REPL (Read-Eval-Print Loop) interface
* Arithmetic operations:

  * add, subtract, multiply, divide
  * power, root
* History management using pandas DataFrame
* Save/load history to CSV
* Undo/redo functionality (Memento pattern)
* Configuration via environment variables
* Error handling (EAFP & LBYL)

---

## Design Patterns

* **Facade**: Calculator class provides a unified interface
* **Factory**: Creates operation objects dynamically
* **Strategy**: Different operation implementations
* **Observer**: Tracks history updates
* **Memento**: Supports undo/redo

---

## Project Structure

```
module5_calculator/
│
├── app/
│   ├── calculator_repl.py
│   ├── calculation.py
│   ├── calculator_config.py
│   ├── calculator_memento.py
│   ├── exceptions.py
│   ├── history.py
│   ├── input_validators.py
│   ├── operations.py
│
├── tests/
│   ├── test_calculations.py
│   ├── test_calculator_config.py
│   ├── test_calculator_memento.py
│   ├── test_calculator_repl.py
│   ├── test_calculator_repl_run_and_autoload.py
│   ├── test_exceptions.py
│   ├── test_history.py
│   ├── test_input_validators.py
│   ├── test_operations.py
│
├── main.py
├── requirements.txt
├── pytest.ini
└── README.md
```

---

## Setup

Clone the repository:

```
git clone https://github.com/xing583/module5_calculator.git
cd module5_calculator
```

Create and activate virtual environment:

```
python -m venv venv
source venv/bin/activate
```

Install dependencies:

```
pip install -r requirements.txt
```

---

## Run

```
python main.py
```

---

## Testing

Run tests:

```
pytest -q
```

Run coverage:

```
pytest --cov=app tests/
coverage report --fail-under=100
```

This project achieves **100% test coverage**.

---

## CI (GitHub Actions)

GitHub Actions is configured to:

* Run tests automatically on push
* Check 100% coverage
* Fail the build if coverage is below 100%

Workflow file:

```
.github/workflows/python-app.yml
```

---

## Example Commands

```
add 1 2
subtract 5 3
history
undo
redo
clear
save history.csv
load history.csv
exit
```

---

## Notes

* History is stored using pandas DataFrame
* Data is persisted in CSV files
* The application is modular and testable

---

## Course

NJIT IS601 - Web Systems Development
Assignment: Module 5 Enhanced Calculator
