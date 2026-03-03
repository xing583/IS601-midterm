from __future__ import annotations

from dataclasses import asdict
from typing import Any, Callable, Dict, List, Optional

import pandas as pd

from app.exceptions import HistoryError


class Observer:
    """Observer interface."""

    def update(self, event: str, payload: Dict[str, Any]) -> None:
        raise NotImplementedError


class History:
    """
    Manages calculation history using a pandas DataFrame.
    Implements a basic Observer pattern to notify observers on events.
    """

    COLUMNS = ["timestamp", "operation", "a", "b", "result"]

    def __init__(self, max_size: int = 100):
        if max_size <= 0:
            raise HistoryError("max_size must be positive")
        self.max_size = max_size
        self._df = pd.DataFrame(columns=self.COLUMNS)
        self._observers: List[Observer] = []

    @property
    def df(self) -> pd.DataFrame:
        return self._df

    def attach(self, observer: Observer) -> None:
        self._observers.append(observer)

    def notify(self, event: str, payload: Dict[str, Any]) -> None:
        for obs in self._observers:
            obs.update(event, payload)

    def add_record(
        self,
        timestamp: str,
        operation: str,
        a: float,
        b: float,
        result: float,
    ) -> None:
        row = {
            "timestamp": timestamp,
            "operation": operation,
            "a": a,
            "b": b,
            "result": result,
        }
        self._df = pd.concat([self._df, pd.DataFrame([row])], ignore_index=True)

        # Enforce max size (drop oldest)
        if len(self._df) > self.max_size:
            self._df = self._df.iloc[-self.max_size :].reset_index(drop=True)

        self.notify("history_added", {"row": row})

    def clear(self) -> None:
        self._df = pd.DataFrame(columns=self.COLUMNS)
        self.notify("history_cleared", {})

    def __len__(self) -> int:
        return len(self._df)

    def to_list(self) -> List[Dict[str, Any]]:
        return self._df.to_dict(orient="records")

    def save_csv(self, filepath: str, encoding: str = "utf-8") -> None:
        try:
            self._df.to_csv(filepath, index=False, encoding=encoding)
        except Exception as e:
            raise HistoryError(f"Failed to save history: {e}")

        self.notify("history_saved", {"filepath": filepath})

    def load_csv(self, filepath: str, encoding: str = "utf-8") -> None:
        try:
            df = pd.read_csv(filepath, encoding=encoding)
        except FileNotFoundError as e:
            raise HistoryError(f"History file not found: {e}")
        except Exception as e:
            raise HistoryError(f"Failed to load history: {e}")

        # Validate columns
        for col in self.COLUMNS:
            if col not in df.columns:
                raise HistoryError(f"Missing column in history file: {col}")

        # Keep only expected columns and enforce max size
        df = df[self.COLUMNS]
        if len(df) > self.max_size:
            df = df.iloc[-self.max_size :].reset_index(drop=True)

        self._df = df
        self.notify("history_loaded", {"filepath": filepath})  # pragma: no cover
