#!/usr/bin/env python3
import utils.message as msg

from utils.prompt import prompt
from utils.prompt import prompt_boolean
import git_helpers.git_utils as git

from git_helpers.get_all_branch_regexes import get_branch_type_from_location

from git_helpers.update_branch import update_branch			

import os
import sys

def open_feature(repo):

    msg.subtitle("Open Feature Branch")

    git.checkout("develop")
        
    new_branch_name="feature-{}".format(prompt("\nEnter Feature Name").replace(" ","_"))

    if git.is_branch_on_local(new_branch_name):
        msg.user_error(
            "Branch "+new_branch_name+" already exists on local.",
            "Please git checkout -b "+new_branch_name+" or choose a new branch name."    
        )
        sys.exit(1)

    git.checkoutb(new_branch_name)
    git.push_origin(repo, new_branch_name)

    msg.dbg("success", sys._getframe().f_code.co_name)

def close_feature(repo, regex_branch, regex_branches, all_version_tags):
    msg.subtitle("Close Feature Branch '"+regex_branch.text+"'")

    update_branch(all_version_tags, regex_branch)

    release_branches=get_branch_type_from_location("release", "local", regex_branches)
    
    # a feature branch can close if there are no open release branch
    if len(release_branches) == 0:
        msg.info("Preparing to merge "+regex_branch.text+" on branch develop")
        msg.info("Checkout on branch 'develop'")
        git.checkout("develop")
        git.merge_noff(regex_branch.text)
        git.delete_local_branch(regex_branch.text)

        git.delete_origin_branch(repo, regex_branch.text)
        git.push_origin(repo, "develop")

        msg.success(regex_branch.text+" has been closed on develop")
    else: # release_branch["num"] == 1
        msg.user_error("A Feature Branch can't be closed when a release Branch is still open. Close the Branch \""+release_branches[0].text+"\" and retry the operation.")
        sys.exit(1)
