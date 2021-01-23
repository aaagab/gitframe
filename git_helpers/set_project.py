#!/usr/bin/env python3
import os
import re
import shutil
import sys

# from . import git_utils as git
from . import msg_helpers as msgh
from .license import get_license_content
from .helpers import get_path

from ..gpkgs import message as msg

from ..gpkgs import shell_helpers as shell
from ..gpkgs.prompt import prompt_boolean, prompt
from ..gpkgs.gitlib import GitLib

def set_project(
    direpas=[],
    email=None,
    init=False,
    shared=None,
    username=None,
):
    if username is None:
        username=prompt("username")
    if email is None:
        email=prompt("email", default="not-set")
    if shared is None:
        shared=prompt("shared value from 'false|true|umask|group|all|world|everybody|0xxx'", default="null")
    if shared == "null":
        shared=None

    if len(direpas) == 0:
        direpas.append(os.getcwd())

    for d, direpa_git in enumerate(direpas):
        # direpa_delete=os.path.join(direpa_git, ".git")
        # if os.path.exists(direpa_delete):
        #     shell.rmtree(direpa_delete)

        git=GitLib(direpa=direpa_git)
        if init is True:
            if git.is_direpa_git() is True:
                msg.error("Current Path '"+direpa_git+"' is at a git project toplevel",
                    "cd into another directory or remove its .git directory and restart the operation.")
                sys.exit(1)
            git.init()
            git.set_user_name(username)
            git.set_user_email(email)
            if shared is not None:
                git.set_shared_repo(shared=shared)
            git.commit_empty("Branch master created")

            if os.path.basename(direpa_git) not in ["doc", "mgt"]:
                git.checkoutb("develop")
                git.commit_empty("Branch develop created")
            msg.success("Path '{}' initialized.".format(direpa_git))
        else:
            git.is_direpa_git(fail_exit=True)
            git.set_user_name(username)
            git.set_user_email(email)
