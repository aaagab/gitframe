#!/usr/bin/env python3
import os
from pprint import pprint
import sys 

from ..git_helpers import git_utils as git
from ..git_helpers import msg_helpers as msgh

from ..gpkgs import message as msg

from .json_config import Json_config


def create_directory(path):
    if os.path.exists(path):
        diren_path=os.path.basename(path)
        if diren_path == "src":
            msg.error("src folder already exists be sure that it is empty, erase it and relaunch the command.")
            sys.exit(1)
        else:
            msg.warning("'"+path+"' already exists.")
    else:
        try:
            os.mkdir(path)
            msg.success("Path '"+path+"' created.")
        except:
            msg.error("Cannot create path '"+path+"'")
            sys.exit(1)

        return path

def create_file(filenpa):
    if os.path.exists(filenpa):
        msg.warning("'"+filenpa+"' already exists.")
    else:
        try:
            open(filenpa, 'w').close()
            msg.success("File '"+filenpa+"' created.")
        except:
            msg.error("Cannot create file '"+filenpa+"'")
            sys.exit(1)

        return filenpa

def create_symlink(filenpa_src, filenpa_dst):
    if os.path.exists(filenpa_dst):
        os.remove(filenpa_dst)

    try:
        os.symlink(filenpa_src, filenpa_dst)
        msg.success("Symlink '"+filenpa_dst+"' created.")
    except:
        msg.error("Cannot create symlink '"+filenpa_dst+"'")
        sys.exit(1)

def create_directory_tree(git_user_name):
    conf=Json_config().data
    msgh.title("Create directory Tree")

    directorys=[
        "src",
        "doc",
        "mgt",
        os.path.join("mgt",git_user_name)
    ]
    created_directories=[]
    current_path=os.getcwd()
    for directory in directorys:
        tmp_directory=create_directory(os.path.join(current_path, directory))
        if tmp_directory:
            if os.path.basename(os.path.dirname(tmp_directory)) != "mgt":
                created_directories.append(tmp_directory)

    direpa_mgt_user=os.path.join(current_path,"mgt", git_user_name)
    
    filenpa_bump=os.path.join(direpa_mgt_user, conf["filer_bump_version"]+".py")
    filenpa_publish=os.path.join(direpa_mgt_user, conf["filer_deploy"]+".py")
    filenpa_scriptjob_json=os.path.join(direpa_mgt_user, conf["filen_scriptjob_save_json"])

    files=[
        filenpa_publish,
        filenpa_bump,
        filenpa_scriptjob_json,
        os.path.join(direpa_mgt_user, "todo.txt")
    ]
    created_files=[]

    for file in files:
        tmp_file=create_file(file)
        if tmp_file:
            created_files.append(tmp_file)

    if filenpa_publish in created_files:
        os.chmod(filenpa_publish, 0o755)

    filenpa_publish_link=os.path.join(current_path, os.path.basename(filenpa_publish))
    create_symlink(filenpa_publish, filenpa_publish_link)
    created_files.append(filenpa_publish_link)

    if filenpa_bump in created_files:
        os.chmod(filenpa_bump, 0o755)

    filenpa_bump_link=os.path.join(current_path, os.path.basename(filenpa_bump))
    create_symlink(filenpa_bump, filenpa_bump_link)
    created_files.append(filenpa_bump_link)

    filenpa_scriptjob_json_link=os.path.join(current_path, os.path.basename(filenpa_scriptjob_json))
    create_symlink(filenpa_scriptjob_json, filenpa_scriptjob_json_link)
    created_files.append(filenpa_scriptjob_json_link)
            
    return created_directories, created_files