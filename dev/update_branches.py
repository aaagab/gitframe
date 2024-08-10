#!/usr/bin/env python3
import os
import sys

from ..gpkgs import shell_helpers as shell
from ..gpkgs.gitlib import GitLib

def update_branches(
    commit_message:str|None=None,
    project_path:str|None=None,
):
    if project_path is None:
        project_path=os.getcwd()

    git=GitLib(direpa=project_path)
    git.is_direpa_git(fail_exit=True)
    git.commit(message=commit_message)

    shell.cmd_prompt("git push origin --tags")
    for branch in git.get_local_branches():
        git.push("origin", branch_name=branch)
