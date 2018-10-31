#!/usr/bin/env python3
import utils.message as msg
from utils.prompt import prompt_boolean
import git_helpers.regex_obj as ro
import git_helpers.git_utils as git
import os, sys

def update_branch(all_version_tags, regex_branch=""):

    if not regex_branch:
        regex_branch=ro.get_element_regex(git.get_active_branch_name())

    msg.title("Update Branch '"+regex_branch.text+"'")

    if regex_branch.type in ["master", "develop", "release", "support"]:
        # branch is just synchronized with the validator
        pass
    elif regex_branch.type in ["feature", "hotfix"]:
        linked_branch=""
        if regex_branch.type == "feature":
            linked_branch="develop"
        elif regex_branch.type == "hotfix":
            latest_release_tags=git.get_latest_release_for_each_major(all_version_tags)
            regex_latest_release=ro.Version_regex(latest_release_tags[-1])

            # check if hotfix comes from master
            if regex_latest_release.major_minor == regex_branch.major_minor:
                    linked_branch="master"
            else: # hotfix comes from support
                linked_branch=ro.Support_regex().get_new_branch_name(regex_branch.major_minor)
        
        msg.info("Linked branch: "+linked_branch)

        cmp_status=git.get_branch_compare_status(regex_branch.text, linked_branch)
        msg.dbg("info", cmp_status)

        if cmp_status in  ["up_to_date", "push"]:
            pass
        elif cmp_status in ["pull","divergent_with_common_ancestor"]:
            git.merge_noff(linked_branch)
        elif cmp_status == "divergent_without_common_ancestor":
            msg.user_error(
                "Compare Status for '"+regex_branch.text+"' and '"+linked_branch+"' is '"+cmp_status+"'",
                "Branches are not related, find and correct the issue."
            )

    msg.success("Branch '"+regex_branch.text+"' updated.")
