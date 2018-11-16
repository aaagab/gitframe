#!/usr/bin/env python3
import sys
import git_helpers.git_utils as git
import utils.message as msg
import utils.shell_helpers as shell
import re
import git_helpers.regex_obj as ro
from git_helpers.tags_commits import Tags_commits
from copy import deepcopy

# all tags from remote are fetched
# Tags to monitor closely are release and patch
# (release) all tags of form v\d+\.\d+\.\d+ with last d == 0
# (early release) all tags of re.match(r"v\d+\.\d+\.(\d+)-(alpha|beta|rc)(-o|-c)?-\d+" with last d == 0
# (patch) all tags of form v\d+\.\d+\.\d+ with last d > 0

# (start_hotfix tags) all tags of form start_hotfix-\d+\.\d+\.\d+.*
# As a rule Tags are not fetch globally from remote because if two tags with same name but different commits then the one local is updated without prompt with the one from remote. This behaviour is not desired. That is why only tag of importance are fetch automatically, the other tags have to be pushed and fetched manually

def err_msg_commit(name, tags_commits):
    msg.user_error(
        "local tag '"+name+"' with commit '"+tags_commits["local"][name]+"' is different than: ",
        "remote tag '"+name+"' with commit '"+tags_commits["remote"][name]+"'",
        "Correct issue."
    )
    sys.exit(1)

def tags_validator(repo):
    msg.subtitle("Verify Tags on local and remote")
    from datetime import datetime

    if repo.is_reachable:
        tags_commits=Tags_commits("all")

        local_tags=tags_commits.tags["local"]
        remote_tags=tags_commits.tags["remote"]
        not_found_remote_tags=deepcopy(remote_tags)

        for name in local_tags:
            if name in remote_tags:
                del not_found_remote_tags[name]
                if local_tags[name] != remote_tags[name]:
                    err_msg_commit(name, tags_commits)
            else:
                process_tag_not_found(name, "remote")

        for name in not_found_remote_tags:
            process_tag_not_found(name, "local")

        msg.dbg("success", sys._getframe(  ).f_code.co_name)
    else:
        msg.warning("Remote is not reachable, Tags can't be compared from local to remote")

def process_tag_not_found(tag_name, not_found_location):

    regex_version=ro.Version_regex().set_text_if_tag_match(tag_name)
    regex_hotfix=ro.Hotfix_regex().set_text_if_tag_match(tag_name)
    regex_early_release=ro.Early_release_regex().set_text_if_tag_match(tag_name)

    if regex_version.match or regex_early_release.match or regex_hotfix.match:
        if not_found_location=="remote":
            msg.user_error("tag '"+tag_name+"' exists on local but not on remote. tag not pushed.")
        elif not_found_location == "local":
            msg.user_error("tag '"+tag_name+"' exists on remote but not on local. tag not pulled.")

        if regex_version.match:
            # for release
            if int(regex_version.patch) == 0:
                if not_found_location=="remote":
                    msg.user_error("Maybe master branch needs to be pushed with the tag.")
                elif not_found_location == "local":
                    msg.user_error("Maybe master branch needs to be pulled with the tag.")

            # for patch
            elif int(regex_version.patch) > 0:
                if not_found_location=="remote":
                    msg.user_error("Maybe a support branch or master needs to be pushed with the tag.")
                elif not_found_location == "local":
                    msg.user_error("Maybe a support branch or master needs to be pulled with the tag.")

        elif regex_early_release.match:
            if not_found_location=="remote":
                msg.user_error("Define from which branch this tag has been generated and push the branch with the tag.")
            elif not_found_location == "local":
                msg.user_error("Define from which branch this tag has been generated and pull the branch with the tag.")

        elif regex_hotfix.match:
            if not_found_location=="remote":
                msg.user_error("Maybe a hotfix branch needs to be pushed with the tag.")
            elif not_found_location == "local":
                msg.user_error("Maybe a hotfix branch needs to be pulled with the tag.")
    else: # less important tag
        if not_found_location=="remote":
            msg.warning("tag '"+tag_name+"' exists on local but not on remote. tag not pushed.")
        elif not_found_location == "local":
            msg.warning("tag '"+tag_name+"' exists on remote but not on local. tag not pulled.")

        return

    sys.exit(1)
