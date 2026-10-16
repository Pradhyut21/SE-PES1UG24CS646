# Lab 5 - Tournament Scoreboard

USN: PES1UG24CS646

| Check | Before | After |
|---|---|---|
| Pylint | 4.75/10 | 10.00/10 |
| Bandit | 4 findings | 0 active findings, 2 reviewed exemptions |
| Flake8 | 4 findings | 0 findings |

The cleaned program, issue table and original tool reports are included. Before and after reports are in `reports/`. An empty Flake8 report means no findings. See `issues.md` for the two subprocess exemptions and `reports/after/bandit_review.txt` for the unsuppressed audit.

Run the demo with `python tournament_scoreboard.py`. It uses only Python's standard library. The optional publishing helper needs OpenSSH scp, an existing table.json, and SSH access to the destination. Publishing was checked with mocks; no remote transfer was attempted.

Three fix commits in the repository history cover Bandit security, Pylint quality and Flake8 formatting.

Source: https://github.com/SETAPESU26/L5_38_tournament_scoreboard (original commit c9ef096).
