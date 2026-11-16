
def mask_card_number(number):
    """
    Hide all digits except the last four.
    Handle invalid inputs without crashing.
    """
    if not isinstance(number, str):
        return "Invalid card number"

    digits = number.replace(" ", "").replace("-", "")

    if len(digits) < 4 or not digits.isdigit():
        return "Invalid card number"

    return "*" * (len(digits) - 4) + digits[-4:]


def parse_transaction(line):
    """
    Parse DATE,CATEGORY,AMOUNT.
    Return a tuple containing category and amount.
    """
    if not isinstance(line, str):
        return ("Invalid transaction", 0)

    parts = line.split(",")

    if len(parts) != 3:
        return ("Invalid transaction", 0)

    date = parts[0].strip()
    category = parts[1].strip().lower()
    amount_text = parts[2].strip()

    if not date or not category or not amount_text:
        return ("Invalid transaction", 0)

    try:
        amount = int(amount_text)
    except ValueError:
        return ("Invalid transaction", 0)

    return (category, amount)


def parse_statement_total(text):
    """
    Extract the amount from a statement
    such as 'Total: 12,500'.
    """
    if not isinstance(text, str):
        return 0

    if ":" not in text:
        return 0

    amount_text = text.split(":", 1)[1].strip()
    amount_text = amount_text.replace(",", "")

    if not amount_text:
        return 0

    try:
        return int(amount_text)
    except ValueError:
        return 0


def main():
    print("==== Running mask_card_number ====")

    value = input(
        "Enter a card number (e.g. 4111 1111 1111 1234): "
    )

    print("Masked card number:", mask_card_number(value))

    print()
    print("==== Running parse_transaction ====")

    value = input(
        "Enter a transaction as DATE,CATEGORY,AMOUNT "
        "(e.g. 2026-11-05,dining,1550): "
    )

    print("Category and amount:", parse_transaction(value))

    print()
    print("==== Running parse_statement_total ====")

    value = input(
        "Enter the statement total line "
        "(e.g. Total: 12,500): "
    )

    print("Statement total:", parse_statement_total(value))


if __name__ == "__main__":
    main()
