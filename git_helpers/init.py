#!/usr/bin/env python3
import os
import re
import shutil
import sys

from . import git_utils as git
from . import msg_helpers as msgh
from .license import get_license_content
from .remote_repository import Remote_repository
from .helpers import get_path

from ..gpkgs import message as msg

from ..gpkgs import shell_helpers as shell
from ..gpkgs.prompt import prompt_boolean, prompt

def init(
    direpas=[],
    email=None,
    username=None,
):
    current_path=False
    direpa_current=os.getcwd()
    if len(direpas) == 0:
        current_path=True
        direpas=[direpa_current]

    if username is None:
        username=prompt("username")
    if email is None:
        email=prompt("email")

    for d, direpa_git in enumerate(direpas):
        if current_path is False:
            if os.path.isfile(direpa_git):
                msg.error("Path '"+direpa_git+"' is not a directory.")
                sys.exit(1)
            direpa_git=get_path(direpa_git)

        if git.is_git_project(direpa_git):
            if git.get_root_dir_path(direpa_git) == direpa_git:
                msg.error("Current Path '"+direpa_git+"' is at a git project toplevel",
                    "cd into another directory or remove its .git directory and restart the operation.")
                sys.exit(1)

        if current_path is False:
            os.chdir(direpa_git)

        shell.cmd("git init")
        shell.cmd("git config --local user.name "+username)
        shell.cmd("git config --local user.email "+email)
        git.commit_empty("Branch master created")
        git.checkoutb("develop")
        git.commit_empty("Branch develop created")
        msg.success("Path '{}' initialized.".format(direpa_git))

    if current_path is False:
        os.chdir(direpa_current)

