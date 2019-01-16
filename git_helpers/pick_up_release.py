#!/usr/bin/env python3
import utils.message as msg
import utils.shell_helpers as shell
import os
import sys
from utils.json_config import Json_config
import git_helpers.git_utils as git
import git_helpers.regex_obj as ro
from git_helpers.get_all_version_tags import get_all_version_tags
# from git_helpers.validator.version_file import check_bump_release_version_script
from git_helpers.tags_commits import Tags_commits			
from utils.prompt import prompt_boolean

release_err_msg="""
 Create a script file deploy.sh or deploy.py
     This file needs to be located:
        - at parent directory of src directory.
     This file generally does the following:
         - It receives two arguments "release_version" and "release_type" 
         - cd on src
         - git checkout release_version_tag
         - compile source (if needed)
             . multiple architectures
             . move binaries to destination directory(s)
             . rename commands aliases if necessary
         - compress source code
             . copy source to destination directory(s)
         - git checkout on previous branch
         - cd on previous directory
         - You can also have some differences depending of the release_type.
"""

def pick_up_release(release_version, deploy_args=[]):
    if release_version[0]=="v":
        release_version=release_version[1:]

    obj_reg_release=ro.Version_regex(release_version)
    if not obj_reg_release.match:
        msg.user_error(
            "Release tag authorized forms:",
            "'(v)?"+ro.Version_regex().string+"'",
            "However your release_version is '"+release_version+"'"
        )
        sys.exit(1)

    msg.title("Pick up release v"+release_version )

    if not Tags_commits("local").get_tag_commit("v"+release_version):
        msg.user_error("There is no tag in the project that matches v"+ release_version)
        sys.exit(1)

    conf = Json_config()
    filer_deploy=conf.get_value("filer_deploy")
    direpa_parent=os.path.dirname(git.get_root_dir_path())

    filerpa_deploy_release=os.path.join(direpa_parent, filer_deploy)

    if os.path.exists(filerpa_deploy_release+".py"):
        filenpa_deploy=filerpa_deploy_release+".py"
    elif os.path.exists(filerpa_deploy_release+".sh"):
        filenpa_deploy=filerpa_deploy_release+".sh"
    else:
        filenpa_deploy=""

    if filenpa_deploy:
        is_cmd_executable= os.access(filenpa_deploy, os.X_OK)
        if not is_cmd_executable:
            msg.user_error("script "+filer_deploy+" is not executable")
            sys.exit(1)
        else:
            msg.dbg("info","launch script "+filer_deploy)
            if deploy_args:
                shell.cmd(filenpa_deploy+" "+release_version+" "+deploy_args)
            else:
                shell.cmd(filenpa_deploy+" "+release_version)
    else:
        msg.warning(release_err_msg[1:])
        sys.exit(1)
