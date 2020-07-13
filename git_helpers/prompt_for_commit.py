#!/usr/bin/env python3
import sys

from . import git_utils as git
from .init_local_config import init_local_config

from ..gpkgs import message as msg

from ..gpkgs.prompt import prompt
from ..gpkgs import shell_helpers as shell


def prompt_for_commit(commit_message=None):
    msg.info("Prompt for commit")
    
    init_local_config()

    files_to_commit=shell.cmd_get_value("git status --porcelain")
    if files_to_commit:
        print("__untracked files present__")
        for f in files_to_commit.splitlines():
            print("  "+str(f))

        if commit_message is None:
            commit_message=prompt("Type Commit Message")
        shell.cmd_prompt("git add .")
        shell.cmd_prompt("git commit -am \""+commit_message+"\"")
    else:
        msg.info("Nothing to commit on "+git.get_active_branch_name())
