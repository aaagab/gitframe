#!/usr/bin/env python3
import utils.message as msg
import git_helpers.git_utils as git
import re
import sys
import git_helpers.regex_obj as ro

def get_branch_type_from_location(branch_type, location, reg_branches):
    msg.dbg("info","Search for '{}' branches of type '{}'".format(location, branch_type))

    reg_objs=[]

    for reg_branch in reg_branches:
        if location == "all":
            if reg_branch.type == branch_type:
                reg_objs.append(reg_branch)
        else:
            if reg_branch.location == location:
                if reg_branch.type == branch_type:
                    reg_objs.append(reg_branch)
    return reg_objs

def filter_all_regex_branches_from_location(reg_branches, location):
    msg.dbg("info","Get All local branches")

    reg_objs=[]

    for reg_branch in reg_branches:
        if reg_branch.location == location:
            reg_objs.append(reg_branch)

    return reg_objs

def get_all_branch_regexes(repo):
    regex_branches=[]
    if repo.is_reachable:
        if repo.has_directory:
            for branch_name in git.get_heads_remote_branch_names(repo):
                reg_obj=ro.get_element_regex(branch_name)
                reg_obj.location="remote"
                regex_branches.append(reg_obj)
        else:
            msg.warning("Branches on Remote Cannot be retrieved.",
                "Validator is going to be partially executed.")
    else:
        msg.warning("Branches on Remote Cannot be retrieved.",
                "Validator is going to be partially executed.")

    for branch_name in git.get_local_branch_names():
        reg_obj=ro.get_element_regex(branch_name)
        reg_obj.location="local"
        regex_branches.append(reg_obj)

    for branch_name in git.get_local_remote_branch_names():
        reg_obj=ro.get_element_regex(branch_name)
        reg_obj.location="local_remote"
        regex_branches.append(reg_obj)

    return regex_branches
