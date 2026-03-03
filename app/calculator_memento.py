from __future__ import annotations

from dataclasses import dataclass
from typing import List

import pandas as pd

from app.exceptions import HistoryError


@dataclass(frozen=True)
class HistoryMemento:
    """Stores a snapshot of the history DataFrame."""
    df_snapshot: pd.DataFrame


class HistoryCaretaker:
    """
    Caretaker for HistoryMemento to support undo/redo.
    """

    def __init__(self):
        self._undo_stack: List[HistoryMemento] = []
        self._redo_stack: List[HistoryMemento] = []

    def save(self, current_df: pd.DataFrame) -> None:
        """Save a deep copy of the current state to undo stack."""
        self._undo_stack.append(HistoryMemento(current_df.copy(deep=True)))
        self._redo_stack.clear()

    def can_undo(self) -> bool:
        return len(self._undo_stack) > 0

    def can_redo(self) -> bool:
        return len(self._redo_stack) > 0

    def undo(self, current_df: pd.DataFrame) -> pd.DataFrame:
        if not self.can_undo():
            raise HistoryError("Nothing to undo")

        # move current -> redo
        self._redo_stack.append(HistoryMemento(current_df.copy(deep=True)))

        # restore previous
        memento = self._undo_stack.pop()
        return memento.df_snapshot.copy(deep=True)

    def redo(self, current_df: pd.DataFrame) -> pd.DataFrame:
        if not self.can_redo():
            raise HistoryError("Nothing to redo")

        # move current -> undo
        self._undo_stack.append(HistoryMemento(current_df.copy(deep=True)))

        memento = self._redo_stack.pop()
        return memento.df_snapshot.copy(deep=True)
