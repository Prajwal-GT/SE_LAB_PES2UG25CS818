"""A small voting and election management demonstration."""

import os
import secrets
from datetime import datetime
from typing import TypedDict

from defusedxml import ElementTree

ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD")
POLLS_CLOSE_HOUR = 18


class VoterRecord(TypedDict):
    """Information stored for each registered voter."""

    name: str
    voted: bool


voters: dict[str, VoterRecord] = {}
ballots: list[str] = []
candidates = ["Alice", "Bob", "NOTA"]


def register_voter(voter_id: str, name: str, age: int) -> bool:
    """Register an eligible voter once."""
    if age < 18 or voter_id in voters:
        return False

    voters[voter_id] = {"name": name, "voted": False}
    return True


def is_officer(role: str) -> bool:
    """Return whether the supplied role is an election officer."""
    return role == "officer"


def cast_vote(voter_id: str, candidate: str, when: datetime) -> bool:
    """Record one valid vote before the polls close."""
    voter = voters.get(voter_id)
    if (
        voter is None
        or voter["voted"]
        or candidate not in candidates
        or when.hour >= POLLS_CLOSE_HOUR
    ):
        return False

    ballots.append(candidate)
    voter["voted"] = True
    return True


def tally() -> dict[str, int]:
    """Return the number of ballots for each selected candidate."""
    counts: dict[str, int] = {}
    for ballot in ballots:
        counts[ballot] = counts.get(ballot, 0) + 1
    return counts


def winner() -> str | None:
    """Return the candidate with the most votes, or None if no votes exist."""
    counts = tally()
    return max(counts, key=counts.get) if counts else None


def vote_percent(name: str) -> int:
    """Return the candidate's whole-number share of all ballots."""
    if not ballots:
        return 0
    return tally().get(name, 0) * 100 // len(ballots)


def turnout() -> float:
    """Return the percentage of registered voters who cast a ballot."""
    if not voters:
        return 0.0
    return len(ballots) / len(voters) * 100


def count_for(candidate: str, ballot_list: list[str]) -> int:
    """Count occurrences of a candidate in the provided ballots."""
    return sum(ballot == candidate for ballot in ballot_list)


def announce() -> list[str]:
    """Return one announcement per candidate."""
    counts = tally()
    return [f"{name}: {counts.get(name, 0)}" for name in candidates]


def receipt_number() -> str:
    """Generate a six-digit receipt number using a secure random source."""
    return f"RCPT-{secrets.randbelow(900_000) + 100_000}"


def import_postal_ballots(xml_text: str) -> int:
    """Import ballots for known candidates from safely parsed XML."""
    root = ElementTree.fromstring(xml_text)
    imported = 0
    for ballot in root.iter("ballot"):
        candidate = ballot.get("candidate")
        if candidate in candidates:
            ballots.append(candidate)
            imported += 1
    return imported


def main() -> None:
    """Run the demonstration election and print its results."""
    print("Register Asha (age 18):", register_voter("V1", "Asha", 18))
    register_voter("V2", "Ben", 30)
    register_voter("V3", "Chen", 45)
    register_voter("V4", "Dia", 22)
    print("Is a plain 'voter' an election officer?", is_officer("voter"))
    print(
        "Ben votes Alice:",
        cast_vote("V2", "Alice", datetime(2026, 11, 20, 10, 0)),
    )
    print(
        "Ben votes Alice again:",
        cast_vote("V2", "Alice", datetime(2026, 11, 20, 11, 0)),
    )
    print(
        "Chen votes 'bob':",
        cast_vote("V3", "bob", datetime(2026, 11, 20, 12, 0)),
    )
    print(
        "Dia votes Bob at 18:30:",
        cast_vote("V4", "Bob", datetime(2026, 11, 20, 18, 30)),
    )
    postal_xml = "<postal><ballot voter='V1' candidate='Bob'/></postal>"
    print("Postal ballots imported:", import_postal_ballots(postal_xml))
    print("Tally:", tally())
    print("Winner:", winner())
    print("Alice %:", vote_percent("Alice"))
    print("Turnout %:", turnout())
    print("Announcements:", announce())
    print("Receipt:", receipt_number())


if __name__ == "__main__":
    main()
