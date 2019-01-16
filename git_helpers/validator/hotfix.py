#!/usr/bin/env python3
import sys

import utils.message as msg
import git_helpers.git_utils as git

import git_helpers.regex_obj as ro

# you can have multiple hotfix
# hotfix must always be on the latest release of all major releases

# a hotfix can be either on latest release or on a support branch but never alone
def check_hotfix_is_either_on_master_or_on_support(regex_hotfix_branch, all_version_tags, regex_support_branches):
    latest_release_tags=git.get_latest_release_for_each_major(all_version_tags)
    regex_latest_release=ro.Version_regex(latest_release_tags[-1])

    # check if hotfix comes from master
    if regex_latest_release.major != regex_hotfix_branch.major:
        # if no check if hotfix comes from one of the support branch
        if not regex_support_branches:
            msg.user_error(
                "Hotfix branch '"+regex_hotfix_branch.text+"' does not come from master and no support branches are also present.",
                "Checkout Hotfix branch according to master or a support branch."
                )
            sys.exit(1)
        else:
            found=False
            regex_selected_support_branch=""
            for regex_support_branch in regex_support_branches:
                if regex_support_branch.major == regex_hotfix_branch.major:
                    regex_selected_support_branch=ro.Support_regex(regex_support_branch.text)
                    found=True
                    break

            if not found:
                msg.user_error(
                    "Hotfix branch '"+regex_hotfix_branch.text+"' does not come from a support branch nor from master.",
                    "Checkout Hotfix branch according to master or a support branch."
                )
                sys.exit(1)
            else:
                msg.dbg("success", "hotfix '"+regex_hotfix_branch.text+"' comes from support branch '"+regex_selected_support_branch.text+"'")
    else:
        msg.dbg("success", "hotfix '"+regex_hotfix_branch.text+"' comes from latest release '"+regex_latest_release.text+"'")
