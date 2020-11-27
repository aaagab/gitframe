#!/usr/bin/env python3
from lxml import etree
from pprint import pprint
import os
import sys

# from . import git_utils as git
from . import msg_helpers as msgh
from . import regex_obj as ro
from .get_all_version_tags import get_all_version_tags
from .helpers import get_path	
from .prompt_for_commit import prompt_for_commit
from .remote_repository import Remote_repository
from .tags_commits import Tags_commits		


from ..gpkgs.prompt import prompt_boolean
from ..gpkgs import shell_helpers as shell
from ..utils.json_config import Json_config

from ..gpkgs import message as msg
from ..gpkgs.gitlib import GitLib

def tag(
    commit_message=None,
    direpa_src=None,
    tag=None,
    version_file=None,
):
    git=GitLib(direpa=direpa_src)
    git.is_direpa_git(fail_exit=True)
    repo=Remote_repository()

    branch=git.get_active_branch_name()
    reg_branch=ro.get_element_regex(branch)
    if reg_branch.type in ["develop", "master", "draft"]:
        msg.error("tag is not done on branch '{}'".format(branch), exit=1)

    if tag is None:
        if version_file is None:
            msg.error("--version-file needs to be set", exit=1)

        version_file=get_path(version_file)
        if not os.path.isfile(version_file):
            msg.error("version file is not a file '{}'".format(version_file), exit=1)

        filer, ext =os.path.splitext(version_file)
        if os.path.basename(version_file).lower() == "web.config":
            xml_elem=etree.parse(version_file).getroot().find("./appSettings/add[@key='VERSION']")
            if xml_elem is None:
                msg.error("VERSION attribute not found in appsettings '{}'.".format(version_file), exit=1)
            tag=xml_elem.attrib["value"]
        elif ext == ".json":
            data=Json_config(version_file).data
            if not "version" in data:
                msg.error("version attribute not found in '{}'".format(version_file), exit=1)
            tag=data["version"]
        else:
            with open(version_file, "r") as f:
                tag=f.read().strip()

    if ro.Version_regex(tag).match is False:
        msg.error("tag from does not follow semantic versioning '{}'".format(tag[:50]), exit=1)

    if tag in get_all_version_tags():
        msg.error("tag '{}' already exists".format(tag),exit=1)

    if tag[0]!="v":
        tag="v"+tag

    prompt_for_commit(commit_message=commit_message, direpa_git=git.get_direpa_root())

    git.set_annotated_tags(tag, "Bump release version {}".format(tag.replace("v", "")), remote_names=["origin"])
    branches=git.get_local_branches()
    if reg_branch.type in ["features", "hotfix"]:
        for main_branch in ["develop", "master"]:
            if main_branch in branches:
                if reg_branch.type == "hotfix" and main_branch == "develop":
                    pass
                else:
                    git.checkout(main_branch) 
                    git.merge_noff(branch)
                    git.push("origin", branch_name=main_branch)

    if git.get_active_branch_name() != branch:
        git.checkout(branch)
        git.push("origin", branch_name=branch)
