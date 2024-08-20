#!/usr/bin/env python3
import argparse
import getopt
import getpass  
import importlib
import json
import os 
import platform
from pprint import pprint
import sys

if __name__ == "__main__":
    direpa_script_parent=os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    module_name=os.path.basename(os.path.dirname(os.path.realpath(__file__)))
    sys.path.insert(0, direpa_script_parent)
    pkg = importlib.import_module(module_name)
    del sys.path[0]

    args=pkg.Nargs(
        metadata=dict(
            executable="gitframe",
        ),
        options_file="config/options.yaml", 
    ).get_args()

    if args.clone._here is True:
        remote_name=args.clone.remote._value
        diren_git=args.clone.diren_git._value
        direpa_src=args.clone._value
        shared=args.clone.shared._value

        if args.clone.to_directory._here:
            pkg.clone_to_directory(
                remote_name=remote_name,
                diren_git=diren_git,
                direpa_dst=args.clone.to_directory._value,
                direpa_src=direpa_src,
                package_alias=args.clone.to_directory.package._value,
                shared=shared,
            )
            
        elif args.clone.to_repository._here:
            pkg.clone_to_repository(
                remote_name=remote_name,
                diren_git=diren_git,
                direpa_dst=args.clone.to_repository._value,
                direpa_src=direpa_src,
                package_alias=args.clone.to_repository.package._value,
                shared=shared,
                uuid4=args.clone.to_repository.uuid4._value,
            )
            
        else:
            raise Exception("Please provide either --to-directory or --to-repository.")
    elif args.set_project._here:
        pkg.set_project(
            branches=args.set_project.branches._values,
            direpa_src=args.set_project._value,
            email=args.set_project.email._value,
            init=args.set_project.init._here,
            shared=args.set_project.shared._value,
            username=args.set_project.username._value,
        )
    elif args.tag._here:
        
        direpa_src=args.tag.path_src._value
        direpa_previous=os.getcwd()
        if direpa_src is not None and direpa_previous != direpa_src:
            os.chdir(direpa_src)
            
        files:list[pkg.VersionFile]=[]
        for branch in args.tag.file._branches:
            if branch._here is True:
                filetype=branch.filetype._value
                if filetype is not None:
                    filetype=pkg.ManagedFile[filetype.upper()]
                file=pkg.VersionFile(
                    path=branch._value,
                    json_keys=branch.json_keys._values,
                    filetype=filetype,
                )
                files.append(file)

        if direpa_src is not None and direpa_previous != direpa_src:
            os.chdir(direpa_previous)

        increment_type=args.tag.increment._value
        if increment_type is not None:
            increment_type=pkg.IncrementType[increment_type.upper()]

        pkg.tag(
            commit_message=args.tag.msg._value,
            direpa_src=direpa_src,
            pull=args.tag.pull._here,
            increment=args.tag.increment._here,
            increment_type=increment_type,
            files=files,
            version=args.tag.version._value,
            remote_name=args.tag.remote._value,
        )
    elif args.update._here:
        if args.update.gitframe._here:
            pkg.update_gitframe_bin()
        
        elif args.update.gitignore._here:
            pkg.update_gitignore(
                direpa=args.update.gitignore._value,
            )
        elif args.update.branches._here:
            pkg.update_branches(
                project_path=args.update.branches._value,
                commit_message=args.update.branches.msg._value,
                remote_name=args.update.branches.remote._value,
            )
        elif args.update.mgt._here:
            pkg.update_mgt(
                project_path=args.update.mgt._value,
                commit_message=args.update.mgt.msg._value,
                remote_name=args.update.mgt.remote._value,
            )

