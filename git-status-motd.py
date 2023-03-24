#!/usr/bin/python3
import subprocess
import os
import sys

import click

from colorama import Fore, Style


@click.command()
@click.option(
    "-r",
    "--repofile",
    help="The relative or absolute path of the file containing paths of local git repositories"
)
@click.option(
    "-v",
    "--verbose",
    help="Prints out additional information related to git repository status",
    default=False,
    is_flag=True
)
def git_stat(repofile, verbose):
    with open(repofile, "r") as reader:
        repo_list = [i.strip("\n") for i in reader.readlines()]

    status_mapping = {
        "m": {"count": 0, "description": "Missing"},
        "M": {"count": 0, "description": "Modified"},
        "?": {"count": 0, "description": "New"},
        "A": {"count": 0, "description": "Staged"},
        "D": {"count": 0, "description": "Removed"},
    }

    repo_not_found_list = []
    needs_commit_list = []
    needs_pull_list = []
    pull_value = ""
    commit_value = ""

    for repo in repo_list:
        if not os.path.exists(repo):
            repo_not_found_list.append(repo)
            continue

        os.chdir(repo)

        needs_commit = False

        # Fetch remote
        git_fetch = subprocess.Popen(["git", "fetch"], stderr=subprocess.PIPE)
        fetch_err = git_fetch.communicate()[1]

        if fetch_err:
            repo_not_found_list.append(repo)
            continue

        git_status_short = [
            i.lstrip(" ") for i in subprocess.check_output(
                ["git", "status", "-s"],
                stderr=subprocess.PIPE
            ).decode("UTF8").split("\n")[:-1]
        ]

        git_status_long = subprocess.check_output(
            ["git", "status"],
            stderr=subprocess.PIPE
        ).decode("UTF8").split("\n")

        pull_message = ""
        if "Your branch is behind" in git_status_long[1]:
            needs_pull = True
            pull_message = f"Git repository: {repo}"
            pull_value = f"{git_status_long[1]}"
            needs_pull_list.append(repo)

        if len(git_status_short):
            needs_commit = True
            for i in git_status_short:
                status_mapping[i[0]]["count"] += 1
                if i[1] in status_mapping.keys():
                    status_mapping[i[1]]["count"] += 1

        commit_message = ""
        if needs_commit:
            commit_message = f"{Fore.GREEN}A git commit is required on {repo}"
            needs_commit_list.append(repo)
            commit_value = "\n".join([f"  {v.get('count')}\t{v.get('description')}" for v in status_mapping.values()])

        if verbose:
            print(Fore.GREEN + pull_message)
            print(Fore.WHITE + pull_value)
            print(Fore.GREEN + commit_message)
            print(Fore.WHITE + commit_value)

    if not verbose:
        if len(needs_commit_list):
            print(Fore.GREEN + "The following repositories can be commited: ")
            for repo in needs_commit_list:
                print(Fore.WHITE + f"  - {repo}")

        if len(needs_pull_list):
            print(Fore.GREEN + "The following repositories need to pull from the remote: ")
            for repo in needs_pull_list:
                print(Fore.WHITE + f"  - {repo}")

    if len(repo_not_found_list):
        for repo in repo_not_found_list:
            print(Fore.RED + f"Was unable to find {repo}, please check {repofile}")
    print(Style.RESET_ALL)

try:
    git_stat.invoke(git_stat.make_context(info_name="ezt", args=sys.argv[1:]))

except click.exceptions.Exit as code:
    if code == 0:
        pass

except TypeError as type_err:
    print(git_stat.get_help(click.Context(git_stat)))
    print(f"\nGit-Stat ERROR: {type_err} Invalid arugment")



