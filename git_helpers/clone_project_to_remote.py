#!/usr/bin/env python3
import os
import shutil
import sys
import re

from . import git_utils as git
from . import msg_helpers as msgh


from ..gpkgs import message as msg

from ..utils import shell_helpers as shell
from ..utils.prompt import prompt, prompt_boolean




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
        msg.error("'{}' not deleted on local.".format(direpa))
        sys.exit(1)

def clone_project_to_remote(repo):

    direpa_app=git.get_root_dir_path()
    diren_app=os.path.basename(direpa_app)
    direpa_par_app=os.path.dirname(direpa_app)
    direpa_app_git=os.path.join(direpa_par_app, diren_app+".git")

    msgh.title("clone '{}' to remote repository".format(diren_app))

    if repo.is_reachable:
        if not repo.is_git_directory:
            if repo.path_type == "directory":
                msg.dbg("info", "repo is a directory")
                # verify_direpa_app_git(direpa_app, direpa_app_git)
                shell.cmd_prompt("git clone --bare "+direpa_app+" "+repo.path, True)
                os.chdir(direpa_app)
                
            elif repo.path_type == "url":
                msg.dbg("info", "repo is an url")
                user_ssh=prompt("Type ssh username")
                scp_path=re.sub(r"^.*?(@.*)$",user_ssh+r"\1",repo.path)
                ssh_url=user_ssh+"@"+repo.domain

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


                shell.cmd_prompt("ssh "+ssh_url+" \"mkdir -p "+repo.direpa_par_src+"\"", True)
                shell.cmd_prompt("scp -r "+direpa_app+".git "+scp_path, True)
                shell.cmd_prompt("ssh -t "+ssh_url+" \"sudo chown -R "+repo.user_git+":"+repo.user_git+" "+repo.direpa_src+"\"",True)
                repo.is_git_directory=True

                delete_dir(direpa_app_git)
        else:
            msg.error(
                "Remote Directory "+direpa_app+".git Already Exists on remote repository 'Origin'",
                "Clone "+direpa_app+".git from remote to Local or Change application name"
                )
            sys.exit(1)
    else:
        msg.error("Remote repository 'Origin' is not reachable, verify your internet connectivity.")
        sys.exit(1)

        