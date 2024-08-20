#!/usr/bin/env python3
import os
import sys

from ..gpkgs import shell_helpers as shell
from ..gpkgs.gitlib import GitLib

def update_branches(
    commit_message:str|None=None,
    project_path:str|None=None,
    remote_name:str|None=None,
):
    if project_path is None:
        project_path=os.getcwd()

    git=GitLib(direpa=project_path)
    git.is_direpa_git(fail_exit=True)
    
    if remote_name is None:
        remote_name=git.get_remote_name()
        
    git.commit(message=commit_message)

    git.cmd(f"git push {remote_name} --tags")
    for branch in git.get_local_branches():
        git.push(remote_name=remote_name, branch_name=branch, set_upstream=True)
