#!/usr/bin/env python3
import os
import utils.message as msg
import utils.shell_helpers as shell
import git_helpers.git_utils as git
from utils.prompt import prompt, prompt_boolean

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

def delete_dir(direpa):
    try:
        shutil.rmtree(direpa)
        msg.success("'{}' deleted on local.".format(direpa))
    except:
        msg.app_error("'{}' not deleted on local.".format(direpa))
        sys.exit(1)

def verify_direpa_app_git(direpa_app, direpa_app_git):
    create_direpa_app_git=True

    if os.path.exists(direpa_app_git):
        msg.warning("'{} already exists'".format(direpa_app_git))
        if not prompt_boolean("Do you want to upload existing folder to repo ('N' means create a new one from source)"):
            delete_dir(direpa_app_git)
        else:
            create_direpa_app_git=False

    if create_direpa_app_git:
        shell.cmd_prompt("git clone --bare "+direpa_app+" "+direpa_app_git, True)

    os.chdir(direpa_app)

def clone_project_to_remote(repo):
    msg.title("clone project to remote repository")

    direpa_app=git.get_root_dir_path()
    diren_app=os.path.basename(direpa_app)
    direpa_par_app=os.path.dirname(direpa_app)
    direpa_app_git=os.path.join(direpa_par_app, diren_app+".git")

    if repo.is_reachable:
        if not repo.has_directory:
            if repo.path_type == "directory":
                msg.dbg("info", "repo is a directory")
                verify_direpa_app_git(direpa_app, direpa_app_git)
                
                shell.cmd_prompt("git push origin master")
                shell.cmd_prompt("git push origin develop")
                
            elif repo.path_type == "url":
                msg.dbg("info", "repo is an url")
                user_ssh=prompt("Type ssh username")
                scp_path=re.sub(r"^.*?(@.*)$",user_ssh+r"\1",repo.path)
                ssh_url=user_ssh+"@"+repo.domain

                verify_direpa_app_git(direpa_app, direpa_app_git)

                shell.cmd_prompt("ssh "+ssh_url+" \"mkdir -p "+repo.direpa_par_src+"\"", True)
                shell.cmd_prompt("scp -r "+direpa_app+".git "+scp_path, True)
                shell.cmd_prompt("ssh -t "+ssh_url+" \"sudo chown -R "+repo.user_git+":"+repo.user_git+" "+repo.direpa_src+"\"",True)
                repo.has_directory=True

                shell.cmd_prompt("git push origin master")
                shell.cmd_prompt("git push origin develop")

                delete_dir(direpa_app_git)
        else:
            msg.user_error(
                "Remote Directory "+direpa_app+".git Already Exists on remote repository 'Origin'",
                "Clone "+direpa_app+".git from remote to Local or Change application name"
                )
            sys.exit(1)
    else:
        msg.user_error("Remote repository 'Origin' is not reachable, verify your internet connectivity.")
        sys.exit(1)

        