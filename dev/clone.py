#!/usr/bin/env python3
import os
import sys

from ..gpkgs import message as msg
from ..gpkgs.gitlib import GitLib

def get_path(path_elem, exit_not_found=True)-> str:
    if not os.path.isabs(path_elem):
        path_elem=os.path.abspath(path_elem)
    path_elem=os.path.normpath(path_elem)
    if exit_not_found is True:
        if not os.path.exists(path_elem):
            msg.error("Path not found '{}'".format(path_elem))
            sys.exit(1)
    return path_elem

def clone_to_directory(
    direpa_dst:str,
    diren_git:str|None=None,
    direpa_src:str|None=None,
    package_alias:str|None=None,
    shared:str|None=None,
    remote_name: str|None=None,
):
    if direpa_src is None:
        direpa_src=os.getcwd()
    git=GitLib(direpa=direpa_src)
    git.is_direpa_git(fail_exit=True)
    if diren_git is None:
        diren_git=os.path.basename(direpa_src)

    if direpa_dst is None:
        msg.error("directory dst is required", exit=1)

    direpa_dst=get_path(direpa_dst, exit_not_found=False)
    elems=[
        direpa_dst
    ]
    if package_alias is not None:
        elems.append(package_alias)
    elems.append(f"{diren_git}.git")

    direpa_dst_full=os.path.join(*elems)
    finalize_clone(git, direpa_src, direpa_dst_full, shared, remote_name)

def clone_to_repository(
    diren_git:str|None=None,
    direpa_dst:str|None=None,
    direpa_src:str|None=None,
    package_alias:str|None=None,
    shared:str|None=None,
    uuid4:str|None=None,
    remote_name: str|None=None,
):
    if direpa_src is None:
        direpa_src=os.getcwd()
    git=GitLib(direpa=direpa_src)
    git.is_direpa_git(fail_exit=True)
    if diren_git is None:
        diren_git=os.path.basename(direpa_src)

    tmp_direpa_dst:str
    if direpa_dst is None:
        tmp_direpa_dst=os.path.join(os.path.expanduser("~"), "fty", "src")
    else:
        tmp_direpa_dst=get_path(direpa_dst, exit_not_found=False)

    if uuid4 is None:
        msg.error("uuid4 is required")
        sys.exit(1)
    if package_alias is None:
        msg.error("package alias is required")
        sys.exit(1)

    uuid4=uuid4.replace("-", "")
    direpa_dst_full=os.path.join(tmp_direpa_dst, package_alias[0], package_alias, uuid4, diren_git+".git")

    finalize_clone(git, direpa_src, direpa_dst_full, shared, remote_name)

def finalize_clone(
    git: GitLib,
    direpa_src: str,
    direpa_dst: str,
    shared: str|None,
    remote_name: str|None,
):
    os.makedirs(os.path.dirname(direpa_dst), exist_ok=True)
    if os.path.exists(direpa_dst):
        msg.error("directory already exists '{}'".format(direpa_dst), exit=1)
    
    default_branch=git.get_principal_branch_name()

    git.clone(direpa_src, direpa_dst=direpa_dst, bare=True, shared=shared, remote_name=remote_name, default_branch=default_branch)

    if remote_name is None:
        remote_name=git.get_remote_name()
    git.set_remote(name=remote_name, repository_path=direpa_dst)    
