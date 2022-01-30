#!/usr/bin/env python3
from collections import defaultdict
import os
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
    print("Generate one at https://github.com/settings/tokens")
    exit(1)


def ask_yes_no(question):
    print(question)
    response = input("Y/n> ").lower()
    if response == "y" or response == "":
        return True
    else:
        return False


def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]}: organisation", file=sys.stderr)
        exit(1)
    organisation_name = sys.argv[1]
    organisation = g.get_organization(organisation_name)
    user_me = g.get_user()
    print(f"Using GitHub user {user_me.login}")
    # Too slow:
    # repos = filter(lambda r: user_me.has_in_watched(r) or user_me.has_in_subscriptions(r), organisation.get_repos())
    repos = organisation.get_repos()

    print("Fetching repositories...")
    print(
        f"Available repositories: {', '.join([f'{r.name} private={r.private}' for r in repos])}."
    )
    print(
        "Remove yourself from (p)rivate repositories, (a)ll repositories, or a(s)k for each one?"
    )
    response = input("p/a/s> ").strip()
    if response == "p":
        filterer = lambda r: r.private
    elif response == "a":
        filterer = lambda r: True
    elif response == "s":
        filterer = lambda r: ask_yes_no(f"Remove {r.name} from watches?")
    else:
        print(f"Incorrect response '{response}'; exiting.")
        exit(1)

    for repo in filter(filterer, repos):
        if repo.archived:
            continue
        try:
            user_me.remove_from_watched(repo)
            repo.remove_from_collaborators(user_me.login)
            print(f"Unfollowed {repo.name}")
        except GithubException as e:
            print(f"Exception unfollowing {repo.name}: {e}")


if __name__ == "__main__":
    main()
