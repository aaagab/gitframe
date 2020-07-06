#!/usr/bin/env python3
import os
import shutil
import sys
import re

from . import git_utils as git
from . import msg_helpers as msgh
from .helpers import get_path
from .set_origin import set_origin

from ..gpkgs import message as msg
from ..gpkgs import shell_helpers as shell
from ..gpkgs.prompt import prompt, prompt_boolean

def clone(
    add_origin=False,
    direpa_dst=None,
    index=None,
    is_repo=False,
    package_name=None,
    projects_paths=[],
    sync=False,
):
    current_path=False
    direpa_current=os.getcwd()
    if len(projects_paths) == 0:
        current_path=True
        projects_paths=[direpa_current]

    direpa_dst=get_path(direpa_dst, exit_not_found=False)
    for d, direpa_git in enumerate(projects_paths):
        direpa_dst_full=None
        if current_path is False:
            if os.path.isfile(direpa_git):
                msg.error("Path '"+direpa_git+"' is not a directory.")
                sys.exit(1)
            direpa_git=get_path(direpa_git)

        if git.is_git_project(direpa_git) is False:
            msg.error("Not a Git directory '{}'".format(direpa_git))
            sys.exit(1)

        if current_path is False:
            os.chdir(direpa_git)

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

        cmd="git clone --quiet --bare \"{}\" \"{}\"".format(direpa_git, direpa_dst_full)
        shell.cmd_prompt(cmd)

        if add_origin is True:
            set_origin(
                path_origin=direpa_dst_full,
                path_git=direpa_git,
                sync=sync,
            )


    if current_path is False:
        os.chdir(direpa_current)

        