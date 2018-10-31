#!/usr/bin/env python3
import os
import utils.message as msg
import utils.shell_helpers as shell
import sys
import re

def has_git_directory(path=""):
    start_path=""
    git_directory_found=False

    if path:
        start_path=os.getcwd()
        os.chdir(path)

    if os.path.exists(".git"):
        if shell.cmd_devnull("git rev-parse --git-dir") == 0:
            git_directory_found=True

    if path:
        os.chdir(start_path)

    if not git_directory_found:
        return False
    else:
        return True

def get_root_dir_name():
    root_dir=shell.cmd_get_value("git rev-parse --show-toplevel")
    return os.path.basename(root_dir)

def get_root_dir_path():
    root_dir=shell.cmd_get_value("git rev-parse --show-toplevel")
    return root_dir

def get_active_branch_name():
    branch_name=shell.cmd_get_value("git rev-parse --abbrev-ref HEAD")
    if not branch_name:
        msg.app_error("No branch name from command git rev-parse --abbrev-ref HEAD")
        sys.exit(1)
    else:
        return branch_name

def is_branch_on_remote(this_branch=""):
    if not this_branch:
        this_branch=get_active_branch_name()

    result=shell.cmd_get_value("git ls-remote --heads origin \""+this_branch+"\"")
    if not result:
        return False
    else:
        return True

def is_branch_on_local(this_branch=""):
    if not this_branch:
        this_branch=get_active_branch_name()

    if shell.cmd_devnull("git rev-parse --verify \""+this_branch+"\"") == 0:
        return True
    else:
        return False

def is_branch_on_local_remote(this_branch=""):
    if not this_branch:
        this_branch=get_active_branch_name()

    if shell.cmd_devnull("git rev-parse --verify \"origin/"+this_branch+"\"") == 0:
        return True
    else:
        return False

def checkout(branch_name):
    if get_active_branch_name() != branch_name:
        shell.cmd_prompt('git checkout --quiet '+branch_name)

def checkoutb(branch_txt):
    branch_name=""
    if len(branch_name.split(" ")) == 2:
        branch_name, from_commit = branch_name.split(" ")
    else:
        branch_name=branch_txt
        
    if get_active_branch_name() != branch_name:
        shell.cmd_prompt('git checkout -b '+branch_txt)

def commit(message):
    msg.info("commit on branch \""+get_active_branch_name()+"\" with message "+message)
    files_to_commit=shell.cmd_get_value("git status --porcelain")
    if files_to_commit:
        print("__untracked files present__")
        for f in files_to_commit.splitlines():
            print("  "+str(f))

        if shell.cmd("git add .") == 0:
            msg.success("Files added.")
            if shell.cmd("git commit -a -m \""+message+"\"") == 0:
                msg.success("Files committed.")
            else:
                msg.app_error("Committing Files Failed!")
        else:
            msg.app_error("Adding Files Failed!")
    else:
        msg.info("No Files To Commit")

def get_local_branch_names():
        raw_branches=shell.cmd_get_value("git branch").splitlines()
        branches=[]
        # remove the asterisk and strip all
        for branch in raw_branches:
            branches.append(re.sub("^\* ","",branch).strip())

        return branches

def get_heads_remote_branch_names(repo):
    # string format
    # d06a492857eea71f64c51257ec81645e50f40957        refs/heads/develop
    raw_branches=shell.cmd_get_value("git ls-remote origin").splitlines()
    branches=[]
    # remove all unneeded string

    if repo.is_reachable:
        if repo.has_directory:
            for branch in raw_branches:
                if re.match("^.*?refs/heads/.*$", branch):
                    branches.append(re.sub("^.*?refs/heads/","",branch).strip())
        else:
            msg.warning("Branches on Remote Cannot be retrieved.",
                "Validator is going to be partially executed.")
    else:
        msg.warning("Branches on Remote Cannot be retrieved.",
                "Validator is going to be partially executed.")

    return branches

def get_local_remote_branch_names(remote_name="origin"):
    # string format
    # origin/develop
    raw_branches=shell.cmd_get_value("git branch -r").splitlines()
    branches=[]
    # remove all unneeded string
    for branch in raw_branches:
        branches.append(re.sub("^.*?"+remote_name+"/","",branch).strip())

    return branches

