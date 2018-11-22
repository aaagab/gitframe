#!/usr/bin/env python3
import os
import sys
import re

import utils.message as msg
from utils.format_text import Format_text as ft

from utils.prompt import prompt_boolean
import git_helpers.git_utils as git

import git_helpers.version as version

from git_helpers.get_all_branch_regexes import get_branch_type_from_location
from git_helpers.get_all_version_tags import get_all_version_tags

from git_helpers.publish_release import publish_release

import git_helpers.regex_obj as ro

def open_release(repo, regex_branches):
    msg.subtitle("Open Release Branch")

    regex_release_branches=get_branch_type_from_location("release", "local", regex_branches)

    if len(regex_release_branches) == 0:
        git.checkout("develop")

        master_version_value=version.get_content_version_file(False, "master")
        regex_curr_tag=ro.Version_regex(master_version_value)
        
        new_tag=""
        if not regex_curr_tag.match:
            new_tag="1.0.0"
        else:
            new_tag=get_increment_type(regex_curr_tag)        
        
        release_branch_name=ro.Release_regex().get_new_branch_name(new_tag)
        git.checkoutb(release_branch_name)
        git.commit("Opening Branch "+release_branch_name)
        git.push_origin(repo, release_branch_name)

        msg.dbg("success", sys._getframe().f_code.co_name)
            
    else: # release.local_branch_num == 1
        msg.user_error(
            "A release Branch Can't be Created when another release branch Already Exists.", 
            "Close the following release branch '"+regex_release_branches[0].text+"' and retry the operation."
        )
        sys.exit(1)

def get_increment_type(regex_curr_tag):
    menu="""
        1 - Major
        2 - Minor

        Choose an increment type for tag '{tag}' or 'q' to quit: """.format(tag=regex_curr_tag.text)

    user_choice=""
    while not user_choice:
        user_choice = input(menu)
        if user_choice == "1":
            return version.increment_version_value("major", regex_curr_tag)
        elif user_choice == "2":
            return version.increment_version_value("minor", regex_curr_tag)
        elif user_choice.lower() == "q":
            sys.exit(1)
        else:
            msg.user_error("Wrong input")
            input("  Press Enter To Continue...")
            user_choice=""
            # clear terminal 
            ft.clear_screen()

# can other materials be added to develop when a release branch is under construction?
def close_release(repo, branch_regex, regex_branches, all_version_tags):
    msg.subtitle("Close Release Branch "+branch_regex.text)

    regex_hotfix_branches=get_branch_type_from_location("hotfix", "local", regex_branches)

    if all_version_tags:
        if has_latest_release_an_hotfix(all_version_tags, regex_hotfix_branches):
            msg.user_error("An hotfix is already present on latest release, you must close the hotfix before you can close the release branch '"+branch_regex.text+"'")
            sys.exit(1)

    prompt_boolean("All developpers involved in the project should approve this action. Do you want to Continue?")

    release_version=ro.Release_regex(branch_regex.text).version
    
    version.bump_version_in_version_txt(release_version)
    version.bump_version_for_user(release_version)
    
    git.checkout("develop")
    git.merge_noff(branch_regex.text)
    git.push_origin(repo, "develop")
    
    git.checkout("master")
    git.merge_noff(branch_regex.text)
    git.set_annotated_tags(repo, "v"+release_version, "release")
    git.push_origin(repo, "master")

    prompt_boolean("  "+branch_regex.text+" has to be deleted on local and remote.\n  Continue?")
    git.delete_local_branch(branch_regex.text)

    git.delete_origin_branch(repo, branch_regex.text)

    publish_release(release_version, "release", get_all_version_tags())

    git.checkout("develop")
    
    msg.success(branch_regex.text+" has been closed.")

def has_latest_release_an_hotfix(all_version_tags, regex_hotfix_branches):
    if regex_hotfix_branches:
        regex_latest_release_tag=ro.Version_regex(all_version_tags[-1])

        for regex_hotfix_branch in regex_hotfix_branches:
            if regex_hotfix_branch.major_minor == regex_latest_release_tag.major_minor:
                return True
        return False
    else:
        return False
