#!/usr/bin/env python3
import utils.message as msg
import git_helpers.git_utils as git
import git_helpers.regex_obj as ro
import sys
from git_helpers.branch.feature import close_feature
from git_helpers.branch.release import close_release
from git_helpers.branch.hotfix import close_hotfix

def close_branch(repo, regex_branches, all_version_tags):
    msg.title("Close Branch")
    # get branch type
    branch_name=git.get_active_branch_name()
    branch_regex=ro.get_element_regex(branch_name)
    if branch_regex.type == "feature":
        close_feature(repo, branch_regex, regex_branches, all_version_tags)
    elif branch_regex.type == "release":
        close_release(repo, branch_regex, branch_regexes, all_version_tags)
    elif branch_regex.type == "hotfix":
        close_hotfix(repo, branch_regex, regex_branches, all_version_tags)
    else:
        msg.user_error(
            "You can't close on branch '"+ branch_name+"'.",
            "git checkout another_branch_type \"feature|release|hotfix\""
        )
        sys.exit(1)