#!/usr/bin/env python3
import utils.message as msg
import utils.shell_helpers as shell
import sys
from utils.format_text import Format_text as ft
from git_helpers.branch.feature import open_feature
from git_helpers.branch.release import open_release
from git_helpers.branch.hotfix import open_hotfix
from git_helpers.branch.support import open_support

def open_branch(repo, regex_branches, all_version_tags):
    msg.title("Open Branch")

    user_choice=get_menu_branch_types()
    if user_choice == "feature":
        open_feature(repo)
    elif user_choice == "release":
        open_release(repo, regex_branches)
    elif user_choice == "hotfix":
        open_hotfix(repo, all_version_tags)
    elif user_choice == "support":
        open_support(repo, regex_branches, all_version_tags)

def get_menu_branch_types():
    menu="""
        1 - Feature
        2 - Release
        3 - Hotfix
        4 - Support

        Choose a Branch Type or 'q' to quit: """

    user_choice=""
    while not user_choice:
        user_choice = input(menu)
        if user_choice == "1":
            return "feature"
        elif user_choice == "2":
            return "release"
        elif user_choice == "3":
            return "hotfix"
        elif user_choice == "4":
            return "support"
        elif user_choice.lower() == "q":
            sys.exit(1)
        else:
            msg.user_error("Wrong input")
            input("  Press Enter To Continue...")
            user_choice=""
            # clear terminal 
            ft.clear_screen()
