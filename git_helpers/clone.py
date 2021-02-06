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
    diren_git=None,
    direpa_dst=None,
    is_repo=False,
    package_alias=None,
    projects_paths=[],
    shared=None,
    sync=False,
    uuid4=None,
):
    if len(projects_paths) == 0:
        projects_paths=[os.getcwd()]

    direpa_dst=get_path(direpa_dst, exit_not_found=False)
    for d, direpa_git in enumerate(projects_paths):
        if diren_git is None:
            tmp_diren_git=os.path.basename(direpa_git)
        else:
            if d > 0:
                msg.error("diren_git '{}' can only be set for one project paths at a time", exit=1)
            tmp_diren_git=diren_git

        git=GitLib(direpa=direpa_git)
        git.is_direpa_git(fail_exit=True)
        direpa_dst_full=None

        if is_repo is True:
            if uuid4 is None:
                msg.error("You have to provide a uuid4 for the package location when is_repo is True", exit=1)
            uuid4=uuid4.replace("-", "")
            direpa_dst_full=os.path.join(direpa_dst, package_alias[0], package_alias, uuid4, tmp_diren_git+".git")
        else:
            if package_alias is None:
                direpa_dst_full=os.path.join(direpa_dst, tmp_diren_git+".git")
            else:
                direpa_dst_full=os.path.join(direpa_dst, package_alias, tmp_diren_git+".git")

        os.makedirs(os.path.dirname(direpa_dst_full), exist_ok=True)

        if os.path.exists(direpa_dst_full):
            msg.error("directory already exists '{}'".format(direpa_dst_full), exit=1)


        branches=git.get_local_branches()
        branch=git.get_active_branch_name()
        
        git.clone(direpa_git, direpa_dst=direpa_dst_full, bare=True, shared=shared, default_branch="master")

        if git.get_active_branch_name() != branch:
            git.checkout(branch)

        if add_origin is True:
            set_origin(
                path_origin=direpa_dst_full,
                path_git=direpa_git,
                sync=sync,
            )
