#!/usr/bin/env python3
import utils.message as msg
from utils.format_text import Format_text as ft
import git_helpers.git_utils as git
import git_helpers.version as version
from git_helpers.get_all_branch_regexes import get_branch_type_from_location
from git_helpers.publish_release import publish_release
import sys
import time
import git_helpers.regex_obj as ro
from git_helpers.get_all_version_tags import get_all_version_tags


def publish_early_release(repo, regex_branches):
    msg.subtitle("Publish Early Version")

    regex_branch=ro.get_element_regex()

    if regex_branch.type in ["release","develop","feature"]:
        version_value=""
        regex_release_branches=get_branch_type_from_location("release", "local", regex_branches)

        msg.dbg("info", "branch_type: "+regex_branch.type)
    
        if regex_branch.type in ["release"]:
            version_value=regex_branch.version
        elif regex_branch.type in ["feature","develop"]:
            if len(regex_release_branches) == 0:
                msg.dbg("info", "no release branches existing")
                version_value=version.get_content_version_file(False, "master")
                if not version_value:
                    msg.dbg("info", "no version_value")
                    version_value="1.0.0"
                else:
                    msg.dbg("info", "version_value")
                    version_value=get_increment_version(version_value)
            elif len(regex_release_branches) == 1:
                msg.dbg("info", "release branches existing")
                version_value=version.get_content_version_file(False, regex_release_branches[0].text)

                if regex_branch.type in ["feature"]:
                    version_value=get_increment_version(version_value)
       
        release_type=get_early_release_type(regex_branch.type, version_value)
        version_value+="-"+release_type
 
        time_stamp=str(int(time.time()))
        version_value+="-"+time_stamp
        git.set_annotated_tags(repo, "v"+version_value, "early-release")

        publish_release(version_value, get_all_version_tags(), "early_release")
    else:
        msg.user_error(
            "Publish early version only applies to 'develop', 'feature' or 'release' branch type.",
            "Checkout on one of this branch and restart command.")
        sys.exit(1)

def get_early_release_type(branch_type, tag):
    if branch_type in ["develop", "feature"]:
        return "alpha"
    else:
        menu="""
            1 - alpha: incomplete version
            2 - beta: complete(heavy testing needed)
            3 - release-candidate: complete(light testing needed)

            Choose an early release type for tag '{tag}' or 'q' to quit: """.format(tag=tag)

        user_choice=""
        while not user_choice:
            user_choice = input(menu)
            if user_choice == "1":
                return "alpha"
            elif user_choice == "2":
                return "beta"
            elif user_choice == "3":
                return "rc"
            elif user_choice.lower() == "q":
                sys.exit(1)
            else:
                msg.user_error("Wrong input")
                input("  Press Enter To Continue...")
                user_choice=""
                # clear terminal 
                ft.clear_screen()

def get_increment_version(tag):
    menu="""
        1 - Major
        2 - Minor

        Choose an increment type for tag '{tag}' or 'q' to quit: """.format(tag=tag)

    user_choice=""
    while not user_choice:
        user_choice = input(menu)
        if user_choice == "1":
            return version.increment_version_value("major", ro.Version_regex(tag))
        elif user_choice == "2":
            return version.increment_version_value("minor", ro.Version_regex(tag))
        elif user_choice.lower() == "q":
            sys.exit(1)
        else:
            msg.user_error("Wrong input")
            input("  Press Enter To Continue...")
            user_choice=""
            # clear terminal 
            ft.clear_screen()
