#!/usr/bin/env python3
import utils.message as msg

from utils.prompt import prompt
from utils.prompt import prompt_boolean
import git_helpers.git_utils as git

from git_helpers.get_all_branch_regexes import get_branch_type_from_location

import git_helpers.regex_obj as ro

import os
import sys

def open_draft(repo):
    
    msg.subtitle("Open Draft Branch")

    new_branch_name="{}-{}".format(ro.Draft_regex().abbrev,prompt("\nEnter Draft Branch Keyword(s)").replace(" ","_"))

    if git.is_branch_on_local(new_branch_name):
        msg.user_error(
            "Branch "+new_branch_name+" already exists on local.",
            "Please git checkout -b "+new_branch_name+" or choose a new branch name."    
        )
        sys.exit(1)

    git.checkoutb(new_branch_name)

    msg.dbg("success", sys._getframe().f_code.co_name)

def close_draft(repo, regex_branch):
    msg.subtitle("Close Draft Branch '"+regex_branch.text+"'")
    git.checkout("develop")

    git.delete_local_branch(regex_branch.text)

    msg.success(regex_branch.text+" has been closed.")
