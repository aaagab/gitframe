#!/usr/bin/env python3
import sys
import git_helpers.git_utils as git
import utils.message as msg
import utils.shell_helpers as shell
import re
import git_helpers.regex_obj as ro

# all tags from remote are fetched
# Tags to monitor closely are release and patch
# (release) all tags of form v\d+\.\d+\.\d+ with last d == 0
# (early release) all tags of re.match(r"v\d+\.\d+\.(\d+)-(alpha|beta|rc)(-o|-c)?-\d+" with last d == 0
# (patch) all tags of form v\d+\.\d+\.\d+ with last d > 0

# (start_hotfix tags) all tags of form start_hotfix-\d+\.\d+\.\d+.*
# As a rule Tags are not fetch globally from remote because if two tags with same name but different commits then the one local is updated without prompt with the one from remote. This behaviour is not desired. That is why only tag of importance are fetch automatically, the other tags have to be pushed and fetched manually

def tags_validator(repo):
    msg.subtitle("Local To Remote Tags Validator")

    if repo.is_reachable:
        local_tag_names=get_local_tags()
        remote_tag_names=get_remote_tags()

        for local_tag_name in local_tag_names:
            tag_found_on_remote=False
            for remote_tag_name in remote_tag_names:
                if local_tag_name == remote_tag_name:
                    if compare_commits_from_tag_name(local_tag_name):
                        tag_found_on_remote=True
                        break

            if not tag_found_on_remote:
                process_tag_not_found(local_tag_name, "remote")

        for remote_tag_name in remote_tag_names:
            tag_found_on_local=False
            for local_tag_name in local_tag_names:
                if remote_tag_name == local_tag_name:
                   if compare_commits_from_tag_name(local_tag_name):
                        tag_found_on_local=True
                        break    
            
            if not tag_found_on_local:
                process_tag_not_found(remote_tag_name, "local")

        msg.success("tags_validator passed")
    else:
        msg.warning("Remote is not reachable, Tags can't be compared from local to remote")

def compare_commits_from_tag_name(tag_name):
    msg.dbg("info","compare commits with tag name '"+tag_name+"'")
    # compare commit
    local_tag_commit=git.get_commit_from_tag(tag_name, "local")
    remote_tag_commit=git.get_commit_from_tag(tag_name, "remote")
    msg.dbg("info",local_tag_commit+", "+remote_tag_commit)

    if local_tag_commit == remote_tag_commit:
        msg.dbg("success", sys._getframe(  ).f_code.co_name)
        return True
    else:
        msg.user_error(
            "local tag '"+tag_name+"' with commit '"+local_tag_commit+"' is different than: ",
            "remote tag '"+tag_name+"' with commit '"+remote_tag_commit+"'",
            "Correct issue."
        )
        sys.exit(1)

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

def get_local_tags():
    tags=shell.cmd_get_value("git tag")
    if tags:
        return tags.splitlines()
    else:
        return []

def get_remote_tags():
    tags=shell.cmd_get_value("git ls-remote --tags origin")
    tmp_tags=[]
    for tag in tags.splitlines():
        this_match=re.match(r"^refs/tags/(.*)$", tag.split("\t")[1])
        if this_match:
            tmp_tags.append(this_match.group(1))
        else:
            msg.app_error(
                "'git ls-remote --tags origin' does not return a string of the form: ",
                "['8ca335fd8c80fe3e584b5ad0981dbf906dd73a4d\trefs/tags/v1.0.0']",
                "instead it returns: "+tag
            )
            sys.exit(1)
    return tmp_tags
        