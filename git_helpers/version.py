#!/usr/bin/env python3
import utils.message as msg
import git_helpers.git_utils as git
import os
import sys
import re
import git_helpers.regex_obj as ro
from utils.json_config import Json_config 

def bump_tag_file(version):
    msg.info("Bump Release Tag")
    
    try:
        with open("version.txt","w") as f:
            f.write(version+'\n')
        msg.success("Inserting \""+version+"\" in version.txt completed.")
        git.commit("Bump Release Tag "+version)
    except:
        msg.app_error("Inserting \""+version+"\" in version.txt failed!")
        sys.exit(1)

def get_content_version_file(debug=False, branch_name=""):
    filenpa_version=get_file_path()
    filen_version=Json_config().get_value("filen_version")
    start_branch=""
    if not branch_name:
        branch_name=git.get_active_branch_name()
        start_branch=branch_name
    else:
        start_branch=git.get_active_branch_name()
        git.checkout(branch_name)
    
    msg.dbg("info","Get version value from file "+filen_version+" on branch '"+branch_name+"'")

    if os.path.exists(filenpa_version):
        with open(filenpa_version) as f:
            value=f.read().strip()

        if not value:
            if branch_name:
                git.checkout(start_branch)
            if debug == True:
                msg.user_error(
                    "'"+filen_version+"' is empty on branch '"+branch_name+"'.",
                    )
            
            return ""
        else:
            if branch_name:
                git.checkout(start_branch)
            return value
    else:        
        if branch_name:
            git.checkout(start_branch)

        if debug == True:
            msg.user_error(
                "'"+filen_version+"' not found on branch '"+branch_name+"'.",
                )
        return ""


def get_file_path():
    return os.path.join(git.get_root_dir_path(),Json_config().get_value("filen_version"))

def increment_version_value(version_type, regex_version_value):
    msg.info("Increment '"+version_type+" for Version Value '"+regex_version_value.text+"'")

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
