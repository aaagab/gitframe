#!/usr/bin/env python3
import os
import sys

from . import git_utils as git
from .init_local_config import init_local_config

from ..gpkgs import message as msg

from ..gpkgs.prompt import prompt
from ..gpkgs import shell_helpers as shell


def prompt_for_commit(commit_message=None, direpa_git=None):
    msg.info("Prompt for commit")

    direpa_current=os.getcwd()
    toggled=False
    if direpa_git is not None:
        if direpa_git != direpa_current:
            toggled=True
            os.chdir(direpa_git)
    
    init_local_config()

    files_to_commit=shell.cmd_get_value("git status --porcelain")
    if files_to_commit is not None:
        print("__untracked files present__")
        for f in files_to_commit.splitlines():
            print("  "+str(f))

        if commit_message is None:
            commit_message=prompt("Type Commit Message")
        shell.cmd_prompt("git add .")
        shell.cmd_prompt("git commit -am \""+commit_message+"\"")
    else:
        msg.info("Nothing to commit on '{}' at '{}'".format(git.get_active_branch_name(), direpa_git))
    
    if toggled is True:
        os.chdir(direpa_current)
