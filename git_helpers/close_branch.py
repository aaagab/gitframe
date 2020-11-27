#!/usr/bin/env python3
import sys

# from . import git_utils as git
from . import msg_helpers as msgh

from . import regex_obj as ro
from .branch.features import close_features
from .branch.draft import close_draft
from .branch.hotfix import close_hotfix
from .get_all_version_tags import get_all_version_tags

from ..gpkgs import message as msg
from ..gpkgs.gitlib import GitLib

def close_branch(repo,
    # regex_branches,
    # all_version_tags,
    branch_name=None,
    commit_message=None,
    direpa_src=None,
):
    msg.title("Close Branch")
    # get branch type
    if branch_name is None:
        branch_name=git.get_active_branch_name()
    else:
        if git.is_branch_on_local(branch_name) == False:
            msg.error(
                "Branch "+branch_name+" already not found on local.",
            )
            sys.exit(1)
    branch_regex=ro.get_element_regex(branch_name)
    if branch_regex.type == "features":
        close_feature(repo, branch_regex, regex_branches, all_version_tags)
    elif branch_regex.type == "draft":
        close_draft(repo, branch_regex)
    elif branch_regex.type == "hotfix":
        close_hotfix(repo, branch_regex, regex_branches, all_version_tags)
    else:
        msg.error(
            "You can't close on branch '"+ branch_name+"'.",
            "git checkout another_branch_type \"features|hotfix\""
        )
        sys.exit(1)