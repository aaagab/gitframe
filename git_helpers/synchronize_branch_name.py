
#!/usr/bin/env python3
import os
import re
import sys

from . import git_utils as git
from . import msg_helpers as msgh
from . import regex_obj as ro

from ..gpkgs import message as msg

from ..gpkgs.prompt import prompt_boolean
from ..gpkgs.format_text import ft
from ..gpkgs import shell_helpers as shell

def synchronize_branch_name(repo, regex_branches, branch_name=""):
    
    if not branch_name: 
        branch_name=git.get_active_branch_name()

    start_branch=git.get_active_branch_name()

    msgh.title("Synchronize Branch "+branch_name)

    branch_on={
        "local": False,
        "local_remote": False,
        "remote": False,
    }
    if regex_branches:
        for regex_branch in regex_branches:
            if regex_branch.text == branch_name:
                if regex_branch.location == "local":
                    branch_on["local"]=True
                elif regex_branch.location == "local_remote":
                    branch_on["local_remote"]=True
                elif regex_branch.location == "remote":
                    branch_on["remote"]=True
    else:
        branch_on=get_branch_on(repo, branch_name)

    msg.dbg("info", "Local | Local_Remote | Remote Branch")
    msg.dbg("info","{}_{}_{}".format(branch_on["local"],branch_on["local_remote"],branch_on["remote"]))

    if branch_on["remote"]:
        if branch_on["local_remote"] and branch_on["local"]:
            synchronize_local_with(
                "local_remote", 
                branch_name,
                get_branch_compare_status_repository("local_remote", branch_on, branch_name))
            synchronize_local_with(
                "remote", 
                branch_name,
                get_branch_compare_status_repository("remote", branch_on, branch_name))
        elif branch_on["local_remote"] and not branch_on["local"]:
            synchronize_local_with(
                "local_remote", 
                branch_name,
                get_branch_compare_status_repository("local_remote", branch_on, branch_name))
            synchronize_local_with(
                "remote", 
                branch_name,
                get_branch_compare_status_repository("remote", branch_on, branch_name))
        elif not branch_on["local_remote"] and branch_on["local"]:
            msg.warning(
                "Branch exists on local and on remote but not on local_remote.",
                "Branches are probably different, check manually the authors and commits and decide if you rename one branch or if you want to merge them."
            )
            sys.exit(1)
        elif not branch_on["local_remote"] and not branch_on["local"]:
            synchronize_local_with(
                "remote", 
                branch_name,
                get_branch_compare_status_repository("remote", branch_on, branch_name))
    else: # no remote
        if repo.is_reachable:
            if branch_on["local_remote"] and branch_on["local"]:
                branch_type=ro.get_element_regex(branch_name).type
                if not branch_type in ["master", "develop"]:
                    msg.info("Branch '"+branch_name+"' has probably been deleted on Remote. If it is case you should delete it on local and local_remote.")

                    git_pretty_log(branch_name)
                    if prompt_boolean("Do you want to delete '"+branch_name+"' from local?", "n"):
                        git.checkout("develop")
                        shell.cmd_prompt("git branch -D "+branch_name)
                        if git.is_branch_on_local(start_branch):
                            git.checkout(start_branch)
                        branch_on["local"]=False
                
                    git_pretty_log("origin/"+branch_name)
                    if prompt_boolean("Do you want to delete '"+branch_name+"' from local_remote?", "n"):
                        git.checkout("develop")
                        shell.cmd_prompt("git branch -rD origin/"+branch_name)
                        if git.is_branch_on_local(start_branch):
                            git.checkout(start_branch)
                        branch_on["local_remote"]=False

                synchronize_local_with(
                    "local_remote", 
                    branch_name,
                    get_branch_compare_status_repository("local_remote", branch_on, branch_name))
                synchronize_local_with(
                    "remote", 
                    branch_name,
                    get_branch_compare_status_repository("remote", branch_on, branch_name))
            elif branch_on["local_remote"] and not branch_on["local"]:
                branch_type=ro.get_element_regex(branch_name).type
                if not branch_type in ["master", "develop"]:
                    msg.info("Branch '"+branch_name+"' has probably been deleted on Remote. If it is case you should delete it on local_remote.")

                git_pretty_log("origin/"+branch_name)
                if prompt_boolean("Do you want to delete '"+branch_name+"' from local_remote?", "n"):
                    git.checkout("develop")
                    shell.cmd_prompt("git branch -rD origin/"+branch_name)
                    if git.is_branch_on_local(start_branch):
                        git.checkout(start_branch)
                    branch_on["local_remote"]=False

                synchronize_local_with(
                    "local_remote", 
                    branch_name,
                    get_branch_compare_status_repository("local_remote", branch_on, branch_name))
                synchronize_local_with(
                    "remote", 
                    branch_name,
                    get_branch_compare_status_repository("remote", branch_on, branch_name))
            elif not branch_on["local_remote"] and branch_on["local"]:
                synchronize_local_with(
                    "remote", 
                    branch_name,
                    get_branch_compare_status_repository("remote", branch_on, branch_name))
            elif not branch_on["local_remote"] and not branch_on["local"]:
                msg.warning("Branch does not exists on local, local_remote and remote.")
                msg.warning("No action needed for 'synchronize' on '"+branch_name+"'")
        else: # remote is not reachable
            msg.warning("Remote is not reachable thus it is not possible to compare local branch with remote branch.")
            if branch_on["local_remote"] and branch_on["local"]:
                synchronize_local_with(
                    "local_remote", 
                    branch_name,
                    get_branch_compare_status_repository("local_remote", branch_on, branch_name))
            elif branch_on["local_remote"] and not branch_on["local"]:
                synchronize_local_with(
                    "local_remote", 
                    branch_name,
                    get_branch_compare_status_repository("local_remote", branch_on, branch_name))
            elif not branch_on["local_remote"] and branch_on["local"]:
                msg.warning("Branch only exists on local and remote is not reachable.")
                msg.warning("No action needed for 'synchronize' on '"+branch_name+"'")
            elif not branch_on["local_remote"] and not branch_on["local"]:
                msg.warning("Branch does not exists on local, local_remote and remote can't be verified due to offline mode.")
                msg.warning("No action needed for 'synchronize' on '"+branch_name+"'")

