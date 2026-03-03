import pytest

from app.history import History, Observer
from app.exceptions import HistoryError


class CounterObserver(Observer):
    def __init__(self):
        self.events = []

    def update(self, event, payload):
        self.events.append((event, payload))


def test_history_init():
    h = History(max_size=3)
    assert len(h) == 0
    assert list(h.df.columns) == History.COLUMNS


def test_history_invalid_max_size():
    with pytest.raises(HistoryError):
        History(max_size=0)


def test_add_record_and_max_size_enforced():
    h = History(max_size=2)
    h.add_record("t1", "add", 1, 2, 3)
    h.add_record("t2", "add", 2, 3, 5)
    h.add_record("t3", "add", 3, 4, 7)

    assert len(h) == 2
    rows = h.to_list()
    assert rows[0]["timestamp"] == "t2"
    assert rows[1]["timestamp"] == "t3"


def test_clear_history():
    h = History(max_size=5)
    h.add_record("t1", "add", 1, 2, 3)
    assert len(h) == 1
    h.clear()
    assert len(h) == 0


def test_observer_notified():
    h = History(max_size=5)
    obs = CounterObserver()
    h.attach(obs)

    h.add_record("t1", "add", 1, 2, 3)
    h.clear()

    events = [e[0] for e in obs.events]
    assert "history_added" in events
    assert "history_cleared" in events


def test_save_and_load_csv(tmp_path):
    h = History(max_size=5)
    h.add_record("t1", "add", 1, 2, 3)

    file_path = tmp_path / "history.csv"
    h.save_csv(str(file_path))

    h2 = History(max_size=5)
    h2.load_csv(str(file_path))

    assert len(h2) == 1
    assert h2.to_list()[0]["operation"] == "add"


def test_load_missing_file(tmp_path):
    h = History(max_size=5)
    missing = tmp_path / "nope.csv"

    with pytest.raises(HistoryError):
        h.load_csv(str(missing))

import pandas as pd


def test_observer_interface_not_implemented():
    from app.history import Observer

    obs = Observer()
    try:
        obs.update("x", {})  # should raise
        assert False, "Expected NotImplementedError"
    except NotImplementedError:
        assert True


def test_save_csv_failure_raises_history_error(tmp_path):
    # pass a directory path to to_csv should raise (can't write to a directory)
    from app.history import History
    from app.exceptions import HistoryError

    h = History(max_size=5)
    h.add_record("t1", "add", 1, 2, 3)

    with pytest.raises(HistoryError):
        h.save_csv(str(tmp_path))  # directory, not file


def test_load_csv_missing_columns_raises(tmp_path):
    from app.history import History
    from app.exceptions import HistoryError

    bad = tmp_path / "bad.csv"
    # Missing required columns
    pd.DataFrame([{"foo": 1, "bar": 2}]).to_csv(bad, index=False)

    h = History(max_size=5)
    with pytest.raises(HistoryError):
        h.load_csv(str(bad))

import pandas as pd
import pytest

from app.history import History
from app.exceptions import HistoryError


def test_load_csv_other_exception_branch(tmp_path, monkeypatch):
    """
    Force pd.read_csv to raise a generic Exception (not FileNotFoundError),
    to cover History.load_csv() generic-exception branch.
    """
    h = History(max_size=5)

    def boom(*args, **kwargs):
        raise RuntimeError("boom")

    monkeypatch.setattr(pd, "read_csv", boom)

    with pytest.raises(HistoryError):
        h.load_csv(str(tmp_path / "any.csv"))
