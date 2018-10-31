#!/usr/bin/env python3
import utils.message as msg
import utils.shell_helpers as shell
import git_helpers.git_utils as git
from utils.prompt import prompt
import sys

def prompt_for_commit():
    msg.subtitle("Prompt for commit")
    
    files_to_commit=shell.cmd_get_value("git status --porcelain")
    if files_to_commit:
        print("__untracked files present__")
        for f in files_to_commit.splitlines():
            print("  "+str(f))

        user_str=prompt("Type Commit Message")
        shell.cmd("git add .")
        shell.cmd("git commit -a -m \""+user_str+"\"")
    else:
        msg.info("Nothing to commit on "+git.get_active_branch_name())
