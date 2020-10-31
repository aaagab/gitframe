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

def update_gitignore(
    direpa=None,
):
    if direpa is None:
        direpa=os.getcwd()

    git=GitLib(direpa=direpa)
    git.is_direpa_git(fail_exit=True)
     # fatal: pathspec '.' did not match any files
    # the error above means no file has been added yets
    shell.cmd_prompt("git rm -r --cached \"{}\"".format(direpa))
    print(git.need_commit())
    if git.need_commit() is True:
        git.commit(".gitignore updated")
