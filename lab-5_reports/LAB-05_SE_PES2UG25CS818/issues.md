# Issues Identified in Static Code Analysis

The table documents defects identified in the original `election_system.py`.
Line numbers refer to that original version. Each fix approach describes the
change made to the cleaned version.

| Issue | Type | Line(s) | Description | Fix Approach |
| --- | --- | --- | --- | --- |
| Hidden bidirectional Unicode character and incorrect officer check | Security / Logic - High | 22 | A hidden control character obscured the role comparison, and the function incorrectly treated almost any role as an officer. | Removed the hidden character and made `is_officer` return true only for the exact `"officer"` role. |
| Weak MD5 hash for voter ID | Security - High | 17 | MD5 is unsuitable for security-sensitive hashing, and the stored hash was not used by the application. | Removed the unnecessary hash from voter records instead of replacing it with another unused hash. |
| Repeat voting and invalid candidate acceptance | Election integrity - High | 26-34 | The function did not prevent a voter from voting again or check that the selected candidate was valid. | `cast_vote` now checks voter existence, voting status, and candidate validity before recording a ballot. |
| Hard-coded administrator password | Security - Medium | 9 | The original source contained a password literal, exposing a credential to anyone who could read the file. | Read `ADMIN_PASSWORD` from the environment rather than embedding its value in source code. |
| Unsafe postal ballot XML parsing | Security - Medium | 7, 75 | The original parser could be unsafe for untrusted XML, and imported candidate values were not validated. | Parse with `defusedxml` and import ballots only for recognized candidates. |
| Poll closing boundary was incorrect | Logic - Medium | 26-34 | The original `>` check accepted ballots during the closing hour, including at 18:00. | `cast_vote` rejects votes when `when.hour >= POLLS_CLOSE_HOUR`. |
| Empty-election division by zero | Runtime - Medium | 51-55 | Vote percentage and turnout calculations divided by zero when there were no ballots or no voters. | Return zero when the relevant collection is empty. |
| Announcement lambdas captured the final loop value | Logic - Medium | 65-69 | Each deferred lambda referenced the same loop variable, producing announcements for the final candidate instead of each candidate. | Build announcement strings immediately from each candidate and its tally. |
| Receipt used an undefined and unsuitable random source | Runtime / Security - Medium | 71-72 | `random` was not imported, causing a `NameError`; ordinary pseudorandom generation is not suitable for security-sensitive identifiers. | Generate the six-digit receipt number with `secrets.randbelow`. |
| Bare exception silently hid XML import errors | Code quality / Reliability - Low | 79-83 | A bare `except` with `pass` concealed failures and made the import result unreliable. | Removed the silent catch so parsing errors are reported; validate candidates explicitly. |
| Unused imports and local variables | Code quality - Low | 1-3, 32, 45, 55 | Unused imports and assignments triggered static-analysis warnings and obscured the required logic. | Removed imports and variables that were not needed. |
| Naming, documentation, and formatting violations | Code style - Low | Multiple | Pylint and Flake8 reported non-snake-case names, missing docstrings, long lines, trailing whitespace, and spacing violations. | Renamed functions in snake_case, added docstrings, and corrected formatting. |

## Validation after fixes

| Tool | Result |
| --- | --- |
| Pylint | 10.00/10 |
| Flake8 | No findings |
| Bandit | No issues identified |
