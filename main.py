#!/usr/bin/env python3
# author: Gabriel Auger
# version: 9.1.0
# name: gitframe
# license: MIT

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

	conf = pkg.Json_config()
	conf.set_value("debug", False)
	conf.data["direpa_dev_sources"]=conf.data["direpa_dev_sources"].format(user_profile=os.path.expanduser("~"))

	pkg.install_dependencies(conf.get_value("deps"))
	filenpa_script=os.path.realpath(__file__)
	direpa_script=os.path.dirname(filenpa_script)
	dy_app=None
	filenpa_json=os.path.join(direpa_script, "config", "config.json")	
	with open(filenpa_json, 'r') as f:
		dy_app=json.load(f)

	dy_app["platform"]=platform.system()

	args, dy_app=pkg.Options(filenpa_app="gpm.json", filenpa_args="config/options.json").get_argsns_dy_app()

	direpa_repository=os.path.join(os.path.expanduser("~"), "fty", "src")

	if args.update_gitframe.here:
		pkg.update_gitframe_bin(conf, args.update_gitframe.value)
		sys.exit(0)

	if args.debug.here:
		pkg.msg.info("Debug mode started")
		conf.set_value("debug", True)
		importlib.reload(msg)

	if args.disable_validator.here:
		pkg.msg.info("Validator mode disabled")
		conf.data["validator"]=False
		# if not args.pick_up_release and not args.publish_early_release:
		if args.pick_up_release.here is False:
			msg.error(
				"Disable Validator can only be enabled with Pick up Release (--pr tag).",
				"It allows to work quickly with the deploy_release script."
			)
			sys.exit(1)


	elif args.examples.here:
		print(r"""
gitframe --set-project . ../doc --username user --email user@email.com --init --branches develop
gitframe --clone-to-repository . ../doc --repository ~/fty/git --package gitlib --add-origin --sync
gitframe --clone-to-repository . ..\doc ..\mgt --repository %userprofile%\fty\git --package git_test --add-origin --sync
gitframe --set-origin ~/fty/git/g/gitframe/1/src.git --project . --sync
release --bump-version --increment
gitframe --tag --version-file gpm.json
gitframe --branch fts-at_work --commit "adding base files" --open
gitframe --branch --open # support
release --bump-version --increment # only minor or patch
gitframe --tag --version-file gpm.json
gitframe --update . ..\doc
		""")
	elif args.clone_to_repository.here or args.clone_to_directory.here:
		direpa_dst=None
		projects_paths=None
		if args.clone_to_repository.here:
			if args.repository.value is None:
				direpa_dst=direpa_repository
			else:
				direpa_dst=args.repository.value
			projects_paths=args.clone_to_repository.values
		elif args.clone_to_directory.here:
			direpa_dst=args.directory.value
			projects_paths=args.clone_to_directory.values

		pkg.clone(
			add_origin=args.add_origin.here,
			diren_git=args.diren_git.value,
			direpa_dst=direpa_dst,
			index=args.index.value,
			is_repo=args.repository.here,
			package_name=args.package.value,
			projects_paths=projects_paths,
			shared=args.shared.value,
			sync=args.sync.here,
		)
	elif args.update_gitignore.here:
		pkg.update_gitignore(
			direpa=args.update_gitignore.value,
		)
		sys.exit(0)	
	elif args.set_project.here:
		pkg.set_project(
			branches=args.branches.values,
			direpas=args.set_project.values,
			email=args.email.value,
			init=args.init.here,
			shared=args.shared.value,
			username=args.username.value,
		)
		sys.exit(0)	
	elif args.branch.here:
		if args.open.here:
			pkg.open_branch(
				branch_name=args.branch.value,
				commit_message=args.commit.value,
				direpa_src=args.path_src.value,
				set_upstream=args.set_upstream.here,
			)
			sys.exit(0)
		elif args.close.here:
			print("Need to be refactored")
			sys.exit(1)
			pkg.close_branch(
				branch_name=args.branch.value,
				commit_message=args.commit.value,
				direpa_src=args.path_src.value,
			)
			sys.exit(0)
	elif args.update.here:
		pkg.update_branch(
			commit_message=args.commit.value,
			projects_paths=args.update.values,
			
		)
		sys.exit(0)

	elif args.set_origin.here:
		pkg.set_origin(
			branches=args.sync.values,
			path_origin=args.set_origin.value,
			path_git=args.project.value,
			sync=args.sync.here,
		)
	elif args.synchronize_project.here:
		pkg.validator(
			conf.data["validator"],
			commit_message=args.commit.value,
			direpa_src=args.path_src.value,
		)
		sys.exit(0)
	elif args.tag.here:
		pkg.tag(
			commit_message=args.commit.value,
			direpa_src=args.path_src.value,
			tag=args.tag.value,
			version_file=args.version_file.value
		)


