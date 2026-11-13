from hypothesis import example, given, strategies as st

from elevator_dispatch import load_percent, parse_request, total_travel


FLOORS = st.integers(min_value=-10_000, max_value=10_000)
NON_TEXT = st.none() | st.integers() | st.binary() | st.lists(FLOORS)
BAD_FLOOR = st.text(max_size=20).map(lambda text: f"[{text}]")


@given(start=FLOORS, end=FLOORS)
@example(start=-3, end=0)
def test_parse_request_valid(start, end):
    assert parse_request(f" {start} -> {end} ") == (start, end)


@given(
    text=NON_TEXT
    | st.sampled_from(["", "1->", "1->2->3"])
    | BAD_FLOOR
    | st.builds("{}->{}".format, FLOORS, BAD_FLOOR)
)
def test_parse_request_rejects_invalid_input(text):
    assert parse_request(text) is None


@given(floors=st.lists(FLOORS, min_size=1, max_size=30))
@example(floors=[1, 5, 3, 9])
@example(floors=[-2])
def test_total_travel_valid(floors):
    expected = sum(abs(floors[i] - floors[i - 1]) for i in range(1, len(floors)))
    assert total_travel(", ".join(map(str, floors))) == expected


@given(
    text=NON_TEXT
    | st.sampled_from(["", "1,,3", "1,2,"])
    | BAD_FLOOR
    | st.builds("{},{}".format, FLOORS, BAD_FLOOR)
)
def test_total_travel_rejects_invalid_input(text):
    assert total_travel(text) is None


@given(load=st.integers(0, 10**12), capacity=st.integers(1, 10**12))
@example(load=0, capacity=630)
@example(load=450, capacity=630)
@example(load=700, capacity=630)
def test_load_percent_valid(load, capacity):
    percentage = load_percent(f"{load} of {capacity}")
    assert isinstance(percentage, int)
    assert percentage * capacity <= load * 100 < (percentage + 1) * capacity


@given(
    text=NON_TEXT
    | BAD_FLOOR
    | st.builds("{} of {}".format, st.integers(0, 10**12), st.integers(-10**12, 0))
    | st.builds("{} of {}".format, st.integers(-10**12, -1), st.integers(1, 10**12))
    | st.builds("{} of {}".format, st.integers(0, 10**12), BAD_FLOOR)
)
def test_load_percent_rejects_invalid_input(text):
    assert load_percent(text) is None
