#!/usr/bin/env python3
import sys, os
import utils.message as msg
from utils.json_config import Json_config
import git_helpers.git_utils as git

def create_directory(path):
    if os.path.exists(path):
        diren_path=os.path.basename(path)
        if diren_path == "src":
            msg.user_error("src folder already exists be sure that it is empty, erase it and relaunch the command.")
            sys.exit(1)
        else:
            msg.warning("'"+path+"' already exists.")
    else:
        try:
            os.mkdir(path)
            msg.success("Path '"+path+"' created.")
        except:
            msg.app_error("cannot create path '"+path+"'")
            sys.exit(1)

        return path

def create_directory_tree():
    msg.title("Create directory Tree")

    directorys=[
        "brainstorming",
        "documentation",
        "scripts",
        "todo",
        "src"
    ]
    created_directorys=[]
    current_path=os.getcwd()
    for directory in directorys:
        tmp_directory=create_directory(os.path.join(current_path, directory))
        if tmp_directory:
            created_directorys.append(tmp_directory)
            
    return created_directorys