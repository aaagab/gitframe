#!/usr/bin/env python3
import os
import sys

from .prompt_for_commit import prompt_for_commit

from ..gpkgs import shell_helpers as shell
from ..gpkgs.gitlib import GitLib
from ..gpkgs.prompt import prompt_boolean


def update_branch(
    commit_message=None,
    projects_paths=None,
):
    if len(projects_paths) == 0:
        projects_paths=[os.getcwd()]

    for d, direpa_git in enumerate(projects_paths):
        git=GitLib(direpa=direpa_git)
        git.is_direpa_git(fail_exit=True)
        prompt_for_commit(commit_message=commit_message, direpa_git=git.get_direpa_root())

        shell.cmd_prompt("git push origin --tags")
        for branch in git.get_local_branches():
            git.push("origin", branch_name=branch)
