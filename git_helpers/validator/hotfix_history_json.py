#!/usr/bin/env python3
import os
import sys
import re

import utils.message as msg
import git_helpers.git_utils as git
import git_helpers.version as version

import utils.shell_helpers as shell

from utils.json_config import Json_config

from copy import deepcopy

from git_helpers.get_all_branch_regexes import filter_all_regex_branches_from_location
import git_helpers.regex_obj as ro

# check hotfix-history.json
    # for each hotfix, 
        # if hotfix is closed and branch is still present
        # if hotfix is open and branch is not present
        # if hotfix is present but no related tag on hotfix-history.json
        # For all tags on local check each tag from history.json is present, start and end. otherwise error
        # for each hotfix tag in git tag, check that tag is present in at least one history-json from support, hotfix, master

# you cannot have hotfix id duplicate in json

def hotfix_history_json_validator(regex_branches):
    conf = Json_config()
    filen_hotfix_history=conf.get_value("filen_hotfix_history")

    tags=shell.cmd_get_value("git tag").splitlines()
    hotfix_tags=get_hotfix_tags_from_tags(tags)

    start_branch=git.get_active_branch_name()

    regex_branches_to_monitor=[]
    for regex_branch in filter_all_regex_branches_from_location(regex_branches, "local"):
        if regex_branch.type in ["master", "hotfix", "support"]:
            msg.dbg("info","match type "+regex_branch.type)
            regex_branches_to_monitor.append(regex_branch)
            git.checkout(regex_branch.text)
            
            if not os.path.exists(filen_hotfix_history):
                msg.user_error(filen_hotfix_history+" should be present on " + regex_branch.text)
                git.checkout(start_branch)
                sys.exit(1)

    print("here1")
    compare_git_tags_to_hotfix_json_tags(regex_branches_to_monitor, hotfix_tags, filen_hotfix_history)
    print("here2")

    for regex_branch in regex_branches_to_monitor:
        git.checkout(regex_branch.text)
        print("here3")
        hotfix_objs=Json_config(filen_hotfix_history).data
        print("here4")

        for obj in hotfix_objs:
            end_tag=hotfix_objs[obj]["end_tag"]
            start_tag=hotfix_objs[obj]["start_tag"]
            
            # for each tag from history.json start and end check that it is found in git tag
            start_tag_found=False
            end_tag_found=False
            for tag in hotfix_tags:
                if start_tag_found==False:
                    if not start_tag:
                        msg.user_error("start_tag not found for hotfix "+obj+" in "+filen_hotfix_history+" from "+regex_branch.text)
                        sys.exit(1)
                    elif tag == start_tag:
                        start_tag_found=True

                if end_tag_found==False:
                    if not end_tag:
                        end_tag_found=True
                    elif tag == end_tag:
                        end_tag_found=True

                if start_tag_found and end_tag_found:
                    break

            if not start_tag_found:
                msg.user_error(start_tag+" from "+filen_hotfix_history+" is not found in git tag")
                sys.exit(1)

            if not end_tag_found:
                msg.user_error(end_tag+" from "+filen_hotfix_history+" is not found in git tag")
                sys.exit(1)
            
            # if hotfix is closed and branch is still present
            hotfix_branch_from_json=obj
            if end_tag:
                if git.is_branch_on_local(hotfix_branch_from_json):
                    msg.user_error(hotfix_branch_from_json+" branch is present whereas it is closed in " + filen_hotfix_history)
                    git.checkout(start_branch)
                    sys.exit(1)
            else:
                # if hotfix is open and branch is not present
                if not git.is_branch_on_local(hotfix_branch_from_json):
                    msg.user_error(hotfix_branch_from_json+" branch is not present whereas it is open in " + filen_hotfix_history)
                    git.checkout(start_branch)
                    sys.exit(1)

        # if hotfix is present but no related tag in hotfix-history.json
        if regex_branch.type == "hotfix":
            hotfix_found=False
            for obj in hotfix_objs:
                hotfix_branch_from_json=obj
                if regex_branch.text == hotfix_branch_from_json:
                    hotfix_found=True
                    break
                    
            if not hotfix_found:
                msg.user_error(regex_branch.text+" branch is present whereas it is not found in one start_tag of its " + filen_hotfix_history)
                git.checkout(start_branch)
                sys.exit(1)

    git.checkout(start_branch)
    msg.dbg("success", sys._getframe().f_code.co_name)

def get_hotfix_tags_from_tags(tags):
    hotfix_tags=[]
    version_regex=ro.Version_regex()
    hotfix_regex=ro.Hotfix_regex()
    for tag in tags:
        string="v"
        if tag[0] == string:
            version_regex.set_text(tag[len(string):])
            if version_regex.match:
                if int(version_regex.patch) > 0:
                    hotfix_tags.append(tag)

        # start-hotfix-1.0.X-version
        string="start-"
        if tag[0:len(string)] == string:
            hotfix_regex.set_text(tag[len(string):])
            if hotfix_regex.match:
                hotfix_tags.append(tag)

    return hotfix_tags

# for each hotfix tag in git tag, check that tag is present in at least one history-json from support, hotfix, master
def compare_git_tags_to_hotfix_json_tags(regex_branches_to_monitor, hotfix_tags, filen_hotfix_history):
    
    msg.dbg("subtitle", "compare_git_tags_to_hotfix_json_tags")

    if not regex_branches_to_monitor:
        return msg.dbg("warning", "no branches to monitor" )
    elif not hotfix_tags:
        return msg.dbg("warning", "no hotfix_tags" )

    hotfix_tags_not_found=deepcopy(hotfix_tags)

    # for each hotfix tag in git tag, check that tag is present in at least one history-json from support, hotfix, master
    hotfix_objs_num=0
    for regex_branch in regex_branches_to_monitor:
        msg.dbg("info", regex_branch.text)
        git.checkout(regex_branch.text)
        hotfix_objs=Json_config(filen_hotfix_history).data            

        if hotfix_objs:
            hotfix_objs_num+=1
        
        for obj in hotfix_objs:
            start_tag=hotfix_objs[obj]["start_tag"]
            end_tag=hotfix_objs[obj]["end_tag"]
            
            for i, tag in enumerate(hotfix_tags):
                if tag in hotfix_tags_not_found:
                    msg.dbg("info","Search for tag "+tag)
                    if tag == start_tag or tag == end_tag:
                        msg.dbg("info", "Found >> "+tag)
                        hotfix_tags_not_found.remove(tag)

            if not hotfix_tags_not_found:
                break

        if not hotfix_tags_not_found:
            break

    if hotfix_objs_num == 0:
        msg.user_error(
            "hotfix tags exist "+"["+", ".join(hotfix_tags_not_found)+"] but no "+filen_hotfix_history+" has objects in at least one of these branches ["+", ".join(br.text for br in regex_branches_to_monitor)+"]"
        )
        sys.exit(1)

    if hotfix_tags_not_found:
        list_tags="["+", ".join(hotfix_tags_not_found)+"]"
        list_branches="["+", ".join(br.text for br in regex_branches_to_monitor)+"]"
        msg.user_error(list_tags+" found in 'git tag' but not in "+filen_hotfix_history+" in at least one of these branches "+list_branches)
        sys.exit(1)
    
    msg.dbg("success", sys._getframe().f_code.co_name)