def fetch_tags():
    shell.cmd_prompt('git fetch --tags')

def set_annotated_tags(repo, tag, txt):
    shell.cmd_prompt("git tag -a "+tag+" -m '"+txt+"'")
    if repo.is_reachable:
        shell.cmd_prompt('git push origin '+tag)
    else:
        msg.warning("Tag "+tag+" can't been pushed to Remote.")

def merge_noff(branch_name):
    shell.cmd_prompt("git merge --no-edit --no-ff "+branch_name)

def merge(branch_name):
    shell.cmd_prompt("git merge --no-edit "+branch_name)
    
def delete_local_branch(branch_name):
    shell.cmd_prompt("git branch --delete "+branch_name)

def delete_origin_branch(repo, branch_name):
    if repo.is_reachable:
        if is_branch_on_remote(branch_name):
            shell.cmd_prompt("git push origin --delete "+branch_name)
        else:
            msg.warning("'"+branch_name+"' can't be deleted because it does not exist on remote.")
    else:
        msg.warning(
            "Remote repository is not reachable",
            "Branch '"+branch_name+"' can't be delete on remote for now."
            )

def push_origin(repo, branch_name):
    if repo.is_reachable:
        shell.cmd_prompt("git push origin "+branch_name)
    else:
        msg.warning(
            "Remote repository is not reachable",
            "Branch '"+branch_name+"' can't be pushed for now."
        )

def commit_empty(txt):
    shell.cmd_prompt("git commit --allow-empty -m \""+txt+"\"")
    
def get_commit_from_tag(tag, location="local"):
    if location == "local":
        for line in shell.cmd_get_value("git show "+tag).splitlines():
            if re.match(r"^commit (.*)", line):
                return re.sub(r"^commit (.*)", r"\1", line)
    elif location == "remote":
        for line in shell.cmd_get_value("git ls-remote --tags origin").splitlines():
            this_match=re.match(r"^refs/tags/(.*)$", line.split("\t")[1])
            if this_match:
                if tag == this_match.group(1):
                    return line.split("\t")[0]
            else:
                msg.app_error(
                    "'git ls-remote --tags origin' does not return a string of the form: ",
                    "['8ca335fd8c80fe3e584b5ad0981dbf906dd73a4d\trefs/tags/v1.0.0']",
                    "instead it returns: "+line
                )
                sys.exit(1)
    return ""

def get_latest_release_for_each_major(all_version_tags):
    import git_helpers.regex_obj as ro
    
    all_major_array=[]
    tmp_array=[]
    tag_major_array=[]
    regex_version=ro.Version_regex()
    for i, tag in enumerate(all_version_tags):
        tag_major_array.append(regex_version.set_text(tag).major)
        if i == len(all_version_tags) - 1:
            if i == 0:
                tmp_array.append(tag)
                all_major_array.append(tmp_array)
            else:
                if tag_major_array[i] == tag_major_array[i-1]:
                    tmp_array.append(tag)
                    all_major_array.append(tmp_array)
                else:
                    all_major_array.append(tmp_array)
                    tmp_array=[]
                    tmp_array.append(tag)
                    all_major_array.append(tmp_array)
        else:
            if i == 0:
                tmp_array.append(tag)
            else:
                if tag_major_array[i] == tag_major_array[i-1]:
                    tmp_array.append(tag)
                else:
                    all_major_array.append(tmp_array)
                    tmp_array=[]
                    tmp_array.append(tag)

    latest_release_array=[]
    for major in all_major_array:
        latest_release_array.append(major[-1])

    return latest_release_array

def get_branch_compare_status(active_branch, compare_branch):
    active_branch_last_commit=shell.cmd_get_value("git rev-parse "+active_branch)
    compare_branch_last_commit=shell.cmd_get_value("git rev-parse "+compare_branch)
    common_ancestor=shell.cmd_get_value("git merge-base "+active_branch+" "+compare_branch)
    
    if active_branch_last_commit == compare_branch_last_commit:
        return "up_to_date"
    elif active_branch_last_commit == common_ancestor:
        return "pull"
    elif compare_branch_last_commit == common_ancestor:
        return "push"
    else:
        if common_ancestor:
            return "divergent_with_common_ancestor"
        else:
            return "divergent_without_common_ancestor"
    