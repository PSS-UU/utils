## What's This?

This is a collection of various utilities for the course Platform-Spanning
Systems, so far just `burndown.sh`.

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
followed by an optional P is considered a story point. For cards without story
points, a default value is used (currently 1).

I believe all current methods for specifying story points are parsed correctly,
but PRs are welcome otherwise!

### Do we _have_ to use this?

No. I make no guarantees that it runs on your computer (PRs welcome!), or does
what it should.
