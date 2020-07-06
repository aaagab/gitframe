#!/usr/bin/env python3
import os
import shutil
import sys
import re

from . import git_utils as git
from . import msg_helpers as msgh
from .helpers import get_path
from .remote_repository import Remote_repository

from ..gpkgs import message as msg
from ..gpkgs import shell_helpers as shell
from ..gpkgs.prompt import prompt, prompt_boolean


def set_origin(
    branches=[],
    path_origin=None,
    path_git=None,
    sync=False,
):
    if not "@" in path_origin:
        path_origin=get_path(path_origin)

    current_path=False
    direpa_current=os.getcwd()
    if path_git is None:
        current_path=True
        path_git=direpa_current

    direpa_git=path_git

    if current_path is False:
        if os.path.isfile(direpa_git):
            msg.error("Path '"+direpa_git+"' is not a directory.")
            sys.exit(1)

    if git.is_git_project(direpa_git) is False:
        msg.error("Not a Git directory '{}'".format(direpa_git))
        sys.exit(1)

    if current_path is False:
        os.chdir(direpa_git)

    if shell.cmd_get_value("git config --get remote.origin.url") != "":
        shell.cmd_prompt("git remote set-url origin {}".format(path_origin))
    else:
        shell.cmd_prompt("git remote add origin {}".format(path_origin))

    if sync is True:
        verify_branch=False
        if len(branches) == 0:
            branches=git.get_local_branch_names()
        else:
            verify_branch=True
        
        repo=Remote_repository()
        for branch in branches:
            found=True
            if verify_branch is True:
                if git.is_branch_on_local(branch) == False:
                    found=False
                    msg.warning("At '{}' branch '{}' not found".format(direpa_git, branch))

            if found is True:
                git.push_origin(repo, branch, set_upstream=True)

    if current_path is False:
        os.chdir(direpa_current)
