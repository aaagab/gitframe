#!/usr/bin/env python3
import sys

from . import msg_helpers as msgh
from .get_all_branch_regexes import get_branch_type_from_location
from .synchronize_branch_name import synchronize_branch_name

from ..gpkgs import message as msg

def synchronize_branch_type(repo, regex_branches, branch_type):
    msgh.subtitle("Synchronize Branch Type "+branch_type)

    # first get all branches of the special type
    # type_reg_branches=get_branch_type_from_location(branch_type, "all", reg_branches)
    # then get all unique names and synchronize each unique name branch

    for regex_branch_name in get_unique_regex_branch_names(regex_branches):
        if regex_branch_name.type == branch_type:
            synchronize_branch_name(repo, regex_branches, regex_branch_name.text)

    msg.dbg("success", sys._getframe().f_code.co_name)

def get_unique_regex_branch_names(reg_branches):
    regex_tmp_branches=[]
    for i, reg_branch in enumerate(reg_branches):
        if i == 0:
            regex_tmp_branches.append(reg_branch)
        else:
            found=False
            for regex_tmp_branch in regex_tmp_branches:
                if regex_tmp_branch.text == reg_branch.text:
                    found=True
                    break
            if not found:
                regex_tmp_branches.append(reg_branch)
    
    return(regex_tmp_branches)
    