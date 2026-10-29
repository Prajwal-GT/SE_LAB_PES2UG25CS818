
import pytest

from credit_card_rewards import (
    reward_points,
    late_payment_fee,
    card_status,
)


# -------- REWARD POINTS: BRANCH COVERAGE --------

def test_unknown_card_tier():
    with pytest.raises(ValueError, match="unknown card tier"):
        reward_points("silver", 100, "grocery", False)


@pytest.mark.parametrize("amount", [0, -10])
def test_invalid_amount(amount):
    with pytest.raises(ValueError, match="invalid amount"):
        reward_points("classic", amount, "grocery", False)


def test_fuel_category():
    assert reward_points("gold", 500, "fuel", True) == 0


def test_regular_category():
    assert reward_points("classic", 1000, "grocery", False) == 10


@pytest.mark.parametrize("category", ["dining", "travel"])
def test_double_reward_categories(category):
    assert reward_points("classic", 1000, category, False) == 20


def test_weekend_bonus_applied():
    assert reward_points("gold", 1000, "grocery", True) == 70


def test_weekend_bonus_not_applied_to_classic():
    assert reward_points("classic", 1000, "grocery", True) == 10


def test_weekday_no_bonus():
    assert reward_points("platinum", 1000, "grocery", False) == 40


# -------- LATE PAYMENT FEE: BRANCH COVERAGE --------

@pytest.mark.parametrize(
    ("outstanding", "days_late"),
    [(5000, 0), (5000, -1), (0, 10), (-100, 10)],
)
def test_fee_is_zero_for_invalid_or_on_time_payment(outstanding, days_late):
    assert late_payment_fee(outstanding, days_late) == 0


def test_low_outstanding_fee():
    assert late_payment_fee(500, 10) == 100


def test_medium_outstanding_fee():
    assert late_payment_fee(5000, 10) == 500


def test_high_outstanding_fee():
    assert late_payment_fee(20000, 10) == 1000


def test_additional_fee_after_30_days():
    assert late_payment_fee(500, 31) == 850


def test_no_additional_fee_at_30_days():
    assert late_payment_fee(500, 30) == 100


# -------- CARD STATUS: BRANCH COVERAGE --------

def test_frozen_branch():
    assert card_status(100, 5, True) == "frozen"


def test_blocked_branch():
    assert card_status(20, 3, False) == "blocked"


def test_not_blocked_with_two_missed_payments():
    assert card_status(20, 2, False) == "watch"


def test_over_limit_branch():
    assert card_status(91, 0, False) == "over limit risk"


def test_not_over_limit_at_90_percent():
    assert card_status(90, 0, False) == "watch"


def test_watch_due_to_utilisation():
    assert card_status(31, 0, False) == "watch"


def test_watch_due_to_missed_payment():
    assert card_status(20, 1, False) == "watch"


def test_good_branch():
    assert card_status(30, 0, False) == "good"

# Branch coverage tests validate decision outcomes.