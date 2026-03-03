from app.calculation import Calculation


def test_calculation_create_and_to_dict():
    c = Calculation.create("add", 1.0, 2.0, 3.0)
    d = c.to_dict()

    assert d["operation"] == "add"
    assert d["a"] == 1.0
    assert d["b"] == 2.0
    assert d["result"] == 3.0
    assert isinstance(d["timestamp"], str)
    assert len(d["timestamp"]) > 0