def git_pretty_log(branch_name):
    print()
    msg.info("Git Pretty '"+branch_name+"'")
    shell.cmd("git log --graph --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset' --abbrev-commit --date=relative "+branch_name)
    print()

def get_value_from_menu(values, branch_name):
    menu="\n"

    for i, value in enumerate(values):
        menu+="    "+str(i+1)+" => "+value+"\n"

    menu+="\n"
    menu+="    Choose an action for branch '"+branch_name+"'.\n"
    menu+="    choice or 'q' to quit: "

    user_choice=""
    while not user_choice:
        isValid=True
        user_choice = input(menu)
        if user_choice.isdigit():
            if int(user_choice) >= 1 and int(user_choice) <= len(values):
                return values[int(user_choice)-1]
            else:
                isValid=False
        elif user_choice.lower() == "q":
            sys.exit(1)
        else:
            isValid=False

        if not isValid:
            msg.warning("Wrong input")
            input("  Press Enter To Continue...")
            user_choice=""
            # clear terminal 
            ft.clear_screen()

def get_branch_on(repo, branch_name):
    msg.dbg("subtitle", "get_branch_on "+branch_name)
    remote=""
    if repo.is_reachable:
        if git.is_branch_on_remote(branch_name):
            remote=True
        else:
            remote=False
    else:
        remote=False
    branch_on={
            "local": git.is_branch_on_local(branch_name),
            "local_remote": git.is_branch_on_local_remote(branch_name),
            "remote": remote
        }

    msg.dbg("info", "Local | Local_Remote | Remote Branch")
    msg.dbg("info","branch_on {}_{}_{}".format(branch_on["local"], branch_on["local_remote"], branch_on["remote"]))
        
    return branch_on

def synchronize_local_with(location, branch_name, cmp_status):
    msg.dbg("subtitle", "synchronize_local_with '"+location+"' for '"+branch_name+"'")
       
    msg.info("cmp_status: "+cmp_status)
    if cmp_status == "up_to_date":
        msg.success("No action needed for 'synchronize' with \""+branch_name+"\" on \""+location+"\"")
    elif cmp_status == "pull":
        if location == "local_remote":
            action=get_value_from_menu(["merge", "ignore", "exit"], branch_name)
            execute_action(action, branch_name)
        elif location == "remote":
            action=get_value_from_menu(["pull", "ignore", "exit"], branch_name)
            execute_action(action, branch_name)
    elif cmp_status == "pull_not_local":
        branch_type=ro.get_element_regex(branch_name).type
        if location == "local_remote":
            # if branch_type in ["master", "develop"]:
                # action=get_value_from_menu(["merge", "ignore", "exit"], branch_name)
                # execute_action(action, branch_name)
            # else:
                msg.warning("Branch '"+branch_name+"' is on local_remote but not on local. No need to checkout.")
                msg.success("No action needed for 'synchronize' with \""+branch_name+"\" on \""+location+"\"")
        elif location == "remote":
            if git.is_branch_on_local_remote(branch_name):
                msg.success("No action needed for 'synchronize' with \""+branch_name+"\" on \""+location+"\"")
            else:
                action=get_value_from_menu(["fetch", "ignore", "exit"], branch_name)
                execute_action(action, branch_name)

    elif cmp_status == "push":
        if location == "local_remote":
            msg.warning("Push is never done to local_remote branches, local is already the newest")
            msg.success("No action needed for 'synchronize' with \""+branch_name+"\" on \""+location+"\"")
        elif location == "remote":
            action=get_value_from_menu(["push", "ignore", "exit"], branch_name)
            execute_action(action, branch_name)
    elif cmp_status == "null":
        if location == "local_remote":
            msg.warning("Branch '"+branch_name+"' does not exist on local nor on local_remote.")
        elif location == "remote":
            msg.warning("Branch '"+branch_name+"' does not exist on local nor on remote.")

        msg.success("No action needed for 'synchronize' with \""+branch_name+"\" on \""+location+"\"")
    else:
        if cmp_status == "divergent_with_common_ancestor":
            msg.info(
                "Remote and local branch for "+branch_name+" are divergent WITH a common ancestor.",
                "A simple git merge origin/"+branch_name+" can be enough.",
                "Else use git mergetool, repair conflict manually, commit the changes.",
                "Run all the tests on code",
                "Then git push origin "+branch_name
            )
            msg.dbg("success", "divergent_with_common_ancestor")
            sys.exit(1)
        elif cmp_status == "divergent_without_common_ancestor":
            msg.info(
                "Origin and local branch for "+branch_name+" are divergent WITHOUT a common ancestor.",
                "It is a special case",
                "Try to git merge origin/"+branch_name,
                "Then use git mergetool, repair conflict manually, commit the changes.",
                "Run all the tests on code",
                "Then git push origin "+branch_name
            )
            msg.dbg("success", "divergent_without_common_ancestor")
            sys.exit(1)

