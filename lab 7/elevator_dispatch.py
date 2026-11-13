def parse_request(text):
    """Return the start and destination floors, or None for an invalid request."""
    if not isinstance(text, str):
        return None
    try:
        start, end = text.split("->")
        return int(start), int(end)
    except ValueError:
        return None


def total_travel(floors_csv):
    """Return the distance for a nonempty floor list, or None for invalid CSV."""
    if not isinstance(floors_csv, str):
        return None
    try:
        floors = [int(floor) for floor in floors_csv.split(",")]
    except ValueError:
        return None
    return sum(abs(end - start) for start, end in zip(floors, floors[1:]))


def load_percent(text):
    """Return the whole load percentage, or None for invalid load or capacity."""
    if not isinstance(text, str):
        return None
    try:
        load_text, capacity_text = text.split(" of ")
        load, capacity = int(load_text), int(capacity_text)
    except ValueError:
        return None
    if load < 0 or capacity <= 0:
        return None
    return load * 100 // capacity


def main():
    print("==== Running parse_request ====")
    user_input = input("Enter a request as FROM->TO (e.g. 5->9): ")
    result = parse_request(user_input)
    if result is None:
        print("Invalid request. Enter two integer floors separated by ->.")
    else:
        print("From and To:", result)

    print("\n==== Running total_travel ====")
    user_input = input("Enter floors visited as CSV (e.g. 1,5,3,9): ")
    result = total_travel(user_input)
    if result is None:
        print("Invalid floor list. Enter one or more comma-separated integers.")
    else:
        print("Floors Travelled:", result)

    print("\n==== Running load_percent ====")
    user_input = input("Enter load as 'X of Y' (e.g. 450 of 630): ")
    result = load_percent(user_input)
    if result is None:
        print("Invalid load. Enter a nonnegative load and a positive capacity as 'X of Y'.")
    else:
        print("Load Percent:", result)


if __name__ == "__main__":
    main()
