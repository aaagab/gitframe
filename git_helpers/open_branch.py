#!/usr/bin/env python3
import sys

from .branch.draft import open_draft
from .branch.features import open_features
from .branch.hotfix import open_hotfix
from .branch.support import open_support
from . import regex_obj as ro
from .get_all_version_tags import get_all_version_tags
from .prompt_for_commit import prompt_for_commit
from .get_all_branch_regexes import get_all_branch_regexes

from .remote_repository import Remote_repository



from ..gpkgs import message as msg
from ..gpkgs import shell_helpers as shell
from ..gpkgs.format_text import ft
from ..gpkgs.gitlib import GitLib

def open_branch(
    # repo, 
    # regex_branches, 
    # all_version_tags,
    branch_name=None,
    commit_message=None,
    direpa_src=None,
):
    msg.info("Open Branch")

    git=GitLib(direpa=direpa_src)
    git.is_direpa_git(fail_exit=True)
    prompt_for_commit(commit_message=commit_message)
    repo=Remote_repository()

    if branch_name is None:
        branch_type=get_menu_branch_types()
    else:
        reg_branch=ro.get_element_regex(branch_name)

        authorized_branches=["draft", "features"]
        if reg_branch.type not in authorized_branches:
            msg.error("Branch type '{}' not supported to open with chosen name. Only '{}' are available.".format(reg_branch.type, authorized_branches), exit=1)
        branch_type=reg_branch.type

    if branch_type == "features":
        open_features(
            repo,
            branch_name=branch_name
        )
    elif branch_type == "draft":
        open_draft(repo,
            branch_name=branch_name
        )
    elif branch_type == "hotfix":
        open_hotfix(repo, get_all_version_tags())
    elif branch_type == "support":
        open_support(repo, get_all_branch_regexes(repo, git), get_all_version_tags())

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
