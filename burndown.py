#!/usr/bin/env python3
import os
import sys
from decimal import Decimal
from collections import namedtuple, Counter
import re
from datetime import datetime, timezone, timedelta

DONE_KEYWORDS = ["Done"]
DEFAULT_STORY_POINTS = Decimal(1)
TIMEZONE = timezone(timedelta(hours=1), name="se")
COURSE_START = datetime(2021, 2, 3, tzinfo=TIMEZONE)
COURSE_END = datetime(2021, 3, 21, tzinfo=TIMEZONE)

# Something like (17), or (5.5) or (13P)
STORY_PTS_PAREN_RE = re.compile(r"[\(\[](?P<pts>\d+(\.\d+)?)[Pp]?[\)\]]")

# Something like "weight: 0.5"
STORY_PTS_INLINE_RE = re.compile(r"weight:\s+(?P<pts>\d+(\.\d+)?)\b")

PTS_RES = [STORY_PTS_PAREN_RE, STORY_PTS_INLINE_RE]

# A Task is a tuple of a title, a done-date (or None if in progress), and a
# number of story points.
Task = namedtuple("Task", ["done_at", "title", "story_points"])

try:
    from github import GithubException
    from github import Github
except ImportError:
    print("Package github not found, you need to install pygithub!")
    exit(1)

try:
    g = Github(os.environ["GH_TOKEN"])
except KeyError:
    print("You need to set the environment variable GH_TOKEN to your access token!")
    exit(1)

COURSE_ORG = g.get_organization("PSS-UU")
USER_ME = g.get_user()

# Return the title of the card, or the title of its associated issue/PR if it
# doesn't have one.
def card_title(card):
    return card.note.rstrip() if card.note else card.get_content().title


# Returns a best-effort estimate datetime when this card was completed. For
# regular cards, it just returns the update date with the assumption that that
# the last update was moving them to DONE. For PRs and issues, return the close
# date (if they are closed), otherwise fall back to the date of the last update.
def card_closed_date(card):
    content = card.get_content()
    if content and content.closed_at:
        return content.closed_at.replace(tzinfo=None).astimezone(tz=TIMEZONE)

    return card.updated_at.replace(tzinfo=None).astimezone(tz=TIMEZONE)


# Make a best-effort to parse the card and find its story points as a Decimal
# (floating-point numbers are the Devil's work).
def card_story_points(card):
    title = card_title(card)
    for pts_re in PTS_RES:
        match = pts_re.search(title)
        if match:
            return Decimal(match["pts"])
    return DEFAULT_STORY_POINTS


def heading(text):
    return f"{text}\n{'=' * len(text)}\n"


def fmt_task(task):
    status_str = "TODO" if not task.done_at else "DONE"
    date_str = f"Done: {task.done_at:%Y-%m-%d}" if task.done_at else ""
    return f"{status_str} {task.title} {date_str} {task.story_points:n}p"


def is_done_column(column):
    return any([done_keyword in column.name for done_keyword in DONE_KEYWORDS])


def get_todo_done_tasks(project):
    todo_tasks = []
    done_tasks = []

    for column in project.get_columns():
        cards = list(column.get_cards())

        if is_done_column(column):
            done_tasks.extend(
                [
                    Task(
                        done_at=card_closed_date(c),
                        title=card_title(c),
                        story_points=card_story_points(c),
                    )
                    for c in cards
                ]
            )
        else:
            todo_tasks.extend(
                [
                    Task(
                        done_at=None,
                        title=card_title(c),
                        story_points=card_story_points(c),
                    )
                    for c in cards
                ]
            )
    return todo_tasks, done_tasks


# Generate an ideal burndown of story_points between start_date and end_date,
# as a list of story points left.
def ideal_burndown(story_points, start_date, end_date):
    days = (end_date - start_date).days
    rate = story_points / days
    return [rate * day for day in range(days, 0, -1)]


# Generate a burndown chart
def burndown_chart(todo, done, team_name, filename):
    try:
        import matplotlib

        matplotlib.rcParams["figure.dpi"] = 300
        if filename:
            # This is a non-interactive engine
            matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError as e:
        print(f"Error importing matplotlib: {e}")
        return

    total_pts = sum((t.story_points for t in [*todo, *done]))
    ideal = ideal_burndown(total_pts, COURSE_START, COURSE_END)

    completed_pts_by_day = Counter()

    # group tasks by day offset completed
    for task in done:
        day_offset = (task.done_at - COURSE_START).days
        completed_pts_by_day[day_offset] += task.story_points

    pts_left = total_pts
    burndown = []
    for day in range(len(ideal)):
        pts_left -= completed_pts_by_day[day]
        burndown.append(pts_left)

    # TODO: annotate the X-axis for better readability
    plt.plot(ideal, label="Ideal")
    plt.plot(burndown, label="Actual")
    plt.ylabel("Points left")
    plt.xlabel("Days since start")
    plt.title(f"Burndown for {team_name}", fontname="Helvetica")
    plt.legend()

    if not filename:
        plt.show()
    else:
        plt.savefig(filename, bbox_inches="tight")


def main():
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print(f"Usage: {sys.argv[0]} <repository> [burndown chart file name.png]")
        exit(1)

    repo_name = sys.argv[1]
    filename = sys.argv[2] if len(sys.argv) > 2 else None

    repo = COURSE_ORG.get_repo(repo_name)
    (project,) = repo.get_projects()
    todo_tasks, done_tasks = get_todo_done_tasks(project)

    todo_story_pts = sum((t.story_points for t in todo_tasks))
    done_story_pts = sum((t.story_points for t in done_tasks))
    now = datetime.now(timezone.utc)
    since_start = now - COURSE_START
    velocity = done_story_pts / since_start.days
    print(
        f"{project.name}: {len(todo_tasks)} in backlog"
        f" ({todo_story_pts:n} pts), {len(done_tasks)} completed"
        f" ({done_story_pts:n} pts). Velocity: {velocity:.2} pts/day"
    )

    # print(heading("TODO"))
    # for task in todo_tasks:
    #     print(f"* {fmt_task(task)}")

    # print(heading("DONE"))
    for task in done_tasks:
        print(f"* {fmt_task(task)}")
    print("====")

    burndown_chart(todo_tasks, done_tasks, project.name, filename)


if __name__ == "__main__":
    main()
