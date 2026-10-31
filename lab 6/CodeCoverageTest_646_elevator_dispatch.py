import pytest
from elevator_dispatch import next_direction, door_action, pick_elevator


@pytest.mark.parametrize("direction, requests, expected", [
    ("up", [5], "up"),
    ("up", [1], "down"),
    ("up", [], "idle"),
    ("down", [1], "down"),
    ("down", [5], "up"),
    ("down", [], "idle"),
    ("idle", [5], "up"),
    ("idle", [1], "down"),
    ("idle", [], "idle"),
])
def test_direction(direction, requests, expected):
    assert next_direction(3, direction, requests) == expected


@pytest.mark.parametrize("load, blocked, emergency, expected", [
    (100, False, True, "hold_open"),
    (631, False, False, "overload"),
    (100, True, False, "reopen"),
    (100, False, False, "close"),
])
def test_doors(load, blocked, emergency, expected):
    assert door_action(load, blocked, emergency) == expected


def test_pick_closest_car():
    cars = [("A", 1, False), ("B", 4, True), ("C", 10, True)]
    assert pick_elevator(cars, 5) == "B"
