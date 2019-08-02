#!/usr/bin/env python3
import os
import re
import sys

from . import git_utils as git
from . import msg_helpers as msgh
from . import regex_obj as ro

from ..gpkgs import message as msg

from ..utils.json_config import Json_config
from ..gpkgs import shell_helpers as shell

def increment_version_value(version_type, regex_version_value):
    msg.info("Increment '"+version_type+"' for Version Value '"+regex_version_value.text+"'")

    if version_type == "major":
        major=int(regex_version_value.major)+1
        return "{}.0.0".format(major)
    elif version_type == "minor":
        minor=int(regex_version_value.minor)+1
        return "{}.{}.0".format(regex_version_value.major, minor)
    elif version_type == "patch":
        patch=int(regex_version_value.patch)+1
        return "{}.{}.{}".format(
            regex_version_value.major,
            regex_version_value.minor,
            patch
            )

def bump_version_for_user(version):
    msgh.subtitle("Check bump release version script.")
    conf = Json_config()
    filer_bump_version=conf.get_value("filer_bump_version")

    bump_release_version_script_err_msg="""
    Create a script file {bump_version}.sh or {bump_version}.py
        This file needs to be located at:
            - scripts directory,in parent directory of src directory.
        The script should do the following:
            - It receives a release_version from gitframe.
            - This value is then set in location(s) defined by the developer.
            - For gitframe the release version is stored in config.json but
              it can really be anywhere.
            - This value is then going to be retrieved by the user.
            - Generally the user retrieves the release version by executing 
              the software with -v parameter.
            - That is the purpose of this script.
            - {bump_version} script is automatically called by gitframe 
              just before setting an annotated tag when picking-up a new release.
    """.format(bump_version=filer_bump_version)

    direpa_parent=os.path.dirname(git.get_root_dir_path())

    filerpa_bump_release_version=os.path.join(direpa_parent, filer_bump_version)

    filenpa_bump_version=""
    if os.path.exists(filerpa_bump_release_version+".py"):
        filenpa_bump_version=filerpa_bump_release_version+".py"
    elif os.path.exists(filerpa_bump_release_version+".sh"):
        filenpa_bump_version=filerpa_bump_release_version+".sh"
    else:
        filenpa_bump_version=""

    if filenpa_bump_version:
        is_cmd_executable= os.access(filenpa_bump_version, os.X_OK)
        if not is_cmd_executable:
            msg.error("script "+filer_bump_version+" is not executable")
            sys.exit(1)

        msg.dbg("info","Execute script "+filer_bump_version)
        # shell.cmd(filenpa_bump_version+" "+version)       
        os.system(filenpa_bump_version+" "+version)     
    else:
        msg.warning(bump_release_version_script_err_msg[1:])
        sys.exit(1)
