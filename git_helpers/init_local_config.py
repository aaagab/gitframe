#!/usr/bin/env python3
import os
import sys

from ..gpkgs import message as msg

from ..utils import shell_helpers as shell
from ..utils.prompt import prompt

def set_username(username):
    shell.cmd("git config --local user.name "+username)
    msg.info("local name set to '"+username+"'")

def set_email(email):
    shell.cmd("git config --local user.email "+email)
    msg.info("local email set to '"+email+"'")

def set_repository(repository):
    shell.cmd("git remote add origin "+repository)
    msg.info("Repository set to '"+repository+"'")

def init_local_config(user_obj=""):
    from . import git_utils as git
    
    root_dir=git.get_root_dir_name()

    username=""
    email=""
    repository=""

    if user_obj:
        username=user_obj["username"]
        email=user_obj["email"]
        repository=user_obj["repository"]
        set_username(username)
        set_email(email)
        set_repository(repository)
    else:
        username=shell.cmd_get_value("git config --local user.name")
        email=shell.cmd_get_value("git config --local user.email")
        repository=shell.cmd_get_value("git config --get remote.origin.url")
    
    if not username:
        username=prompt("Enter git user name")
        set_username(username)
 
    if not email:
        email=prompt("Enter git user email")
        set_email(email)

    if not repository:
        print()
        print("repository examples: ")
        print("  On server with name: '{user}@{server_name}:/{path}.git'")
        print("  On server with ip: '{user}@{server_ip}:/{path}.git'")
        print("  On local: '{path}.git'")
        print()
        repository=os.path.normpath(prompt("Enter origin repository"))
        set_repository(repository)
