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

    direpa_app=git.get_root_dir_path()
    diren_app=os.path.basename(direpa_app)
    direpa_par_app=os.path.dirname(direpa_app)
    direpa_app_git=os.path.join(direpa_par_app, diren_app+".git")

    if not os.path.exists(direpa_app_git):
        if repo.is_reachable:
            if not repo.has_directory:
                if repo.path_type == "directory":
                    msg.dbg("info", "repo is a directory")
                    shell.cmd_prompt("git clone --bare "+direpa_app+" "+repo.path, True)
                    os.chdir(direpa_app)
                    
                    shell.cmd_prompt("git push origin master")
                    shell.cmd_prompt("git push origin develop")
                elif repo.path_type == "url":
                    user_ssh=prompt("Type ssh username")
                    scp_path=re.sub(r"^.*?(@.*)$",user_ssh+r"\1",repo.path)
                    ssh_url=user_ssh+"@"+repo.domain
                    shell.cmd_prompt("git clone --bare "+direpa_app+" "+direpa_app_git, True)
                    os.chdir(direpa_app)

                    shell.cmd_prompt("ssh "+ssh_url+" \"mkdir -p "+repo.direpa_par_src+"\"", True)
                    shell.cmd_prompt("scp -r "+direpa_app+".git "+scp_path, True)
                    shell.cmd_prompt("ssh -t "+ssh_url+" \"sudo chown -R "+repo.user_git+":"+repo.user_git+" "+repo.direpa_src+"\"",True)
                    repo.has_directory=True

                    shell.cmd_prompt("git push origin master")
                    shell.cmd_prompt("git push origin develop")

                    try:
                        shutil.rmtree(direpa_app_git)
                        msg.success(direpa_app+".git deleted on local.")
                    except:
                        msg.app_error(direpa_app+".git not deleted on local.")
                        sys.exit(1)
                    
            else:
                msg.user_error(
                    "Remote Directory "+direpa_app+".git Already Exists on remote repository 'Origin'",
                    "Clone "+direpa_app+".git from remote to Local or Change application name"
                    )
                sys.exit(1)
        else:
            msg.user_error("Remote repository 'Origin' is not reachable, verify your internet connectivity.")
            sys.exit(1)
    else:
        msg.user_error(direpa_app+".git already Exists on local, delete it or back-it up in another directory and restart the operation.")
        sys.exit(1)
        