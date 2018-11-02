#!/usr/bin/env python3
import os
import sys
import shutil

import utils.message as msg
import git_helpers.git_utils as git
from git_helpers.clone_project_to_remote import clone_project_to_remote
from git_helpers.init_local_config import init_local_config
import utils.shell_helpers as shell
from utils.prompt import prompt_boolean
from git_helpers.license import get_license_content
from git_helpers.remote_repository import Remote_repository
from utils.create_directory_tree import create_directory_tree
import re

def test_path_is_not_file(path):
    if os.path.isfile(path):
        msg.user_error("Path '"+path+"' is not a directory.")
        sys.exit(1)

def test_path_syntax(path):
    reg_text=r'^[A-Za-z0-9_\-\.]+$'

    if not os.path.dirname(path) == path:
        path_splitted=path.split(os.sep)
        if path_splitted[0] == "":
            del path_splitted[0] # empty for posix, drive letter for windows
        for path_chunk in path_splitted:
            if not re.match(reg_text, path_chunk):
                msg.user_error("Element '"+path_chunk+"' is not conform to path regex syntax '"+reg_text+"'")
                sys.exit(1)

def create_directory(path):
    if prompt_boolean("Path '"+path+"' does not exist.\nDo you want to create directory?"):
        try:
            os.mkdir(path)
            msg.success("Path '"+path+"' created.")
        except:
            msg.app_error("cannot create path '"+path+"'")
            sys.exit(1)
    else:
        sys.exit(1)

def test_file_not_exist(file):
    if os.path.exists(file):
        msg.user_error("File '"+file+"' already exists.")
        sys.exit(1)

def new_project(path=""):
    msg.title("Create new Git Project")
    existing_directory=False
    start_directory=os.getcwd()

    if not path:
        msg.dbg("info","empty path")
        path=os.getcwd()
    elif os.path.isabs(path):
        msg.dbg("info","path is absolute")
        test_path_is_not_file(path)
    else: # relative path
        msg.dbg("info","path is relative")
        path=os.path.join(os.getcwd(), path)
        test_path_is_not_file(path)
    
    test_path_syntax(path)

    if os.path.exists(path):
        existing_directory=True
        msg.dbg("info","path exists")
        root_dir=os.path.basename(os.path.normpath(path))

        if git.has_git_directory(path):
            msg.user_error("Current Path '"+path+"' has a .git directory",
                "cd into another directory or remove this .git directory and restart the operation.")
            sys.exit(1)

        if not prompt_boolean("Path '"+path+"' already exists, Do you want to add git to directory anyway?"):
            sys.exit(1)

    else: # path does not exist
        parent_directory_path=os.path.dirname(path)
        if not os.path.exists(parent_directory_path):
            msg.user_error("Path parent directory '"+parent_directory_path+"' does not exist.")
            sys.exit(1)

        root_dir=os.path.basename(os.path.normpath(path))
        create_directory(path)

    os.chdir(path)

    created_directorys=create_directory_tree()

    os.chdir("src")

    shell.cmd("git init")
    init_local_config()

    file_added=[]
    file="hotfix-history.json"
    test_file_not_exist(file)

    with open(file,"w") as f:
        f.write("{}")
    file_added.append(file)
    shell.cmd_prompt("git add .")
    git.commit_empty("Branch master created")

    if prompt_boolean("Do you Want To Add a License"):
        file="license.txt"
        test_file_not_exist(file)
        license_content=get_license_content()
        with open(file,"w") as f:
            f.write(license_content+'\n')

        file_added.append(file)
        git.commit(file+" added")

    git.checkoutb("develop")
    git.commit_empty("Branch develop created")
        
    repo=Remote_repository()

    if repo.is_reachable:
        if repo.has_directory:
            msg.user_error("Remote Directory "+root_dir+".git Already Exists on remote repository 'Origin'",                               "Clone "+root_dir+".git from Remote or Change application name")
            try:
                if existing_directory:
                    shutil.rmtree(".git")
                    for f in file_added:
                        msg.info("Remove file '"+f+"'")
                        os.remove(f)
                    
                    os.chdir(path)
                    for directory in created_directorys:
                        msg.info("Remove directory '"+directory+"'")
                        shutil.rmtree(directory)
                else:
                    os.chdir(os.path.dirname(path))
                    shutil.rmtree(root_dir)
            except:
                msg.app_error("cannot clean directory '"+root_dir+"'")
                sys.exit(1)

            msg.info("directory '"+root_dir+"' cleaned.")
            os.chdir(start_directory)
            sys.exit(1)
        else:
            clone_project_to_remote(repo)
            shell.cmd_prompt("git push origin develop")
            shell.cmd_prompt("git push origin master")
    else:
        msg.warning("Clone your project when connectivity is back.")

    msg.success("New Project "+root_dir+" initialized.")
