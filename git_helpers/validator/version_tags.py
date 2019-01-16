#!/usr/bin/env python3
import sys, os
import git_helpers.git_utils as git
import utils.message as msg
import re
import utils.shell_helpers as shell

from git_helpers.get_all_branch_regexes import get_branch_type_from_location, filter_all_regex_branches_from_location
import git_helpers.version as version

import git_helpers.regex_obj as ro

# from git_helpers.validator.hotfix import compare_version_tag_with_hotfix_branch_name
from git_helpers.validator.support import find_related_tag_for_support_branch_name
from git_helpers.validator.hotfix import check_hotfix_is_either_on_master_or_on_support

# if a release_tag exists.
    # each version_value must follow the form \d+\.\d+\.\d+
        
    # if support or hotfix
        # functions are called from respective validators file to apply the needed rules
        # the rules are listed there

# def version_file_validator(regex_branches, all_version_tags):
def version_tags_validator(regex_branches, all_version_tags):
    msg.subtitle("Verify version tags.")
    
    local_regex_branches=filter_all_regex_branches_from_location(regex_branches, "local")

    if all_version_tags:
        regex_support_branches=get_branch_type_from_location("support", "local", regex_branches)
        regex_hotfix_branches=get_branch_type_from_location("hotfix", "local", regex_branches)

        for regex_branch in local_regex_branches:
            if regex_branch.type == "support":
                # match_branch_name_with_version_value(regex_branch, regex_version_value)
                find_related_tag_for_support_branch_name(regex_branch, all_version_tags)
            elif regex_branch.type == "hotfix":
                # match_branch_name_with_version_value(regex_branch, regex_version_value)
                check_hotfix_is_either_on_master_or_on_support(regex_branch, all_version_tags, regex_support_branches)
    else: # not all_version_tags
        for regex_branch in local_regex_branches:
            regex_branch.type=ro.get_element_regex(regex_branch.text).type

            if regex_branch.type in ["hotfix", "support"]:
                msg.user_error(
                    "The project has no release tags",
                    " Branch '{}' shouldn't exist.".format(regex_branch.text)
                )
                sys.exit(1)
    
    msg.dbg("success", sys._getframe().f_code.co_name)
