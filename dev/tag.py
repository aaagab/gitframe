#!/usr/bin/env python3
from lxml import etree
from pprint import pprint
import json
import os
import sys

from ..gpkgs import message as msg
from ..gpkgs.gitlib import GitLib
from ..gpkgs.bump_version import bump_version, VersionFile, IncrementType

def tag(
    commit_message: str| None = None,
    direpa_src=None,
    pull:bool=False,

    increment: bool = False,
    increment_type: IncrementType | None= None,
    files: list[VersionFile] | None = None,
    version: str | None = None,
    remote_name:str|None=None,
):
    version=bump_version(
        increment=increment,
        increment_type=increment_type,
        files=files,
        version=version,
    )

    git=GitLib(direpa=direpa_src)
    git.is_direpa_git(fail_exit=True)
    dev_branch=git.get_active_branch_name()

    principal_branch=git.get_principal_branch_name()
    if principal_branch is None:
        msg.error(f"Principal branch 'main' must be set in the repo.")
        sys.exit(1)
    if dev_branch == principal_branch:
        msg.error(f"Tag can't be set on principal branch '{dev_branch}'.")
        sys.exit(1)

    if remote_name is None:
        remote_name=git.get_remote_name()

    git.commit(commit_message)
    commands=[
        f'git tag -a v{version} -m "Bump release version {version}"',
        f'git push {remote_name} v{version}',
        f'git checkout {principal_branch}',
        f'git merge --no-edit --no-ff {dev_branch}',
        f'git push {remote_name} {principal_branch}',
        f'git checkout {dev_branch}',
        f'git push {remote_name} {dev_branch}',
    ]
    has_error=False
    try:
        if pull is True:
            for cmd in reversed([
                f'git checkout {principal_branch}',
                f'git pull {remote_name} {principal_branch}',
                f'git checkout {dev_branch}',
                f'git pull {remote_name} {dev_branch}',
                f'git merge --no-edit --no-ff {principal_branch}',
            ]):
                commands.insert(0, cmd)
            for name in [principal_branch, dev_branch]:
                git.checkout(branch_name=name)
                git.pull(remote=remote_name, branch_name=name)
                commands.pop(0)
            git.merge_noff(branch_name=principal_branch)
            commands.pop(0)

        git.set_annotated_tags(f"v{version}", f"Bump release version {version}", remote_names=[remote_name])
        commands.pop(0)
        commands.pop(0)

        git.checkout(principal_branch)
        commands.pop(0)
        git.merge_noff(branch_name=dev_branch)
        commands.pop(0)
        git.push(remote_name=remote_name, branch_name=principal_branch)
        commands.pop(0)

        git.checkout(dev_branch)
        commands.pop(0)
        git.push(remote_name=remote_name, branch_name=dev_branch)
        commands.pop(0)
    except:
        has_error=True
        raise
    finally:
        if has_error is True:
            msg.info(f"Remaining Steps after solving issue at path '{git.direpa_root}':")
            print("\n".join(commands)+"\n")
        