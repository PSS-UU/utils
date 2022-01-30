#!/usr/bin/env python3
import os
import datetime
import sys

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
YEAR = datetime.date.today().year

# A list of GitHub handles to remove from repository watchers
COTEACHERS = [g.get_user(user_name) for user_name in ["andreasjohnsson"]]
PROJECT_COLUMNS = ["Blocked", "Backlog", "Doing", "Done"]

print(f"Using GitHub user {USER_ME.login}")

existing_members = {m.login for m in COURSE_ORG.get_members()}


def add_to_organisation(user, role):
    assert user, f"E: Could not find user {user}"
    if not user.login in existing_members:
        COURSE_ORG.add_to_members(user, role=role)
    else:
        print(f"W: User {user.login} is already a member of {COURSE_ORG.name}")


for teacher in COTEACHERS:
    add_to_organisation(teacher, role="admin")


def create_team(team_name, repo_name, owners):
    owners = [g.get_user(user) for user in owners]
    for owner in owners:
        add_to_organisation(owner, role="member")

    repo = COURSE_ORG.create_repo(repo_name, private=True)
    print(f"I: created repo {COURSE_ORG.name}/{repo.name}")

    team = COURSE_ORG.create_team(
        team_name, repo_names=[repo], permission="admin", privacy="secret"
    )

    print(f"I: created team {team.name}")

    for owner in owners:
        repo.add_to_collaborators(owner, permission="admin")
        team.add_membership(owner, role="maintainer")

    for staff in COTEACHERS:
        team.add_membership(staff, role="maintainer")

    # CREATE A GH PROJECT
    project = repo.create_project(name=team_name, body=f"Grupp i PSS {YEAR}")
    print(f"I: created project {project.name}")

    # You will thank me when you don't receive spam
    for staff in [USER_ME, *COTEACHERS]:
        repo.remove_from_collaborators(staff.login)
        print(f"I: Staff member {staff.login} removed from notifications.")

    # We need an active handler on a user name, so we can't do this for our
    # co-teachers :(
    USER_ME.remove_from_watched(repo)


    for column in PROJECT_COLUMNS:
        project.create_column(column)

    for column in project.get_columns():
        if column.name == "Backlog":
            column.create_card(note="Decide how you want to use this Kanban board!")
    print(f"I: set up project {project.name}")


def get_students():
    return filter(lambda l: l, map(lambda l: l.strip(), sys.stdin))


def main():
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} team-name repo-name < student-team.txt")
        exit(1)

    team = sys.argv[1]
    repo = sys.argv[2]
    students = get_students()
    create_team(team, repo, students)

if __name__ == "__main__":
    main()
