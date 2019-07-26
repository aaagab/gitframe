#!/usr/bin/env python3
import os
import sys

from .. import git_utils as git
from .. import msg_helpers as msgh
from .. import regex_obj as ro

from ..get_all_branch_regexes import get_branch_type_from_location
from ..update_branch import update_branch			

from ...gpkgs import message as msg

from ...utils.prompt import prompt
from ...utils.prompt import prompt_boolean

def open_features(repo):
    
    msgh.subtitle("Open Features Branch")

    git.checkout("develop")
        
    new_branch_name="{}-{}".format(ro.Features_regex().abbrev,prompt("\nEnter Features Branch Keyword(s)").replace(" ","_"))

    if git.is_branch_on_local(new_branch_name):
        msg.error(
            "Branch "+new_branch_name+" already exists on local.",
            "Please git checkout -b "+new_branch_name+" or choose a new branch name."    
        )
        sys.exit(1)

    git.checkoutb(new_branch_name)
    git.push_origin(repo, new_branch_name)

    msg.dbg("success", sys._getframe().f_code.co_name)

def close_features(repo, regex_branch, regex_branches, all_version_tags):
    msgh.subtitle("Close Features Branch '"+regex_branch.text+"'")

    update_branch(all_version_tags, regex_branch)

    msg.info("Preparing to merge "+regex_branch.text+" on branch develop")
    msg.info("Checkout on branch 'develop'")
    git.checkout("develop")
    git.merge_noff(regex_branch.text)
    git.delete_local_branch(regex_branch.text)

    git.delete_origin_branch(repo, regex_branch.text)
    git.push_origin(repo, "develop")

    msg.success(regex_branch.text+" has been closed on develop")