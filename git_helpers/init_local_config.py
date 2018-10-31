#!/usr/bin/env python3
import utils.message as msg
import utils.shell_helpers as shell
from utils.prompt import prompt
import sys, os

def init_local_config():
    import git_helpers.git_utils as git
    
    root_dir=git.get_root_dir_name()

    username=shell.cmd_get_value("git config --local user.name")
    if not username:
        username=prompt("Enter user name")
        shell.cmd("git config --local user.name "+username)
        msg.info("local name set to '"+username+"'")

    email=shell.cmd_get_value("git config --local user.email")
    if not email:
        email=prompt("Enter user email")
        shell.cmd("git config --local user.email "+email)
        msg.info("local email set to '"+email+"'")

    repository=shell.cmd_get_value("git config --get remote.origin.url")
    if not repository:
        print()
        print("repository examples: ")
        print("  On server with name: '{user}@{server_name}:/{path}.git'")
        print("  On server with ip: '{user}@{server_ip}:/{path}.git'")
        print("  On local: '{path}.git'")
        print()
        repository=prompt("Enter origin repository")

        repository=os.path.normpath(repository)
        shell.cmd("git remote add origin "+repository)
        msg.info("Repository set to '"+repository+"'")
