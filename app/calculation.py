from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict


@dataclass(frozen=True)
class Calculation:
    """Represents a single calculation record."""
    timestamp: str
    operation: str
    a: float
    b: float
    result: float

    @classmethod
    def create(cls, operation: str, a: float, b: float, result: float) -> "Calculation":
        ts = datetime.now().isoformat(timespec="seconds")
        return cls(timestamp=ts, operation=operation, a=a, b=b, result=result)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "timestamp": self.timestamp,
            "operation": self.operation,
            "a": self.a,
            "b": self.b,
            "result": self.result,
        }
