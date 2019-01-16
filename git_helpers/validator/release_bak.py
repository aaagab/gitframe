#!/usr/bin/env python3
import os
import sys
import re

import git_helpers.git_utils as git
import utils.message as msg

from git_helpers.get_all_branch_regexes import get_branch_type_from_location
import git_helpers.regex_obj as ro

# Only one or None release branch is tolerated max (on local and Remote),
# Release Branch name needs to be the same on local and Remote
# release branches are also always updated with Remote because it has to be there to know if you can open a new release branch from another computer.
# name of release branch must be latest release + major or + minor.
# if release branch name is different than 1.0.0 or different than 0.1.0 then tags must already exists

def force_unique_release_branch_name(reg_branches):
    msg.subtitle("One Release Branche max at a time.")
    local_branches=get_branch_type_from_location("release", "local", reg_branches)
    if len(local_branches) > 1:
        msg.user_error("There are more than one release branch on local ['{}'], please delete one.".format("', '".join(br.text for br in local_branches)))
        sys.exit(1)
    
    remotes_branches=get_branch_type_from_location("release", "remote", reg_branches)
    if len(remotes_branches) > 1:
        msg.user_error("There are more than one release branch on remote ['{}'], please delete one".format("', '".join(br.text for br in remotes_branches)))
        sys.exit(1)

    if len(remotes_branches) == 1 and len(local_branches) == 1:
        if remotes_branches[0].text != local_branches[0].text:
            msg.user_error(
                "local release branch name '"+local_branches[0].text+"' and remote release branch name '"+remotes_branches[0].text+"' are different.",
                "Only One Release Branch Name can exist at a time. Please correct the issue."
            )
            sys.exit(1)

    msg.dbg("success", sys._getframe().f_code.co_name)

def  validate_release_branch_name(reg_branches, all_version_tags):
    msg.subtitle("Validate Release Branche Names.")
    release_branch=get_branch_type_from_location("release", "local", reg_branches)
    if release_branch:
        release_branch=release_branch[0]
                
        if not all_version_tags:
            if release_branch.version != "0.1.0" and release_branch.version != "1.0.0":
                msg.user_error("Tags are not present and release branch version '"+release_branch.version+"' is different than '0.1.0' or '1.0.0'")
                sys.exit(1)
        else:
            latest_release=ro.Version_regex(all_version_tags[-1])
            if release_branch.major == latest_release.major:
                if int(release_branch.minor) != int(latest_release.minor) + 1:
                    msg.user_error(
                        "Latest release is '"+latest_release.text+"' and release branch name is '"+release_branch.text+"'",
                        "Minor number on release tag branch name should be '{}' not '{}'".format(int(latest_release.minor)+1,release_branch.minor))
                    sys.exit(1)
            else:
                if int(release_branch.major) != int(latest_release.major) + 1:
                    msg.user_error(
                        "Latest release is '"+latest_release.text+"' and release branch name is '"+release_branch.text+"'",
                        "Major number on release tag branch name should be '{}' not '{}'".format(int(latest_release.major)+1,release_branch.major))
                    sys.exit(1)
        
        msg.dbg("success", sys._getframe().f_code.co_name)
    