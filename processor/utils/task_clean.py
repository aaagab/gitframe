#!/usr/bin/env python3
import os 
import sys
import shutil
import re
from pprint import pprint
import getpass

try:
    from ...git_helpers.remote_repository import Remote_repository
    from ...git_helpers import git_utils as git
    from ...gpkgs import message as msg
    from ...gpkgs import shell_helpers as shell
    from ...git_helpers import msg_helpers as msgh
except:
    direpa_script=os.path.realpath(__file__)
    direpa_launcher=os.path.dirname(os.path.dirname(os.path.dirname(direpa_script)))
    sys.path.insert(0,direpa_launcher)
    from git_helpers.remote_repository import Remote_repository
    from git_helpers import git_utils as git
    from gpkgs import message as msg
    from gpkgs import shell_helpers as shell
    from git_helpers import msg_helpers as msgh


def delete_test_and_repo(conf):
    msgh.subtitle("Cleaning Unit assets")
    os.chdir(conf["direpa_task_conf"])

    if os.path.exists(conf["direpa_task"]):
        shutil.rmtree(conf["direpa_task"])
        msg.success("'"+conf["direpa_task"]+"' deleted.")
    
    if os.path.exists(conf["remote"]["direpa_src"]):
        user_group_repository=shell.cmd_get_value("sudo stat --format '%U:%G' '{}'".format(conf["remote"]["direpa_src"]).strip())
        if user_group_repository != conf["user_current"]+":"+conf["user_current"]:
            shell.cmd_prompt("sudo rm -rf '{}'".format(conf["direpa_repository"]))
        else:
            # shell.cmd_prompt("sudo chown -R  '{}'".format(conf["direpa_repository"]))
            shell.cmd_prompt("sudo rm -rf '{}'".format(conf["direpa_repository"]))
            # shutil.rmtree(conf["direpa_repository"])
   
        msg.success("'"+conf["direpa_repository"]+"' deleted.")
        

def delete_directory_content(path):
    for element in os.listdir(path):
        element_path = os.path.join(path, element)
        try:
            if os.path.isfile(element_path):
                os.unlink(element_path)
            elif os.path.isdir(element_path): 
                shutil.rmtree(element_path)
        except Exception as e:
            msg.app_error("")
            sys.exit(1)

def clean_end_cmds(conf):
    clean_heredoc="""
        git checkout master
        git reset --hard start_master
        git clean -f

        git checkout develop
        git reset --hard start_develop
        git clean -f

        # delete all tags
        git tag | grep -Ev "start_develop|start_master" | xargs git tag -d
        git fetch --tags
        git tag -l | grep -Ev "start_develop|start_master" | xargs -n 1 git push --delete origin
        git tag | grep -Ev "start_develop|start_master" | xargs git tag -d
        git push origin --force master
        git push origin --force develop

        # delete tmp directory for dual directory test
        rm -rf {direpa_task_src}_tmp
        rm {direpa_task}/mock_project || true
    """.format(direpa_task=conf["direpa_task"], direpa_task_src=conf["direpa_task_src"] )

    return re.sub(r'\n\s*','\n',clean_heredoc)[1:-1]

def clean_after_cmd(conf):
    msgh.subtitle("Cleaning Unit")
    path=os.path.join(conf['direpa_task_conf'],conf['diren_task'], conf['diren_src'])
    dev_null=" > /dev/null 2>&1"
    if os.path.exists(path):
        os.chdir(path)
        if os.path.exists(".git"):
            for cmd in clean_end_cmds(conf).splitlines():
                if not cmd[0] == "#":
                    # print("# "+cmd)
                    # os.system(cmd+dev_null)
                    os.system(cmd)
            
            branches=""

            branches={
                "local": git.get_local_branch_names(),
                "local_remote": git.get_local_remote_branch_names(),
                "remote": git.get_heads_remote_branch_names(Remote_repository())
            }

            for branch in branches["local"]:
                if branch != "develop" and branch != "master":
                    os.system("git branch -D "+branch+dev_null)

            for branch in branches["remote"]:
                if branch != "develop" and branch != "master":
                    os.system("git push origin --delete "+branch+dev_null)

            # clean local_remote
            os.system("git fetch --prune"+dev_null)
            os.chdir(conf['direpa_task_conf'])
        else:
            msg.user_error("Not a git directory.")
            sys.exit(1)
    else:
        msg.user_error(path+" does not exist.")
        sys.exit(1)
