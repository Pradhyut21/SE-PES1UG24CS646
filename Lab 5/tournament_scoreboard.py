"""Record match results and display a league scoreboard."""

import os
import pathlib
import re
import secrets
import shutil
# Reviewed subprocess use: fixed executable, validated host, no shell.
import subprocess  # nosec B404
import tempfile

POINTS = {"win": 3, "draw": 1, "loss": 0}
TEAMS = {}
MATCHES = []


def add_team(team_name, players=None):
    """Register a team with its own player list."""
    TEAMS[team_name] = {"played": 0, "won": 0, "drawn": 0, "lost": 0,
                        "gf": 0, "ga": 0,
                        "players": [] if players is None else list(players)}


def match_result(home_goals, away_goals):
    """Return the winning side, or draw for equal scores."""
    if home_goals > away_goals:
        return "home"
    if home_goals < away_goals:
        return "away"
    return "draw"


def record_match(home, away, home_goals, away_goals):
    """Update both teams' statistics and save the match result."""
    result = match_result(home_goals, away_goals)
    sides = ((home, home_goals, away_goals), (away, away_goals, home_goals))
    for team, scored, conceded in sides:
        TEAMS[team]["played"] += 1
        TEAMS[team]["gf"] += scored
        TEAMS[team]["ga"] += conceded
    if result == "draw":
        TEAMS[home]["drawn"] += 1
        TEAMS[away]["drawn"] += 1
    else:
        winner, loser = (home, away) if result == "home" else (away, home)
        TEAMS[winner]["won"] += 1
        TEAMS[loser]["lost"] += 1
    MATCHES.append((home, away, home_goals, away_goals))


def points(team_name):
    """Calculate league points from wins and draws."""
    stats = TEAMS[team_name]
    return stats["won"] * POINTS["win"] + stats["drawn"] * POINTS["draw"]


def goal_difference(team_name):
    """Calculate goals scored minus goals conceded."""
    return TEAMS[team_name]["gf"] - TEAMS[team_name]["ga"]


def league_table():
    """Rank teams by points and then goal difference."""
    return sorted(TEAMS, key=lambda t: (points(t), goal_difference(t)),
                  reverse=True)


def is_top_two(team_name):
    """Check the top two safely, even with fewer than two teams."""
    return team_name in league_table()[:2]


def toss_coin():
    """Choose either coin side using the system random source."""
    return secrets.choice(["Heads", "Tails"])


def table_file_path():
    """Create a temporary JSON file; the caller must remove it later."""
    descriptor, path = tempfile.mkstemp(suffix=".json")
    os.close(descriptor)
    return path


def publish_table(server):
    """Copy table.json to /var/www/ using scp and a validated host."""
    pattern = (
        r"(?:[A-Za-z0-9_][A-Za-z0-9_.-]*@)?"
        r"[A-Za-z0-9](?:[A-Za-z0-9.-]*[A-Za-z0-9])?"
    )
    if not isinstance(server, str) or not re.fullmatch(pattern, server):
        raise ValueError("Use a hostname or user@hostname.")
    scp_path = shutil.which("scp")
    if scp_path is None:
        raise FileNotFoundError("Install OpenSSH scp to publish the table.")
    executable = str(pathlib.Path(scp_path).resolve(strict=True))
    source = str(pathlib.Path("table.json").resolve(strict=True))
    # Reviewed B603: literal arguments, validated destination, shell disabled.
    subprocess.run(  # nosec B603
        [executable, "-o", "BatchMode=yes", "--", source,
         f"{server}:/var/www/"],
        check=True, shell=False,
    )


def main():
    """Run the sample tournament and print its standings."""
    for name in ["Royal Strikers", "City Rovers", "Lake United"]:
        add_team(name)
    add_team("Hill Warriors")
    print("Toss:", toss_coin())
    record_match("Royal Strikers", "City Rovers", 2, 1)
    record_match("Lake United", "Hill Warriors", 0, 0)
    record_match("City Rovers", "Lake United", 3, 2)
    record_match("Hill Warriors", "Royal Strikers", 1, 1)
    print("Pos Team Played Won Drawn Lost Pts")
    for pos, name in enumerate(league_table(), 1):
        stats = TEAMS[name]
        print(pos, name, stats["played"], stats["won"], stats["drawn"],
              stats["lost"], points(name))  # one row per team
    print("Is City Rovers in the top two?", is_top_two("City Rovers"))
    print("Matches played:", len(MATCHES))


if __name__ == "__main__":
    main()
