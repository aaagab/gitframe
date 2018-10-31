#!/usr/bin/env python3
import os
import utils.message as msg
import utils.shell_helpers as shell
import git_helpers.git_utils as git
from utils.prompt import prompt

import shutil
import sys
import re

# if in a src directory
#     ok

#     if apps_directory is reachable:
#         if app_directory is reachable:
#             if type directory:

#             elif type url:

#             if src_directory is reachable:
#         else:

#     First check that apps_directory exists.
#         then check for app_directory:
#         then change right for app_directory
#         then clone src to app_directory
# else:
#     code needs to be in a src directory



def clone_project_to_remote(repo):
    msg.title("clone project to remote repository")

    direpath_git_root=git.get_root_dir_path()
    diren_app=os.path.basename(direpath_git_root)
    path_root_dir=os.path.dirname(direpath_git_root)
    os.chdir(path_root_dir)

    if not os.path.exists(diren_app+".git"):
        if repo.is_reachable:
            if not repo.has_directory:
                if repo.path_type == "directory":
                    msg.dbg("info", "repo is a directory")
                    shell.cmd_prompt("git clone --bare "+diren_app+" "+repo.path)
                    # repo.has_directory_set=True

                elif repo.path_type == "url":
                    user_ssh=prompt("Type ssh username")
                    scp_path=os.path.dirname(re.sub(r"^.*?(@.*)$",user_ssh+r"\1",repo.path))
                    ssh_url=user_ssh+"@"+repo.domain

                    shell.cmd_prompt("git clone --bare "+diren_app+" "+diren_app+".git")
                    shell.cmd_prompt("scp -r "+diren_app+".git "+scp_path)
                    shell.cmd_prompt("ssh -t "+ssh_url+" \"sudo chown -R "+repo.user_git+":"+repo.user_git+" "+repo.direpa_src+"\"")
                    repo.has_directory=True

                    try:
                        shutil.rmtree(diren_app+".git")
                        msg.success(diren_app+".git deleted on local.")
                        os.chdir(diren_app)
                    except:
                        msg.app_error(diren_app+".git not deleted on local.")
                        sys.exit(1)
                    
            else:
                msg.user_error(
                    "Remote Directory "+diren_app+".git Already Exists on remote repository 'Origin'",
                    "Clone "+diren_app+".git from remote to Local or Change application name"
                    )
                sys.exit(1)
        else:
            msg.user_error("Remote repository 'Origin' is not reachable, verify your internet connectivity.")
            sys.exit(1)
    else:
        msg.user_error(diren_app+".git already Exists on local, delete it or back-it up in another directory and restart the operation.")
        sys.exit(1)
        