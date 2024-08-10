#!/usr/bin/env python3
import os
import sys

from ..gpkgs import message as msg
from ..gpkgs.prompt import prompt
from ..gpkgs.gitlib import GitLib

def set_project(
    branches:list|None=None,
    direpa_src:str|None=None,
    email:str|None=None,
    init:bool=False,
    shared:str|None=None,
    username:str|None=None,
):  
    if branches is None:
        branches=[]
    if username is None:
        username=prompt("username")
    if email is None:
        email=prompt("email", default="not-set")

    if direpa_src is None:
        direpa_src=os.getcwd()

    git=GitLib(direpa=direpa_src)
    if init is True:
        if git.is_direpa_git() is True:
            msg.error("Current Path '"+direpa_src+"' is at a git project toplevel",
                "cd into another directory or remove its .git directory and restart the operation.")
            sys.exit(1)
        git.init()
        git.set_user_name(username)
        git.set_user_email(email)
        if shared is not None:
            git.set_shared_repo(shared=shared)
        git.commit_empty("Default branch created")

        for branch in branches:
            git.checkoutb(branch)
            git.commit_empty("Branch {} created".format(branch))
        msg.success("Path '{}' initialized.".format(direpa_src))
    else:
        git.is_direpa_git(fail_exit=True)
        git.set_user_name(username)
        git.set_user_email(email)
