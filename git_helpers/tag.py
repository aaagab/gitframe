#!/usr/bin/env python3
from pprint import pprint
import os
import sys

from . import git_utils as git
from . import msg_helpers as msgh
from . import regex_obj as ro
from .tags_commits import Tags_commits		
from .helpers import get_path	

from ..gpkgs.prompt import prompt_boolean
from ..gpkgs import shell_helpers as shell
from ..utils.json_config import Json_config

from ..gpkgs import message as msg

def tag(
    all_version_tags=[],
    repo=None,
    tag=None,
    version_file=None
):
    if tag is None:
        if version_file is None:
            msg.error("--version-file needs to be set", exit=1)

        version_file=get_path(version_file)
        if not os.path.isfile(version_file):
            msg.error("version file is not a file '{}'".format(version_file), exit=1)

        filer, ext = os.path.splitext(version_file)
        if ext == ".json":
            data=Json_config(version_file).data
            if "version" not in Json_config(version_file).data:
                msg.error("There is no 'version' first level key in '{}'".format(version_file), exit=1)
            tag=data["version"].strip()
        else:
            with open(version_file, "r") as f:
                tag=f.read().strip()

    if tag in all_version_tags:
        msg.error("tag '{}' already exists".format(tag),exit=1)

    if tag == "":
        msg.error("Tag can't be empty", exit=1)
    if tag[0]!="v":
        tag="v"+tag



    git.set_annotated_tags(repo, tag, "release")

    for branch in git.get_local_branch_names():
        git.push_origin(repo, branch)
    

    sys.exit()
    if tag[0]=="v":
        tag=tag[1:]

    obj_reg_release=ro.Version_regex(tag)
    if not obj_reg_release.match:
        msg.error(
            "Release tag authorized forms:",
            "'(v)?"+ro.Version_regex().string+"'",
            "However your tag is '"+tag+"'"
        )
        sys.exit(1)

    msg.info("Pick up release v"+tag )

    if not Tags_commits("local").get_tag_commit("v"+tag):
        msg.error("There is no tag in the project that matches v"+ tag)
        sys.exit(1)

    conf = Json_config()
    filer_deploy=conf.get_value("filer_deploy")
    direpa_parent=os.path.dirname(git.get_root_dir_path())

    filerpa_deploy_release=os.path.join(direpa_parent, filer_deploy)

    if os.path.exists(filerpa_deploy_release+".py"):
        filenpa_deploy=filerpa_deploy_release+".py"
    elif os.path.exists(filerpa_deploy_release+".sh"):
        filenpa_deploy=filerpa_deploy_release+".sh"
    else:
        filenpa_deploy=""

    if filenpa_deploy:
        is_cmd_executable= os.access(filenpa_deploy, os.X_OK)
        if not is_cmd_executable:
            msg.error("script "+filer_deploy+" is not executable")
            sys.exit(1)
        else:
            msg.dbg("info","launch script "+filer_deploy)
            if deploy_args:
                os.system(filenpa_deploy+" "+tag+" "+deploy_args)
            else:
                os.system(filenpa_deploy+" "+tag)
    else:
        msg.warning(release_err_msg[1:])
        sys.exit(1)
