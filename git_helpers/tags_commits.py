#!/usr/bin/env python3
from pprint import pprint
import sys

from . import git_utils as git

from ..gpkgs import message as msg

from ..gpkgs import shell_helpers as shell
from ..gpkgs.prompt import prompt

class Tags_commits():
    def __init__(self, location):
        if not location in ["local", "remote", "all"]:
            msg.error(
                "Unknown location '{}' for Tags_commits".format(location),
                "Authorized location are '{}'.".format("local, remote, all")    
            )
            sys.exit(1)
        self.tags={}

        if location == "local":
            self.get_local_tags()
        elif location == "remote":
            self.get_remote_tags()
        elif location == "all":
            self.get_local_tags()
            self.get_remote_tags()

    def get_local_tags(self):
        location="local"
        self.tags.update({
                location: {}
            })
        all_tags=shell.cmd_get_value("git tag")
        if all_tags is not None:
            for name in all_tags.splitlines():
                self.tags[location].update({
                        name: shell.cmd_get_value("git rev-list -n 1 "+name).strip()
                    })

    def get_remote_tags(self):
        location="remote"
        self.tags.update({
            location: {}
        })
        all_tags=shell.cmd_get_value("git ls-remote --tags origin")
        
        if all_tags is not None:
            for line in all_tags.splitlines():
                commit, name=line.split('\t')
                name=name.replace("refs/tags/","")

                is_annotated_tag=False
                if "^{}" in name:
                    is_annotated_tag=True

                # if annotated tag commit is chosen instead of regular tag for same name
                if is_annotated_tag:
                    name=name.replace("^{}", "")
                    self.tags[location].update({
                        name: commit
                    })
                else:
                    if not name in self.tags[location]:
                        self.tags[location].update({
                            name: commit
                        })

    def get_tag_commit(self, tag_name, location=""):
        if not location:
            msg.dbg("info", "Commit for "+tag_name+" on local")
            if self.tags.get("local"):
                if self.tags["local"].get(tag_name):
                    return self.tags["local"][tag_name]
                else:
                    return ""
            else:
                return ""
        else:
            msg.dbg("info", "Commit for "+tag_name+" on "+location)
            if self.tags.get("local"):
                if self.tags[location].get(tag_name):
                    return self.tags[location][tag_name]
                else:
                    return ""
            else:
                return ""
