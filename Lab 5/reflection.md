# Reflection

**Tools:** Pylint caught code-quality problems, Bandit found security risks, and Flake8 checked spacing.

**Main fix:** I replaced the shell command with a validated scp argument list. I also stopped teams from sharing a player list.

**Lesson:** A program can print the right output and still have bugs. Checking small leagues exposed the top-two error.

**Result:** The standings stayed the same. The tools helped, but I still needed behavior checks and manual review of the subprocess warnings.

*The supplied handout mentions reflection questions but does not include their text. These four points cover the work completed.*
