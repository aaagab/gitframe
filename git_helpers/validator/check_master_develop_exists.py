#!/usr/bin/env python3
import sys
import utils.message as msg
import re

import git_helpers.regex_obj as ro

# master branch has to exist on local
# develop branch has to exist on local
# then the other branch have to follow regex rules

def check_master_develop_exists(regex_branches):
    msg.subtitle("master and develop branch on local")

    master_found=False
    develop_found=False
    for reg_branch in regex_branches:
        if reg_branch.location == "local":
            if reg_branch.text == "master":
                master_found=True
            elif reg_branch.text == "develop":
                develop_found=True

            if master_found and develop_found:
                break
            
    if not master_found:
        msg.user_error("Branch \"master\" does not exist as a local branch.")
        sys.exit(1)
    
    if not develop_found:
        msg.user_error("Branch \"develop\" does not exist as a local branch.")
        sys.exit(1)

    msg.dbg("success", sys._getframe().f_code.co_name)

    