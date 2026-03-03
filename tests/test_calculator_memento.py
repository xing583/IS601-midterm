import pytest
import pandas as pd

from app.calculator_memento import HistoryCaretaker
from app.exceptions import HistoryError


def make_df(values):
    return pd.DataFrame(values, columns=["x"])


def test_save_and_undo():
    caretaker = HistoryCaretaker()

    df1 = make_df([[1]])
    df2 = make_df([[2]])

    caretaker.save(df1)
    restored = caretaker.undo(df2)

    assert restored.iloc[0]["x"] == 1


def test_undo_empty_raises():
    caretaker = HistoryCaretaker()
    with pytest.raises(HistoryError):
        caretaker.undo(make_df([[1]]))


def test_redo_empty_raises():
    caretaker = HistoryCaretaker()
    with pytest.raises(HistoryError):
        caretaker.redo(make_df([[1]]))


def test_undo_then_redo():
    caretaker = HistoryCaretaker()

    df1 = make_df([[1]])
    df2 = make_df([[2]])
    df3 = make_df([[3]])

    caretaker.save(df1)          # undo has df1
    restored1 = caretaker.undo(df2)  # current df2 -> redo, restore df1
    assert restored1.iloc[0]["x"] == 1

    restored2 = caretaker.redo(df3)  # current df3 -> undo, restore df2
    assert restored2.iloc[0]["x"] == 2


def test_save_clears_redo():
    caretaker = HistoryCaretaker()

    df1 = make_df([[1]])
    df2 = make_df([[2]])

    caretaker.save(df1)
    caretaker.undo(df2)  # now redo available
    caretaker.save(df2)  # save should clear redo

    with pytest.raises(HistoryError):
        caretaker.redo(df1)
