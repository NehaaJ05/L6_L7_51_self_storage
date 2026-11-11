from hypothesis import given, strategies as st
from self_storage import parse_rental, duration_average, payable_rent


@given(st.one_of(st.text(), st.none()))
def test_parse_rental_no_crash(s):
    try:
        result = parse_rental(s)
    except Exception as exc:
        assert False, f"parse_rental crashed with {s!r}: {type(exc).__name__}: {exc}"


@given(st.one_of(st.text(), st.none()))
def test_duration_average_no_crash(s):
    try:
        result = duration_average(s)
    except Exception as exc:
        assert False, f"duration_average crashed with {s!r}: {type(exc).__name__}: {exc}"


@given(st.one_of(st.text(), st.none()))
def test_payable_rent_no_crash(s):
    try:
        result = payable_rent(s)
    except Exception as exc:
        assert False, f"payable_rent crashed with {s!r}: {type(exc).__name__}: {exc}"


def test_parse_rental_valid_input():
    assert parse_rental("medium:6") == ("Medium", 6.0)


def test_duration_average_valid_input():
    assert duration_average("3,6,12") == 7


def test_payable_rent_valid_input():
    assert payable_rent("2400|200") == 2632.0


def test_invalid_inputs_return_none():
    assert parse_rental(None) is None
    assert parse_rental("medium") is None
    assert duration_average("") is None
    assert duration_average("1,,3") is None
    assert payable_rent("1000") is None
    assert payable_rent("abc|10") is None
