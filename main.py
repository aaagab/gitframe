#!/usr/bin/env python3
# author: Gabriel Auger
# version: 4.1.1
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
	# conf.data["validator"]=True




	pkg.install_dependencies(conf.get_value("deps"))
	filenpa_script=os.path.realpath(__file__)
	direpa_script=os.path.dirname(filenpa_script)
	dy_app=None
	filenpa_json=os.path.join(direpa_script, "config", "config.json")	
	with open(filenpa_json, 'r') as f:
		dy_app=json.load(f)

	dy_app["platform"]=platform.system()

	args, dy_app=pkg.Options(filenpa_app="gpm.json", filenpa_args="config/options.json").get_argsns_dy_app()

	if args.update_gitframe.here:
		pkg.update_gitframe_bin(conf, args.update_gitframe.value)
		sys.exit(0)

	if args.debug.here:
		pkg.msgh.subtitle("Debug mode started")
		conf.set_value("debug", True)
		importlib.reload(msg)

	if args.disable_validator.here:
		pkg.msgh.subtitle("Validator mode disabled")
		conf.data["validator"]=False
		# if not args.pick_up_release and not args.publish_early_release:
		if args.pick_up_release.here is False:
			msg.error(
				"Disable Validator can only be enabled with Pick up Release (--pr tag).",
				"It allows to work quickly with the deploy_release script."
			)
			sys.exit(1)

	if args.close_branch.here:
		pkg.close_branch(*pkg.validator(conf.data["validator"]), args.deploy_args.values)
		sys.exit(0)
	elif args.examples.here:
		print("""
gitframe --init . ../doc --username user --email user@email.com
gitframe --clone-to-repository . ../doc --repository /data/git --package gitlib --add-origin --sync
gitframe --set-origin /data/git/g/gitframe/1/src.git --project . --sync
gitframe --tag --version-file gpm.json
		""")
	elif args.clone_to_repository.here or args.clone_to_directory.here:
		direpa_dst=None
		projects_paths=None
		if args.clone_to_repository.here:
			direpa_dst=args.repository.value
			projects_paths=args.clone_to_repository.values
		elif args.clone_to_directory.here:
			direpa_dst=args.directory.value
			projects_paths=args.clone_to_directory.values
		
		pkg.clone(
			add_origin=args.add_origin.here,
			direpa_dst=direpa_dst,
			index=args.index.value,
			is_repo=args.repository.here,
			package_name=args.package.value,
			projects_paths=projects_paths,
			sync=args.sync.here,
		)
	elif args.init.here:
		pkg.init(
			direpas=args.init.values,
			email=args.email.value,
			username=args.username.value,
		)
		sys.exit(0)	
	elif args.new_project.here:
		pkg.new_project(args.new_project.value)
		sys.exit(0)
	elif args.automated_new_project.here:
		pkg.pe.terminal_setup(conf.data, ["new_project"])
		# print("Need to be refactored")
		sys.exit(0)

	elif args.clone_project_to_remote.here:
		# repo, regex_branches, all_version_tags=pkg.validator(conf.data["validator"])

		pkg.clone_project_to_remote(pkg.Remote_repository())
		sys.exit(0)

	elif args.open_branch.here:
		pkg.open_branch(*pkg.validator(conf.data["validator"]))
		sys.exit(0)

	elif args.pick_up_release.here:
		if args.pick_up_release.here:
			repo, regex_branches, all_version_tags=pkg.validator(conf.data["validator"])
			pkg.create_new_release(repo, regex_branches, all_version_tags, *args.deploy_args.values)
		else:
			if conf.data["validator"]:
				repo, regex_branches, all_version_tags=pkg.validator(conf.data["validator"])

			pkg.pick_up_release(args.pick_up_release.value, *args.deploy_args.values)
	elif args.set_origin.here:
		pkg.set_origin(
			branches=args.sync.values,
			path_origin=args.set_origin.value,
			path_git=args.project.value,
			sync=args.sync.here,
		)
	elif args.synchronize_project.here:
		pkg.validator(conf.data["validator"])
		sys.exit(0)
	elif args.tag.here:
		repo, regex_branches, all_version_tags=pkg.validator(conf.data["validator"])
		pkg.tag(
			all_version_tags=all_version_tags,
			repo=repo,
			tag=args.tag.value,
			version_file=args.version_file.value
		)
	elif args.test.here:
		print("Need to be refactored")
		# pkg.pe.terminal_setup(conf.data, args.test)
		sys.exit(0)

	elif args.update_branch.here:
		print("Need to be refactored")
		repo, regex_branches, all_version_tags=pkg.validator(conf.data["validator"])
		pkg.update_branch(all_version_tags)
		sys.exit(0)

	elif args.version.here:
		lspace="  "
		print(lspace+pkg.ft.bold("Name: ")+conf.get_value("app_name"))
		print(lspace+pkg.ft.bold("Author: ")+conf.get_value("author"))
		print(lspace+pkg.ft.bold("License: ")+conf.get_value("license"))
		print(lspace+pkg.ft.bold("Version: ")+conf.get_value("version"))
		sys.exit(0)



	# class MyParser(argparse.ArgumentParser):
	# 	def error(self, message):
	# 		sys.stderr.write('error: %s\n' % message)
	# 		self.print_help()
	# 		sys.exit(1)



	# parser=MyParser(description="Python wrapper for git. It applies a git workflow close to GitFlow model from nvie.com. It uses semantic versioning 2.0.0")

	# parser.add_argument(
	# 	"-d",
	# 	"--debug",  
	# 	action="store_true",
	# 	dest="debug",
	# 	# help="debug mode in order to display all processing steps. Mainly use for testing",
	# 	help=argparse.SUPPRESS
	# )
	# parser.add_argument(
	# 	"--dv",
	# 	action="store_true",
	# 	dest="disable_validator",
	# 	help="disable gitframe validator. This function should be used only to test and write the deploy_release script. For instance: gitframe --dv --pr v1.0.0",
	# )
	# parser.add_argument(
	# 	"-c",
	# 	"--cb",  
	# 	"--close-branch",
	# 	action="store_true",
	# 	dest="close_branch",
	# 	help="close current working branch",
	# )
	# parser.add_argument(
	# 	"--cp",
	# 	"--cptr",  
	# 	"--clone-project-to-remote",
	# 	action="store_true",
	# 	dest="clone_project_to_remote",
	# 	help="clone Project directory to Remote Repository"
	# )
	# parser.add_argument(
	# 	"--anp",  
	# 	"--automated-new-project",
	# 	action="store_true",
	# 	dest="automated_new_project",
	# 	help="Create a  new project using the processor engine. It avoids having to type multiple times the same entry."
	# )
	# parser.add_argument(
	# 	"-n",
	# 	"--np",
	# 	"--new-project",
	# 	const=True,
	# 	dest="new_project",
	# 	help="create a new git project. Use relative path or Full Path, existing or not",
	# 	metavar="PATH",
	# 	nargs='?',
	# )
	# parser.add_argument(
	# 	"-o",
	# 	"--ob",
	# 	"--open-branch",
	# 	action="store_true",
	# 	dest="open_branch",
	# 	help="open branch Feature"
	# )
	# parser.add_argument(
	# 	"--da",
	# 	"--deploy-args",
	# 	dest="deploy_args",
	# 	help="This parameter can be added to --close-branch for hotfix branch type only. It can also be added to --pick-up-release. The arguments are going to be send to the script deploy",
	# 	metavar="RELEASE_NUMBER",
	# 	nargs='*'
	# )
	# parser.add_argument(
	# 	"--pr",
	# 	"--pur",
	# 	"--pick-up-release",
	# 	const=True,
	# 	dest="pick_up_release",
	# 	help="select a tag to pick up a release version from. ex: 1.0.0",
	# 	metavar="RELEASE_NUMBER",
	# 	nargs='?'
	# )
	# parser.add_argument(
	# 	"-s",
	# 	"--sp",
	# 	"--synchronize-project",
	# 	action="store_true",
	# 	dest="synchronize_project",
	# 	help="branching model validator is applied and all branches are synchronized"
	# )
	# parser.add_argument(
	# 	"-t",
	# 	"--test",
	# 	dest="test",
	# 	# help="launch tests. Tests are by default in debug mode. select Mode is either 'local_path' or 'ssh_url'. 'ssh_url' mode mocks a ssh server on local.",
	# 	help=argparse.SUPPRESS,
	# 	metavar="MODE",
	# 	nargs=1	
	# )
	# parser.add_argument(
	# 	"-u",
	# 	"--ub",
	# 	"--update-branch",
	# 	action="store_true",
	# 	dest="update_branch",
	# 	help="if active branch has a linked branch, then depending on circumstances, linked branch is merged into active branch"
	# )
	# parser.add_argument(
	# 	"--ug",
	# 	"--update-gitframe",
	# 	const=True,
	# 	# action="store",
	# 	dest="update_gitframe",
	# 	help="this is for gitframe developers only. This command is needed in order to allow development on gitframe with gitframe. It copies the src code to a temporary folder and execute gitframe from this folder with the remaining parameters. ex: ./gitframe.py --ug=\"--pr\" will execute /tmp/test-gf/bin/gitframe.py --pr. NOTE: --test command does not need --update_gitframe and it must be executed from the main source code.",
	# 	metavar="PARAMETERS",
	# 	nargs='?',
	# )
	# parser.add_argument(
	# 	"-v",
	# 	"--version",
	# 	action="store_true",
	# 	dest="version",
	# 	help="get program version"
	# )
	# Remote_repository(_platform=dy_app["platform"])

	# if not sys.argv[1:]:
	# 	parser.print_usage()
	# 	sys.exit(1)

	# try:
	# 	args = parser.parse_args()
	# except Exception as e:
	# 	print(e)
	# 	sys.exit(1)
