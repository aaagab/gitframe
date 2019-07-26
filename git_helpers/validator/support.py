#!/usr/bin/env python3
import sys

from .. import git_utils as git
from .. import regex_obj as ro

from ...gpkgs import message as msg


# there is no support branch on releases that has the latest major
# if one support branch it must be on the latest release of previous major releases
# Support Branch name needs to be the same on local and remote

def find_related_tag_for_support_branch_name(regex_branch, all_version_tags):
    latest_release_tags=git.get_latest_release_for_each_major(all_version_tags)
    
    found=False
    regex_release=ro.Version_regex()
    for release in latest_release_tags:
        regex_release.set_text(release)
        if regex_branch.major == regex_release.major:
            found=True
            break

    if not found:
        msg.error(
            "Support Branch name '"+regex_branch.text+"' does not contain tag from one of the latest releases '"+', '.join(latest_release_tags)+"' that matches its Major Number",
            "Please rename Support branch_name to match the tag of the latest release on one Major."    
        )
        sys.exit(1)
    else:
        regex_latest_release=ro.Version_regex(latest_release_tags[-1])

        # there is no support branch on releases that has the latest major
        if regex_latest_release.major == regex_branch.major:
            msg.error(
                "Support branch name major '"+regex_branch.text+"' can't be equal to Latest release Major from '"+regex_latest_release.text+"'",
                "No support branch on latest major version is tolerated."
            )
            sys.exit(1)

    msg.dbg("success", sys._getframe().f_code.co_name)
