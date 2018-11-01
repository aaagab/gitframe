#!/usr/bin/env python3
import utils.message as msg
import utils.shell_helpers as shell
import os
import sys
from utils.json_config import Json_config
import git_helpers.git_utils as git
import git_helpers.regex_obj as ro

release_err_msg="""
 Create a script file deploy_release.sh or deploy_release.py
     This file needs to be located at:
        - scripts directory,in parent directory of src directory.
     This file generally does the following:
         - It receives one argument "release_version" 
         - cd on src
         - git checkout release_version_tag
         - compile source (if needed)
             . multiple architectures
             . move binaries to destination directory(s)
             . rename commands aliases if necessary
         - compress source code
             . copy source to destination directory(s)
         - git checkout on previous branch
"""

def publish_release(release_version, all_version_tags):
    release_type=""
    if release_version[0]=="v":
        release_version=release_version[1:]
    
    obj_reg_release=ro.Version_regex(release_version)
    if not obj_reg_release.match:
        obj_reg_release=ro.Early_release_regex(release_version)
        if not obj_reg_release.match:
            msg.user_error(
                "Release tag authorized forms:",
                "'(v)?"+ro.Version_regex().string+"'",
                "'(v)?"+ro.Early_release_regex().string+"'",
                "However your release_version is '"+release_version+"'"
            )
            sys.exit(1)
        else:
            release_type="early_release"
    else:
        release_type="release"

    msg.title("Publish Tag v"+release_version )
    msg.dbg("info", release_type)

    if not git.get_commit_from_tag("v"+release_version):
        msg.user_error("There is no tag in the project that matches v"+ release_version)
        sys.exit(1)

    conf = Json_config()
    filer_deploy_release=conf.get_value("filer_deploy_release")
    direpa_parent = os.path.abspath('..')

    filerpa_deploy_release=os.path.join(direpa_parent, conf.get_value("diren_scripts"), filer_deploy_release)

    if os.path.exists(filerpa_deploy_release+".py"):
        filenpa_deploy_release=filerpa_deploy_release+".py"
    elif os.path.exists(filerpa_deploy_release+".sh"):
        filenpa_deploy_release=filerpa_deploy_release+".sh"
    else:
        filenpa_deploy_release=""

    if filenpa_deploy_release:
        is_cmd_executable= os.access(filenpa_deploy_release, os.X_OK)
        if not is_cmd_executable:
            msg.user_error("script "+filer_deploy_release+" is not executable")
            sys.exit(1)
        else:
            msg.dbg("info","launch script "+filer_deploy_release)
            shell.cmd(filenpa_deploy_release+" "+release_version+" "+release_type)
    else:
        msg.warning(release_err_msg[1:])
        sys.exit(1)
