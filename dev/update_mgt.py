#!/usr/bin/env python3
import os
import sys

from ..gpkgs import shell_helpers as shell
from ..gpkgs.gitlib import GitLib
from ..gpkgs import message as msg

def update_mgt(
    commit_message:str|None=None,
    project_path:str|None=None,
    remote_name:str|None=None,
):
    if project_path is None:
        project_path=os.getcwd()

    if commit_message is None:
        commit_message="edit"

    folder=os.path.basename(project_path)

    if folder != "mgt":
        if "mgt" in os.listdir(os.path.dirname(project_path)):
            project_path=os.path.join(os.path.dirname(project_path), "mgt")
        elif "mgt" in os.listdir(project_path):
            project_path=os.path.join(project_path, "mgt")
        else:
            msg.error(f"mgt folder not found in parent or children at {project_path}")
            sys.exit(1)

    git=GitLib(direpa=project_path)
    git.is_direpa_git(fail_exit=True)

    if remote_name is None:
        remote_name=git.get_remote_name()

    git.commit(message=commit_message)

    for branch in git.get_local_branches():
        git.push(branch_name=branch, set_upstream=True)
