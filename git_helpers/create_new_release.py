#!/usr/bin/env python3
import os
import re
import sys

from . import git_utils as git
from . import msg_helpers as msgh

from . import regex_obj as ro
from . import version as version
from .get_all_branch_regexes import get_branch_type_from_location, get_all_branch_regexes
from .get_all_version_tags import get_all_version_tags
from .pick_up_release import pick_up_release
from .remote_repository import Remote_repository

from ..gpkgs import message as msg

from ..gpkgs.format_text import ft
from ..gpkgs.prompt import prompt_boolean, prompt

def get_increment_type(regex_curr_tag):
    menu="""
        1 - Major
        2 - Minor
        3 - Patch

        Choose an increment type for tag '{tag}' or 'q' to quit: """.format(tag=regex_curr_tag.text)

    user_choice=""
    while not user_choice:
        user_choice = input(menu)
        if user_choice == "1":
            return version.increment_version_value("major", regex_curr_tag)
        elif user_choice == "2":
            return version.increment_version_value("minor", regex_curr_tag)
        elif user_choice == "3":
            return version.increment_version_value("patch", regex_curr_tag)
        elif user_choice.lower() == "q":
            sys.exit(1)
        else:
            msg.warning("Wrong input")
            input("  Press Enter To Continue...")
            user_choice=""
            # clear terminal 
            ft.clear_screen()

# can other materials be added to develop when a release branch is under construction?
def create_new_release(repo="", regex_branches="", all_version_tags="", deploy_args=[]):

    branch_name=git.get_active_branch_name()
    branch_regex=ro.get_element_regex(branch_name)

    if not repo:
        repo=Remote_repository()
        regex_branches=get_all_branch_regexes(repo)
        all_version_tags=get_all_version_tags()

    if branch_regex.type != "features":
        msg.error(
            "Non-authorized branch type '{}'".format(branch_regex.type),
            "A new release can only be created from a 'features' branch")
        sys.exit(1)

    msgh.subtitle("Create new release from '{}'".format(branch_regex.text))
    

    # Do I want to decide on what version do I start??? I am not sure
    # If not tag, ask number where to start, fill by default 1.0.0
    regex_release_version=ro.Version_regex("")
    if not all_version_tags:
        print("\n  No release version has been found.")
        while not regex_release_version.match:
            regex_release_version=regex_release_version.set_text(
                prompt("Type release version to start with(ex:0.1.0)")
            )
            if not regex_release_version.match:
                msg.warning("Version release must be of the form '\d+\.\d+\.\d+'")

        regex_release_version.set_text(regex_release_version.major_minor_patch)
    else:
        regex_latest_release=ro.Version_regex(all_version_tags[-1])
        regex_release_version.set_text(get_increment_type(
            regex_latest_release
        ))

        if int(regex_release_version.major) - int(regex_latest_release.major) == 1:
            regex_hotfix_branches=get_branch_type_from_location("hotfix", "local", regex_branches)
            if has_latest_release_an_hotfix(all_version_tags, regex_hotfix_branches):
                msg.warning(
                    "Hotfix branch(es) '[{}]' found.".format(", ".join([reg.text for reg in regex_hotfix_branches])),
                    "It is recommended to close hotfix branch(es) before creating a new version tag"
                    )
                
                if prompt_boolean("Do you want to continue anyway"):
                    # create a support branch from latest release.
                    new_support_branch=ro.Support_regex().get_new_branch_name(regex_latest_release.major)
                    msgh.subtitle("Create Support branch '{}' from latest release '{}'".format(
                        new_support_branch,
                        regex_latest_release.text
                    ))
                    git.checkoutb(new_support_branch+" v"+regex_latest_release.text)
                    git.checkout(branch_regex.text)
                else:
                    msg.warning("Gitframe Create a new release cancelled")
                    sys.exit(1)
                    
    print()
    version.bump_version_for_user(regex_release_version.text)
    git.commit("Bump Release Version "+regex_release_version.text)
    git.push_origin(repo, branch_regex.text)
    
    git.checkout("develop")
    git.merge_noff(branch_regex.text)
    git.push_origin(repo, "develop")
    
    git.checkout("master")
    git.merge_noff(branch_regex.text)
    git.set_annotated_tags(repo, "v"+regex_release_version.text, "release")
    git.push_origin(repo, "master")

    git.checkout(branch_regex.text)

    pick_up_release(regex_release_version.text, deploy_args)

def has_latest_release_an_hotfix(all_version_tags, regex_hotfix_branches):
    if regex_hotfix_branches:
        regex_latest_release_tag=ro.Version_regex(all_version_tags[-1])

        for regex_hotfix_branch in regex_hotfix_branches:
            if regex_hotfix_branch.major == regex_latest_release_tag.major:
                return True
        return False
    else:
        return False
