#!/usr/bin/env python3
import os
import sys

from .. import git_utils as git
from .. import msg_helpers as msgh
from .. import regex_obj as ro
from ..get_all_branch_regexes import get_branch_type_from_location

from ...gpkgs import message as msg

from ...gpkgs.prompt import prompt

def open_draft(repo):
    
    msgh.subtitle("Open Draft Branch")

    new_branch_name="{}-{}".format(ro.Draft_regex().abbrev,prompt("\nEnter Draft Branch Keyword(s)").replace(" ","_"))

    if git.is_branch_on_local(new_branch_name):
        msg.error(
            "Branch "+new_branch_name+" already exists on local.",
            "Please git checkout -b "+new_branch_name+" or choose a new branch name."    
        )
        sys.exit(1)

    git.checkoutb(new_branch_name)

    msg.dbg("success", sys._getframe().f_code.co_name)

def close_draft(repo, regex_branch):
    msgh.subtitle("Close Draft Branch '"+regex_branch.text+"'")
    git.checkout("develop")

    git.delete_local_branch(regex_branch.text)

    msg.success(regex_branch.text+" has been closed.")
