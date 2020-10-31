#!/usr/bin/env python3
import os
import shutil
import sys
import re

from . import msg_helpers as msgh
from .helpers import get_path
from .set_origin import set_origin

from ..gpkgs import message as msg
from ..gpkgs import shell_helpers as shell
from ..gpkgs.prompt import prompt, prompt_boolean
from ..gpkgs.gitlib import GitLib

def clone(
    add_origin=False,
    direpa_dst=None,
    index=None,
    is_repo=False,
    package_name=None,
    projects_paths=[],
    sync=False,
):
    if len(projects_paths) == 0:
        projects_paths=[os.getcwd()]

    direpa_dst=get_path(direpa_dst, exit_not_found=False)
    print(direpa_dst)
    for d, direpa_git in enumerate(projects_paths):
        git=GitLib(direpa=direpa_git)
        git.is_direpa_git(fail_exit=True)
        direpa_dst_full=None

        diren_git=os.path.basename(direpa_git)

        if is_repo is True:
            if index is None:
                index=1
            else:
                try:
                    index=int(index)
                    if index <= 0:
                        raise Exception()
                except:
                    msg.error("--clone-to-repository index '{}' must be an integer > 0".format(index), exit=1)
            direpa_dst_full=os.path.join(direpa_dst, package_name[0], package_name, str(index), diren_git+".git")
        else:
            if package_name is None:
                direpa_dst_full=os.path.join(direpa_dst, diren_git+".git")
            else:
                direpa_dst_full=os.path.join(direpa_dst, package_name, diren_git+".git")

        os.makedirs(os.path.dirname(direpa_dst_full), exist_ok=True)

        if os.path.exists(direpa_dst_full):
            msg.error("directory already exists '{}'".format(direpa_dst_full), exit=1)


        branches=git.get_local_branches()
        branch=git.get_active_branch_name()
        
        if branch != "master":
            # you have to checkout to the branch that you want as head on repository, it can only be done when cloning.
            if "master" in branches:
                git.checkout("master")
            elif "develop" in branches:
                git.checkout("develop")

        git.clone(direpa_git, direpa_dst=direpa_dst_full, bare=True)

        if git.get_active_branch_name() != branch:
            git.checkout(branch)

        if add_origin is True:
            set_origin(
                path_origin=direpa_dst_full,
                path_git=direpa_git,
                sync=sync,
            )
