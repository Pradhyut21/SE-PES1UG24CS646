# Issues fixed

USN: PES1UG24CS646. Lines refer to the original file.

| Issue | Type | Line(s) | Description | Fix Approach |
|---|---|---|---|---|
| Shell injection | Bandit B605, High | 71 | The server name became part of a shell command. | Validate the host and call scp with separate arguments and no shell. |
| Unsafe temporary file | Bandit B306, Medium | 66 | mktemp returned a name without creating the file. | Use mkstemp and close its descriptor. |
| Embedded password | Bandit B105, Low | 6 | A demo password was stored in the source. | Remove the unused constant. |
| Predictable random source | Bandit B311, Low | 61 | The coin toss used random.choice. | Use secrets.choice. |
| Shared player list | Pylint W0102 | 11 | Teams could share the same default list. | Default to None and give each team a fresh list. Copy supplied rosters too. |
| Top-two check | Pylint R1714 and manual review | 56-58 | Repeated comparisons also failed with fewer than two teams. | Check membership in the first two table entries. |
| Unclear naming and missing docs | Pylint C0103, C0114, C0116 | 1, 11-74 | Names and documentation did not follow Python conventions. | Use snake_case and short docstrings. |
| Unnecessary branching | Pylint R1705 | 17-22 | elif and else followed a return. | Use early returns. |
| Spacing | Flake8 E203, E302, E231, E261 | 5, 60, 79, 87 | Four whitespace violations. | Fix the colon, blank line, comma and comment spacing. |
| Runs during import | Manual review | 92 | Importing the module started the demo. | Add a main guard. |

Bandit review: B404 and B603 are narrowly marked with `nosec` because scp still needs a subprocess. The executable is resolved to an absolute path, the destination is validated, and shell=False is explicit. The unsuppressed audit is saved as `reports/after/bandit_review.txt`; it retains these two Low findings. No global checks are disabled.
