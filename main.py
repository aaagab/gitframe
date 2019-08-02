#!/usr/bin/env python3
# author: Gabriel Auger
# version: 2.2.0
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

	class MyParser(argparse.ArgumentParser):
		def error(self, message):
			sys.stderr.write('error: %s\n' % message)
			self.print_help()
			sys.exit(1)



	parser=MyParser(description="Python wrapper for git. It applies a git workflow close to GitFlow model from nvie.com. It uses semantic versioning 2.0.0")

	parser.add_argument(
		"-d",
		"--debug",  
		action="store_true",
		dest="debug",
		# help="debug mode in order to display all processing steps. Mainly use for testing",
		help=argparse.SUPPRESS
	)
	parser.add_argument(
		"--dv",
		action="store_true",
		dest="disable_validator",
		help="disable gitframe validator. This function should be used only to test and write the deploy_release script. For instance: gitframe --dv --pr v1.0.0",
	)
	parser.add_argument(
		"-c",
		"--cb",  
		"--close-branch",
		action="store_true",
		dest="close_branch",
		help="close current working branch",
	)
	parser.add_argument(
		"--cp",
		"--cptr",  
		"--clone-project-to-remote",
		action="store_true",
		dest="clone_project_to_remote",
		help="clone Project directory to Remote Repository"
	)
	parser.add_argument(
		"--anp",  
		"--automated-new-project",
		action="store_true",
		dest="automated_new_project",
		help="Create a  new project using the processor engine. It avoids having to type multiple times the same entry."
	)
	parser.add_argument(
		"-n",
		"--np",
		"--new-project",
		const=True,
		dest="new_project",
		help="create a new git project. Use relative path or Full Path, existing or not",
		metavar="PATH",
		nargs='?',
	)
	parser.add_argument(
		"-o",
		"--ob",
		"--open-branch",
		action="store_true",
		dest="open_branch",
		help="open branch Feature"
	)
	parser.add_argument(
		"--da",
		"--deploy-args",
		dest="deploy_args",
		help="This parameter can be added to --close-branch for hotfix branch type only. It can also be added to --pick-up-release. The arguments are going to be send to the script deploy",
		metavar="RELEASE_NUMBER",
		nargs='*'
	)
	parser.add_argument(
		"--pr",
		"--pur",
		"--pick-up-release",
		const=True,
		dest="pick_up_release",
		help="select a tag to pick up a release version from. ex: 1.0.0",
		metavar="RELEASE_NUMBER",
		nargs='?'
	)
	parser.add_argument(
		"-s",
		"--sp",
		"--synchronize-project",
		action="store_true",
		dest="synchronize_project",
		help="branching model validator is applied and all branches are synchronized"
	)
	parser.add_argument(
		"-t",
		"--test",
		dest="test",
		# help="launch tests. Tests are by default in debug mode. select Mode is either 'local_path' or 'ssh_url'. 'ssh_url' mode mocks a ssh server on local.",
		help=argparse.SUPPRESS,
		metavar="MODE",
		nargs=1	
	)
	parser.add_argument(
		"-u",
		"--ub",
		"--update-branch",
		action="store_true",
		dest="update_branch",
		help="if active branch has a linked branch, then depending on circumstances, linked branch is merged into active branch"
	)
	parser.add_argument(
		"--ug",
		"--update-gitframe",
		const=True,
		# action="store",
		dest="update_gitframe",
		help="this is for gitframe developers only. This command is needed in order to allow development on gitframe with gitframe. It copies the src code to a temporary folder and execute gitframe from this folder with the remaining parameters. ex: ./gitframe.py --ug=\"--pr\" will execute /tmp/test-gf/bin/gitframe.py --pr. NOTE: --test command does not need --update_gitframe and it must be executed from the main source code.",
		metavar="PARAMETERS",
		nargs='?',
	)
	parser.add_argument(
		"-v",
		"--version",
		action="store_true",
		dest="version",
		help="get program version"
	)
	# Remote_repository(_platform=dy_app["platform"])

	if not sys.argv[1:]:
		parser.print_usage()
		sys.exit(1)

	try:
		args = parser.parse_args()
	except Exception as e:
		print(e)
		sys.exit(1)

	if args.update_gitframe:
		if args.update_gitframe is True:
			pkg.update_gitframe_bin(conf)
		else:
			pkg.update_gitframe_bin(conf, args.update_gitframe)
		sys.exit(0)

	if args.debug is True:
		pkg.msgh.subtitle("Debug mode started")
		conf.set_value("debug", True)
		importlib.reload(msg)

	if args.disable_validator is True:
		pkg.msgh.subtitle("Validator mode disabled")
		conf.data["validator"]=False
		# if not args.pick_up_release and not args.publish_early_release:
		if not args.pick_up_release:
			msg.error(
				"Disable Validator can only be enabled with Pick up Release (--pr tag).",
				"It allows to work quickly with the deploy_release script."
			)
			sys.exit(1)

	if args.close_branch is True:
		if args.deploy_args is None:
			args.deploy_args=[]
		pkg.close_branch(*pkg.validator(conf.data["validator"]), args.deploy_args)
		sys.exit(0)
		
	elif args.new_project is True:
		pkg.new_project()
		sys.exit(0)

	elif args.new_project:
		pkg.new_project(args.new_project)
		sys.exit(0)

	elif args.automated_new_project:
		# pkg.pe.terminal_setup(conf.data, ["new_project"])
		print("Need to be refactored")
		sys.exit(0)

	elif args.clone_project_to_remote is True:
		# repo, regex_branches, all_version_tags=pkg.validator(conf.data["validator"])

		pkg.clone_project_to_remote(pkg.Remote_repository())
		sys.exit(0)

	elif args.open_branch is True:
		pkg.open_branch(*pkg.validator(conf.data["validator"]))
		sys.exit(0)

	elif args.pick_up_release:
		if args.deploy_args is None:
			args.deploy_args=[]

		if args.pick_up_release is True:
			repo, regex_branches, all_version_tags=pkg.validator(conf.data["validator"])
			pkg.create_new_release(repo, regex_branches, all_version_tags, *args.deploy_args)
		else:
			if conf.data["validator"]:
				repo, regex_branches, all_version_tags=pkg.validator(conf.data["validator"])

			pkg.pick_up_release(args.pick_up_release, *args.deploy_args)

	elif args.synchronize_project is True:
		pkg.validator(conf.data["validator"])
		sys.exit(0)

	elif args.test:
		print("Need to be refactored")
		# pkg.pe.terminal_setup(conf.data, args.test)
		sys.exit(0)

	elif args.update_branch is True:
		print("Need to be refactored")
		repo, regex_branches, all_version_tags=pkg.validator(conf.data["validator"])
		pkg.update_branch(all_version_tags)
		sys.exit(0)

	elif args.version is True:
		lspace="  "
		print(lspace+pkg.ft.bold("Name: ")+conf.get_value("app_name"))
		print(lspace+pkg.ft.bold("Author: ")+conf.get_value("author"))
		print(lspace+pkg.ft.bold("License: ")+conf.get_value("license"))
		print(lspace+pkg.ft.bold("Version: ")+conf.get_value("version"))
		sys.exit(0)