def execute_action(action, branch_name):
    if action == "exit":
        msg.error("Operation cancelled 'synchronize' branch '"+branch_name+"'")
        sys.exit(1)
    elif action == "ignore":
        msg.warning("Operation ignored 'synchronize' branch '"+branch_name+"'")
    elif action == "fetch":
        shell.cmd_prompt("git fetch origin "+branch_name)
    elif action == "pull":
        previous_branch=git.get_active_branch_name()
        if git.is_branch_on_local(branch_name):
            git.checkout(branch_name)
            shell.cmd_prompt("git pull origin "+branch_name)
        else:
            shell.cmd_prompt("git fetch origin "+branch_name)
            git.checkout(branch_name)
            git.checkout(previous_branch)
    elif action == "push":
        shell.cmd_prompt("git push origin "+branch_name)
    elif action == "merge":
        previous_branch=git.get_active_branch_name()
        git.checkout(branch_name)
        git.merge(branch_name)
        git.checkout(previous_branch)
    else:
        msg.error("Action unknown "+action+" for operation 'synchronize' on branch "+branch_name)
        sys.exit(1)

def get_branch_compare_status_repository(location, branch_on, branch_name="" ):
   
    if not branch_name:
        branch_name=git.get_active_branch_name()

    msg.dbg("subtitle", "get_branch_compare_status_repository '"+location+"' for '"+branch_name+"'")

    if location == "local_remote":
        msg.info("Compare branch: \""+ branch_name + "\" local to \"origin/"+branch_name+"\"")
        if branch_on["local_remote"] and branch_on["local"]:
            return git.get_branch_compare_status(branch_name, "origin/"+branch_name)
        elif branch_on["local_remote"] and not branch_on["local"]:
            return "pull_not_local"
        elif not branch_on["local_remote"] and branch_on["local"]:
            return "push"
        elif not branch_on["local_remote"] and not branch_on["local"]:
            msg.warning("Branch '"+branch_name+"' does not exist on local and local_remote. Compare Status can't be set for local and local_remote.")
            return "null"

    elif location == "remote":
        msg.info("Compare branch: \""+ branch_name + "\" local to \"origin\"")
        if branch_on["remote"] and branch_on["local"]:
            shell.cmd_prompt("git fetch origin "+branch_name)
            return git.get_branch_compare_status(branch_name, "origin/"+branch_name)
        elif branch_on["remote"] and not branch_on["local"]:
            return "pull_not_local"
        elif not branch_on["remote"] and branch_on["local"]:
            return "push"
        elif not branch_on["remote"] and not branch_on["local"]:
            msg.warning("Branch '"+branch_name+"' does not exist on local and remote. Compare Status can't be set for local and remote.")
            return "null"
        
    # local_last_commit=shell.cmd_get_value("git rev-parse "+branch_name)
    # remote_last_commit=shell.cmd_get_value("git rev-parse origin/"+branch_name)
    # common_ancestor_local_remote=shell.cmd_get_value("git merge-base "+branch_name+" origin/"+branch_name)
    
    # if local_last_commit == remote_last_commit:
    #     return "up_to_date"
    # elif local_last_commit == common_ancestor_local_remote:
    #     return "pull"
    # elif remote_last_commit == common_ancestor_local_remote:
    #     return "push"
    # else:
    #     if common_ancestor_local_remote:
    #         return "divergent_with_common_ancestor"
    #     else:
    #         return "divergent_without_common_ancestor"
