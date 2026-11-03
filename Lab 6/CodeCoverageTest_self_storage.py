import pytest

from self_storage import rent_due, access_allowed, payment_status


@pytest.mark.parametrize(
    "unit_size,months,is_climate,is_member,expected",
    [
        ("small", 1, False, False, 0),
        ("medium", 2, False, False, 0),
        ("large", 3, False, False, 0),
        ("small", 2, False, False, 80),
        ("small", 3, True, False, 240),
        ("small", 3, False, True, 80),
        ("medium", 4, True, True, 120),
        ("large", 4, True, True, 120),
        ("small", 8, False, False, 490),
        ("small", 8, True, False, 735),
    ],
)
def test_rent_due_valid_scenarios(unit_size, months, is_climate, is_member, expected):
    assert rent_due(unit_size, months, is_climate, is_member) == expected


@pytest.mark.parametrize(
    "unit_size,months",
    [
        ("extra_large", 1),
        ("small", -1),
    ],
)
def test_rent_due_invalid_inputs(unit_size, months):
    with pytest.raises(ValueError):
        rent_due(unit_size, months, False, False)


@pytest.mark.parametrize(
    "hour,visitors,is_owner,expected",
    [
        (12, 1, True, True),
        (12, 5, True, False),
        (5, 1, False, False),
        (23, 1, False, False),
        (6, 2, False, True),
        (22, 2, False, True),
        (12, 3, False, False),
    ],
)
def test_access_allowed_scenarios(hour, visitors, is_owner, expected):
    assert access_allowed(hour, visitors, is_owner) is expected


@pytest.mark.parametrize(
    "days_to_due,is_autopay,has_prior_late,expected",
    [
        (0, True, False, "current"),
        (0, True, True, "grace"),
        (5, False, False, "current"),
        (4, False, False, "grace"),
        (-10, False, False, "grace"),
        (-11, False, False, "lien"),
        (15, False, True, "current"),
        (13, False, True, "grace"),
        (-1, False, True, "lien"),
    ],
)
def test_payment_status_scenarios(days_to_due, is_autopay, has_prior_late, expected):
    assert payment_status(days_to_due, is_autopay, has_prior_late) == expected
