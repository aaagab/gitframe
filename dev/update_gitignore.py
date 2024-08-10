#!/usr/bin/env python3
import os
import re
import sys

from ..gpkgs import shell_helpers as shell
from ..gpkgs.gitlib import GitLib

def update_gitignore(
    direpa:str|None=None,
):
    current_dir=os.getcwd()
    if direpa is None:
        direpa=current_dir

    git=GitLib(direpa=direpa)
    git.is_direpa_git(fail_exit=True)

    restore=False
    if git.direpa_root != current_dir:
        os.chdir(git.direpa_root)
        restore=True
    
     # fatal: pathspec '.' did not match any files
    # the error above means no file has been added yets
    shell.cmd_prompt("git rm -r --cached .")
    if git.need_commit() is True:
        git.commit(".gitignore updated")

    if restore is True:
        os.chdir(current_dir)
