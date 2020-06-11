#!/usr/bin/env python3
import getpass
import platform
import os
import shutil
import subprocess, shlex
import sys

try:
    from ..git_helpers import git_utils as git
    from ..gpkgs import message as msg
    from . import shell_helpers as shell
except:
    direpa_script=os.path.realpath(__file__)
    direpa_launcher=os.path.dirname(os.path.dirname(direpa_script))
    sys.path.insert(0,direpa_launcher)
    from git_helpers import git_utils as git
    from gpkgs import message as msg
    from gpkgs import shell_helpers as shell

def install_dependencies(obj_deps):
    if os.name == 'posix':

        user=getpass.getuser()

        if not shutil.which("sudo"):
            msg.error("sudo not found.")
            sys.exit(1)
        elif user != "root":
            if not "sudo" in shell.cmd_get_value("groups"):
                msg.error("user does not belong to sudo group.")
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
                    msg.error("Install '"+app+"' to continue.")
                    sys.exit(1)
    else:
        # print("This program has been created for Linux.")
        # sys.exit(1)	
        pass
