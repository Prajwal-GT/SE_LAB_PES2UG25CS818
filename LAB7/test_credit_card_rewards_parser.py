
from hypothesis import given, strategies as st

from credit_card_rewards_parser import (
    mask_card_number,
    parse_transaction,
    parse_statement_total
)


# Test 1: Fuzz testing card number
@given(st.text() | st.none())
def test_mask_card_number_no_crash(s):
    try:
        mask_card_number(s)
    except Exception as e:
        assert False, f"mask_card_number crashed: {e}"


# Test 2: Fuzz testing transaction
@given(st.text() | st.none())
def test_parse_transaction_no_crash(s):
    try:
        parse_transaction(s)
    except Exception as e:
        assert False, f"parse_transaction crashed: {e}"


# Test 3: Fuzz testing statement total
@given(st.text() | st.none())
def test_parse_statement_total_no_crash(s):
    try:
        parse_statement_total(s)
    except Exception as e:
        assert False, f"parse_statement_total crashed: {e}"


# Test 4: Valid card number
def test_valid_card_number():
    result = mask_card_number("4555 7890 6777 2929")
    assert result == "************2929"


# Test 5: Valid transaction
def test_valid_transaction():
    result = parse_transaction(
        "2026-06-04,breakfast,7000"
    )
    assert result == ("breakfast", 7000)


# Test 6: Valid statement total
def test_valid_statement_total():
    result = parse_statement_total("Total: 12,500")
    assert result == 12500


# Test 7: Invalid card number
def test_invalid_card_number():
    assert mask_card_number(None) == "Invalid card number"
    assert mask_card_number("") == "Invalid card number"


# Test 8: Invalid transaction
def test_invalid_transaction():
    assert parse_transaction(None) == ("Invalid transaction", 0)
    assert parse_transaction("") == ("Invalid transaction", 0)


# Test 9: Invalid statement total
def test_invalid_statement_total():
    assert parse_statement_total(None) == 0
    assert parse_statement_total("") == 0
