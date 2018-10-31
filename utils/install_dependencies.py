#!/usr/bin/env python3
import os
import sys
import utils.shell_helpers as shell
import utils.message as msg
import platform
import subprocess, shlex
import shutil
import git_helpers.git_utils as git
import getpass

def install_dependencies(obj_deps):
    if os.name == 'posix':

        user=getpass.getuser()

        if not shutil.which("sudo"):
            msg.user_error("sudo not found.")
            sys.exit(1)
        elif user != "root":
            if not "sudo" in shell.cmd_get_value("groups"):
                msg.user_error("user does not belong to sudo group.")
                sys.exit(1)

        for obj_dep in obj_deps:
            cmd=obj_dep["cmd"]
            app=obj_dep["app"]

            if not shutil.which(cmd):
                msg.warning("'"+cmd+"' not found.")
                if 'debian' in platform.dist() or 'ubuntu' in platform.dist():
                    msg.info("Trying to install "+app)
                    if user == "root":
                        shell.cmd_prompt("apt-get install " + app)
                    else:
                        shell.cmd_prompt("sudo apt-get install " + app)
                else:
                    msg.user_error("Install '"+app+"' to continue.")
                    sys.exit(1)
    else:
        print("This program has been created for Linux.")
        sys.exit(1)	
