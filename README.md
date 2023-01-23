## What's This?

This is a collection of various utilities for the course Platform-Spanning
Systems, so far just `burndown.sh`. The other scripts are used by  to automate
the use of GitHub, but students are encouraged to look at them if they are
interested.



## Installation

To install the dependencies in a virtual environment, do: 

```
$ python3 -m venv .venv
$ ./.venv/bin/pip3 install -r requirements.txt
$ source .venv/bin/activate
```

## Usage

`burndown.py` is a script for generating a burndown chart of your progress
across the course, based on information found in your team project (Kanban
board). Use it with the name of your team's _repository_ name (the one holding
your project).

```
$ ./burndown.py cinco-amigos burndown.png
Cinco amigos: x in backlog (x pts), y completed (n pts). Velocity: b pts/day
* DONE Task x Done: 2020-02-10 1p
...
```

The burndown chart will be saved in PNG format if you supply a file name,
otherwise you get [an interactive Matplotlib
window](https://matplotlib.org/users/interactive.html), which may or may not
work on some systems (notably, some or all macOS versions have a wonky system
Python setup). Providing a file name will run Matplotlib non-interactively,
which (in my experience) is more reliable.

`scan.sh`will scan for unprotected MySQL installations on the student servers.

`stop-spamming-me.py PSS-UU` will remove you as owner from the student repositories in the PSS-UU organisation to avoid getting drowned in GitHub notifications. You will be prompted (to a somewhat annoying degree).

`init-team-repository.py` Will initialise a project and an empty repository with a project Kanban board for a team. It will read GitHub user names from stdin:

```
$ ./init-team-repository.py "Fish friers" fish-friers << EOF
hacker1
hacker2
hacker3
EOF
```



### Caveats

The following caveats apply:

- Emoji don't render well (read: at all) in chart titles.
- The "number of days since start of course" is somewhat confusing for the
  x-axis in the burndown chart.
- You need [a GitHub access token](https://github.com/settings/tokens) with
  sufficient privileges in the environment variable `$GH_TOKEN`.
- You also need the pygithub and matplotlib packages installed. If you have
  [Poetry](https://python-poetry.org/) installed, there is already a project
  file configured and all you should need is `poetry install` and then sourcing
  the resulting virtual environment.
- End dates are unreliable. If your cards are issues or pull requests, the
  closing date is used as the date of completion. In any other case (including
  open PRs and issues) the script uses the update date of the given card, under
  the assumption that the last modification was moving it to DONE.

### Specifying Story Points

You can specify story points in the notes of a card. Any number in parenthesis
followed by an optional P is considered a story point, or any occurrence by the
string "weight: " followed by a number. For cards without story points, a
default value is used (currently 1).

I believe all current methods for specifying story points are parsed correctly,
but PRs are welcome otherwise!

### Do we _have_ to use this?

No. I make no guarantees that it runs on your computer (PRs welcome!), or does
what it should.
