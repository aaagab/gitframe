#!/usr/bin/env python3
import re
import sys

from .. import msg_helpers as msgh
from .. import regex_obj as ro

from ...gpkgs import message as msg


# master branch has to exist on local
# develop branch has to exist on local
# then the other branch have to follow regex rules

def check_master_develop_exists(regex_branches):
    msgh.subtitle("master and develop branches presence on local or on local remote")

    master_found=False
    develop_found=False
    for reg_branch in regex_branches:
        if reg_branch.location == "local" or reg_branch.location == "local_remote":
            if reg_branch.text == "master":
                master_found=True
            elif reg_branch.text == "develop":
                develop_found=True

            if master_found and develop_found:
                break

    if not master_found:
        msg.error("Branch \"master\" does not exist as a local branch.")
        sys.exit(1)
    
    if not develop_found:
        msg.error("Branch \"develop\" does not exist as a local branch.")
        sys.exit(1)

    msg.dbg("success", sys._getframe().f_code.co_name)

    