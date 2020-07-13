#!/usr/bin/env python3
import platform
import os
import re
import sys

try:
    from . import git_utils as git
    from . import msg_helpers as msgh
    from .init_local_config import init_local_config
    from ..gpkgs import message as msg
    from ..gpkgs import shell_helpers as shell
except:
    direpa_script=os.path.realpath(__file__)
    direpa_launcher=os.path.dirname(direpa_script)
    sys.path.insert(0,direpa_launcher)
    import git_utils as git
    import msg_helpers as msgh
    from init_local_config import init_local_config
    from gpkgs import message as msg
    from gpkgs import shell_helpers as shell


class Remote_repository():
    def __init__(self,
        _platform=None
    ):
        msg.info("Initializing Remote Repository")
        
        self.platform=_platform
        if self.platform is None:
            self.platform=platform.system()
        self.path=self.get_path()
        self.domain=""
        self.direpa_src=""
        self.user_git=""
        self.path_type=self.get_path_type()
        self.direpa_par_src = self.get_direpa_par_src()
        self.is_reachable = self.get_is_reachable()
        self.is_git_directory = self.set_is_git_directory()

    def get_path_type(self):
        path=self.path

        url=re.match(r"^(.+)@(.+?):(.+)$", path)
        
        if url:
            self.user_git=url.group(1)
            self.domain=url.group(2)
            self.direpa_src=url.group(3)

            return "url"
        else:
            self.direpa_src=self.path

            return "directory"

    def get_is_reachable(self):
        found=False
        if  self.path_type == "directory":
            if os.path.exists(self.direpa_par_src):
                found=True
                msg.success("Remote Path '"+self.direpa_par_src+"' is reachable.")
            else:
                msg.warning("Remote Path '"+self.direpa_par_src+"' is not reachable.")
        elif self.path_type == "url":
            # if shell.cmd_devnull("ping -c2 -W1 " + self.domain) == 0:
            if self.short_ping(self.platform, self.domain) is True:
                found=True
                msg.success("Remote Path '"+self.domain+"' is reachable.")
            else:
                msg.warning("Remote Path '"+self.domain+"' is not reachable.")
        
        return found

    def short_ping(self, platform, domain):
        count_arg=""
        null_arg=""
        if platform == "Windows":
            count_arg="-n"
            null_arg="> nul 2>&1"
        elif platform == "Linux":
            count_arg="-c"
            null_arg="> /dev/null 2>&1"

        cmd="ping {} 2 {} {}".format(count_arg, domain, null_arg)
        if os.system(cmd) == 0:
            return True
        else:
            return False

    def set_is_git_directory(self):
        exists=False
        if shell.cmd_devnull("git ls-remote "+self.path) == 0:
            exists=True
            msg.success("Remote Repository '"+self.path+"' exists.")
        else:
            if self.is_reachable:
                msg.warning("Remote Repository '"+self.path+"' does not exist.")
            else:
                msg.warning("Remote Repository '"+self.path+"' may not exist.")

        return exists

    def get_direpa_par_src(self):
        if self.path_type == "directory":
            return os.path.dirname(self.path)
        elif self.path_type == "url":
            return os.path.dirname(self.direpa_src)

    def get_path(self):
        path=shell.cmd_get_value("git config --get remote.origin.url")
        while not path:
            msg.info("remote git url not set, launching init_local_config")
            init_local_config()
            path=shell.cmd_get_value("git config --get remote.origin.url")

        return path
