import pytest
from elevator_dispatch import next_direction, door_action, pick_elevator


@pytest.mark.parametrize("direction, requests, expected", [
    ("up", [1, 3, 5], "up"),
    ("up", [1], "down"),
    ("up", [3], "idle"),
    ("down", [1, 3, 5], "down"),
    ("down", [5], "up"),
    ("down", [], "idle"),
    ("idle", [1, 5], "up"),
    ("idle", [1], "down"),
    ("idle", [], "idle"),
])
def test_direction_branches(direction, requests, expected):
    assert next_direction(3, direction, requests) == expected


@pytest.mark.parametrize("load, blocked, emergency, expected", [
    (631, True, True, "hold_open"),
    (631, True, False, "overload"),
    (630, True, False, "reopen"),
    (630, False, False, "close"),
    (0, False, False, "close"),
])
def test_door_branches(load, blocked, emergency, expected):
    assert door_action(load, blocked, emergency) == expected


@pytest.mark.parametrize("cars, floor, expected", [
    ([], 3, None),
    ([("A", 3, True)], 3, "A"),
    ([("A", 1, True), ("B", 4, True)], 5, "B"),
    ([("A", 4, True), ("B", 10, True)], 5, "A"),
    ([("A", 5, False), ("B", 8, True)], 5, "B"),
    ([("A", 2, True), ("B", 4, True)], 3, "A"),
])
def test_car_selection(cars, floor, expected):
    assert pick_elevator(cars, floor) == expected
