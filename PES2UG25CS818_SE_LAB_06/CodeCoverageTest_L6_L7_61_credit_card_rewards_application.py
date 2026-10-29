
import pytest

from credit_card_rewards import (
    reward_points,
    late_payment_fee,
    card_status,
)


# ---------------- REWARD POINTS TESTS ----------------

def test_classic_grocery():
    assert reward_points("classic", 1000, "grocery", False) == 10


def test_gold_grocery():
    assert reward_points("gold", 1000, "grocery", False) == 20


def test_platinum_grocery():
    assert reward_points("platinum", 1000, "grocery", False) == 40


def test_unknown_card_tier():
    with pytest.raises(ValueError, match="unknown card tier"):
        reward_points("silver", 100, "grocery", False)


@pytest.mark.parametrize("amount", [0, -100])
def test_invalid_reward_amount(amount):
    with pytest.raises(ValueError, match="invalid amount"):
        reward_points("classic", amount, "grocery", False)


def test_fuel_rewards_are_zero():
    assert reward_points("gold", 500, "fuel", False) == 0


@pytest.mark.parametrize(
    ("category", "expected"),
    [("dining", 20), ("travel", 20)],
)
def test_double_points_categories(category, expected):
    assert reward_points("classic", 1000, category, False) == expected


def test_gold_weekend_bonus():
    assert reward_points("gold", 1000, "grocery", True) == 70


def test_platinum_weekend_bonus():
    assert reward_points("platinum", 1000, "grocery", True) == 90


def test_classic_has_no_weekend_bonus():
    assert reward_points("classic", 1000, "grocery", True) == 10


def test_amount_below_100():
    assert reward_points("classic", 99, "grocery", False) == 0


# ---------------- LATE PAYMENT FEE TESTS ----------------

@pytest.mark.parametrize(
    ("outstanding", "days_late"),
    [(5000, 0), (5000, -1), (0, 10), (-100, 10)],
)
def test_invalid_or_on_time_payment(outstanding, days_late):
    assert late_payment_fee(outstanding, days_late) == 0


@pytest.mark.parametrize(
    ("outstanding", "expected"),
    [(1000, 100), (1001, 500), (10000, 500), (10001, 1000)],
)
def test_fee_brackets(outstanding, expected):
    assert late_payment_fee(outstanding, 10) == expected


def test_fee_with_more_than_30_days_late():
    assert late_payment_fee(500, 31) == 850


def test_fee_at_exactly_30_days():
    assert late_payment_fee(500, 30) == 100


def test_highest_fee_with_late_penalty():
    assert late_payment_fee(20000, 45) == 1750


# ---------------- CARD STATUS TESTS ----------------

def test_frozen_card():
    assert card_status(50, 0, True) == "frozen"


def test_blocked_after_three_missed_payments():
    assert card_status(20, 3, False) == "blocked"


def test_blocked_with_more_than_three_missed_payments():
    assert card_status(20, 4, False) == "blocked"


def test_over_limit_risk():
    assert card_status(91, 0, False) == "over limit risk"


def test_watch_above_30_percent():
    assert card_status(31, 0, False) == "watch"


def test_watch_when_payment_missed():
    assert card_status(20, 1, False) == "watch"


def test_good_status():
    assert card_status(30, 0, False) == "good"


def test_exactly_90_percent_is_not_over_limit():
    assert card_status(90, 0, False) == "watch"


def test_frozen_takes_priority():
    assert card_status(100, 5, True) == "frozen"

# Code coverage tests validate application statements.