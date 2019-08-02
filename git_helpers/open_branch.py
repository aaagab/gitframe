#!/usr/bin/env python3
import sys

from . import msg_helpers as msgh

from .branch.draft import open_draft
from .branch.features import open_features
from .branch.hotfix import open_hotfix
from .branch.support import open_support

from ..gpkgs import message as msg
from ..gpkgs import shell_helpers as shell
from ..gpkgs.format_text import ft

def open_branch(repo, regex_branches, all_version_tags):
    msgh.title("Open Branch")

    user_choice=get_menu_branch_types()
    if user_choice == "features":
        open_features(repo)
    elif user_choice == "draft":
        open_draft(repo)
    elif user_choice == "hotfix":
        open_hotfix(repo, all_version_tags)
    elif user_choice == "support":
        open_support(repo, regex_branches, all_version_tags)

def get_menu_branch_types():
    menu="""
        1 - Features
        2 - Draft
        3 - Hotfix
        4 - Support

        Choose a Branch Type or 'q' to quit: """

    user_choice=""
    while not user_choice:
        user_choice = input(menu)
        if user_choice == "1":
            return "features"
        elif user_choice == "2":
            return "draft"
        elif user_choice == "3":
            return "hotfix"
        elif user_choice == "4":
            return "support"
        elif user_choice.lower() == "q":
            sys.exit(1)
        else:
            msg.warning("Wrong input")
            input("  Press Enter To Continue...")
            user_choice=""
            # clear terminal 
            ft.clear_screen()
