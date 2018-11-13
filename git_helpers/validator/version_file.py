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
    # all branches must have a version.txt file
    # each version.txt file must have a version_value
    # each version_value must follow the form \d+\.\d+\.\d+
    # according to branch.
    # if  master
        # master version.txt and latest release on tag must be equal
    # elif develop
        # develop must be equal latest release
    # elif feature
        # feature are not checked because this branch is not mandatorily updated
        # release version file must be equal to latest release
        
    # elif support or hotfix or release
        # functions are called from respective validators file to apply the needed rules
        # the rules are listed there
# else:
    # file version.txt shouldn't exist for any branches type
    # the only branches that could exist are master, develop, feature


def version_file_validator(regex_branches, all_version_tags):
    master_version_file_value=version.get_content_version_file(False, "master")
    
    local_regex_branches=filter_all_regex_branches_from_location(regex_branches, "local")

    if all_version_tags:
        latest_release_tag=all_version_tags[-1]

        regex_support_branches=get_branch_type_from_location("support", "local", regex_branches)
        regex_hotfix_branches=get_branch_type_from_location("hotfix", "local", regex_branches)

        if not master_version_file_value:
            msg.user_error("Master branch version.txt has a no value whereas:")
            if all_version_tags:
                msg.user_error("There is at least a release tag 'v"+", v".join(all_version_tags)+"'")
            if regex_support_branches:
                msg.user_error("At least one support branch is present '["+", ".join(br.text for br in regex_support_branches)+"]'")
            if regex_hotfix_branches:
                msg.user_error("At least one hotfix branch is present '["+", ".join(br.text for br in regex_hotfix_branches)+"]'")
            sys.exit(1)


        start_branch=git.get_active_branch_name()
        for regex_branch in local_regex_branches:
            git.checkout(regex_branch.text)
            # each branch must have a version.txt file
            version_value=version.get_content_version_file(True)
            if not version_value:
                git.checkout(start_branch)
                sys.exit(1)

            regex_version_value=ro.Version_regex(version_value)
            if not regex_version_value.match:
                msg.user_error(
                    "Version value in version.txt is equal to '"+regex_version_value.text+"'",
                    "It should be equal to the form "+regex_version_value.string                    
                )
                git.checkout(start_branch)
                sys.exit(1)

            
            if regex_branch.type == "master" or regex_branch.type == "develop":
                if regex_version_value.text != latest_release_tag:
                    msg.user_error(
                        "Value '"+regex_version_value.text+"' in version.txt from "+regex_branch.type+" branch is different than latest release tag 'v"+latest_release_tag+"'")
                    git.checkout(start_branch)
                    sys.exit(1)
            elif regex_branch.type == "feature":
                # no check on feature branch
                pass
            elif regex_branch.type == "support":
                match_branch_name_with_version_value(regex_branch, regex_version_value)
                find_related_tag_for_support_branch_name(regex_branch, all_version_tags)
            elif regex_branch.type == "hotfix":
                match_branch_name_with_version_value(regex_branch, regex_version_value)
                check_hotfix_is_either_on_master_or_on_support(regex_branch, all_version_tags, regex_support_branches)
            elif regex_branch.type == "release":
                match_branch_name_with_version_value(regex_branch, regex_version_value)

        git.checkout(start_branch)
        
    else: # not all_version_tags
        start_branch=git.get_active_branch_name()
        for regex_branch in local_regex_branches:
            regex_branch.type=ro.get_element_regex(regex_branch.text).type
            if regex_branch.type in ["master", "develop", "feature"]:
                git.checkout(regex_branch.text)
                version_file_path=version.get_file_path()
                if os.path.exists(version_file_path):
                    msg.user_error(
                        "The project has no release tags",
                        " Branch '{}' shouldn't have a version.txt file.".format(regex_branch.text)
                    )
                    git.checkout(start_branch)
                    sys.exit(1)
            elif regex_branch.type in ["release"]:
                # release type branch_name is checked after with validate_release_branch_name
                pass
                # validate_release_branch_name(reg_branches, all_version_tags):
            elif regex_branch.type in ["hotfix", "support",]:
                msg.user_error(
                    "The project has no release tags",
                    " Branch '{}' shouldn't exist.".format(regex_branch.text)
                )
                sys.exit(1)

        git.checkout(start_branch)
    
    msg.dbg("success", sys._getframe().f_code.co_name)

# version_value major and minor must equals branch [hotfix or support] name major and minor
def match_branch_name_with_version_value(regex_branch, regex_version_value):
    regex_match=False
    if regex_branch.type in ["support","hotfix"]:
        print("# "+regex_branch.major_minor)
        print("# "+regex_version_value.major_minor)
        if regex_branch.major_minor == regex_version_value.major_minor:
            regex_match=True
    elif regex_branch.type == "release":
        if regex_branch.version == regex_version_value.text:
            regex_match=True

    if regex_match:
        msg.success("branch "+regex_branch.text+" name matches with its version.txt "+regex_version_value.text)
    else:
        msg.user_error("branch "+regex_branch.text+" name does not match with its version.txt "+regex_version_value.text)
        sys.exit(1)

def check_bump_release_version_script():
    from utils.json_config import Json_config
    msg.subtitle("Check bump release version script.")
    bump_release_version_script_err_msg="""
    Create a script file bump_release_version.sh or bump_release_version.py
        This file needs to be located at:
            - scripts directory,in parent directory of src directory.
        The script should do the following:
            - It receives a release_version from git frame.
            - Then this value is set in a file defined by the developer
            - This value is then going to be retrieved by the user.
            - Generally the user retrieves the release version by executing 
              the software with -v parameter.
            - For gitframe the release version is stored in config.json but
              it can really be anywhere.
            - That is the purpose of this script.
            - The release_version stored for the user is somewhat different
              than the version stored in version.txt.
            - version.txt is automatically managed by gitframe and is necessary
              to maintain the software structure.
            - In short:
                . version.txt is for the source code of the software that is
                  read and maintained by the developers.
                . bump_release_version script insert the software version for
                  release and early_release purpose and it is read by the 
                  software users.
            - Early release version is never stored in version.txt whereas it
              is stored in config.json for gitframe.
            - However release version is always stored in version.txt and also 
              in config.json.
            - bump_release_version script is automatically called by gitframe 
              just before setting an annotated tag for publishing a release or an
              early_release.
    """
    conf = Json_config()
    filer_bump_release_version=conf.get_value("filer_bump_release_version")
    direpa_parent = os.path.abspath('..')

    filerpa_bump_release_version=os.path.join(direpa_parent, conf.get_value("diren_scripts"), filer_bump_release_version)

    filenpa_bump_release_version=""
    if os.path.exists(filerpa_bump_release_version+".py"):
        filenpa_bump_release_version=filerpa_bump_release_version+".py"
    elif os.path.exists(filerpa_bump_release_version+".sh"):
        filenpa_bump_release_version=filerpa_bump_release_version+".sh"
    else:
        filenpa_bump_release_version=""

    if filenpa_bump_release_version:
        is_cmd_executable= os.access(filenpa_bump_release_version, os.X_OK)
        if not is_cmd_executable:
            msg.user_error("script "+filer_bump_release_version+" is not executable")
            sys.exit(1)

        msg.dbg("success", sys._getframe().f_code.co_name)
        
    else:
        msg.warning(bump_release_version_script_err_msg[1:])
        sys.exit(1)
