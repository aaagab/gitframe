#!/usr/bin/env python3
import os
import sys
import shutil

import utils.message as msg
import git_helpers.git_utils as git
from git_helpers.clone_project_to_remote import clone_project_to_remote
from git_helpers.init_local_config import init_local_config
import utils.shell_helpers as shell
from utils.prompt import prompt_boolean, prompt
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
        sys.direns

def init_git_folder(direpa_to_init, user_obj, files_added):
    diren_to_init=os.path.basename(direpa_to_init)
    msg.info("init folder '{}'".format(diren_to_init))
    os.chdir(direpa_to_init)
    shell.cmd("git init")
    init_local_config(user_obj)
    file=os.path.join(os.getcwd(), ".gitignore")
    test_file_not_exist(file)
    open(file, 'w').close()
    files_added.append(file)

    # if diren_to_init == "src":
    #     file="hotfix-history.json"
    #     test_file_not_exist(file)
    #     with open(file,"w") as f:
    #         f.write("{}")
    #     files_added.append(file)

    shell.cmd("git add .")
    git.commit_empty("Branch master created on '"+diren_to_init+"'")

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

        if git.is_git_project(path):
            if git.get_root_dir_path(path) == path:
                msg.user_error("Current Path '"+path+"' is at a git project toplevel",
                    "cd into another directory or remove its .git directory and restart the operation.")
                sys.exit(1)

        if not prompt_boolean("Path '"+path+"' already exists.\nDo you want to add git to directory anyway?"):
            sys.exit(1)

    else: # path does not exist
        parent_directory_path=os.path.dirname(path)
        if not os.path.exists(parent_directory_path):
            msg.user_error("Path parent directory '"+parent_directory_path+"' does not exist.")
            sys.exit(1)

        root_dir=os.path.basename(os.path.normpath(path))
        create_directory(path)

    os.chdir(path)

    user_obj={}
    user_obj.update(username=prompt("Enter git user name"))
    user_obj.update(email=prompt("Enter git user email"))
    print()
    print("  Origin parent repository example: ")
    print("  On server with name: '{user}@{server_name}:/{path}'")
    print("  On server with ip: '{user}@{server_ip}:/{path}'")
    print("  On local: '{path}'")
    print("  The Origin parent repository contains the 'dirname.git' created by git clone --bare")
    print()
    parent_repository=os.path.normpath(prompt("Enter origin parent repository"))

    created_directories, created_files=create_directory_tree(user_obj["username"])

    files_added=[]
    if created_files:
        files_added.extend(created_files)

    direpas_proj=[
        os.path.join(path, "doc"),
        os.path.join(path, "mgt"),
        os.path.join(path, "src")
    ]

    for direpa_proj in direpas_proj:
        diren_proj=os.path.basename(direpa_proj)
        user_obj["repository"]=os.path.join(parent_repository, diren_proj+".git")
        init_git_folder(direpa_proj, user_obj, files_added)
        if diren_proj != "src":
            os.chdir(path)

    if prompt_boolean("Do you Want To Add a License"):
        file="license.txt"
        test_file_not_exist(file)
        license_content=get_license_content()
        print(license_content)
        with open(file,"w") as f:
            f.write(license_content+'\n')

        files_added.append(file)
        git.commit(file+" added")

    git.checkoutb("develop")
    git.commit_empty("Branch develop created")

    for direpa_proj in direpas_proj:
        os.chdir(direpa_proj)
        repo=Remote_repository()
        if repo.is_reachable:
            if repo.is_git_directory:
                diren_repo=os.path.basename(repo.path)
                msg.user_error(
                    "Remote Directory "+diren_repo+" Already Exists on remote repository 'Origin'",
                    "Clone "+diren_repo+" from Remote or Change application name"
                )

                if os.path.basename(direpa_proj) == "src":
                    try:
                        if existing_directory:
                            shutil.rmtree(".git")
                            for f in files_added:
                                msg.info("Remove file '"+f+"'")
                                os.remove(f)
                            
                            os.chdir(path)
                            for directory in created_directories:
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
                if os.path.basename(direpa_proj) == "src":
                    shell.cmd_prompt("git push origin develop")
                    shell.cmd_prompt("git push origin master")
        else:
            msg.warning("Clone your project when connectivity is back.")

    msg.success("New Project "+root_dir+" initialized.")
