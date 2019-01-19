#!/usr/bin/env python3
import os, sys
from utils.format_text import Format_text as ft
from utils.prompt import prompt, prompt_boolean

import git_helpers.git_utils as git

# os.system("ls /etc")
# os.system("ls /etc")
# prompt("I am here")
# prompt_boolean("hello")
# sys.exit()

if os.name != 'posix':
	print("This program has been created for debian Linux.")
	sys.exit(1)	

from utils.json_config import Json_config
conf = Json_config()
conf.set_value("debug", False)
conf.data["validator"]=True

import getopt
from utils.install_dependencies import install_dependencies
from git_helpers.remote_repository import Remote_repository
import utils.message as msg
import importlib

import git_helpers.version as version

from git_helpers.main_validator import validator

import argparse
from pprint import pprint

if __name__ == "__main__":
	install_dependencies(conf.get_value("deps"))

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

	if not sys.argv[1:]:
		parser.print_usage()
		sys.exit(1)

	try:
		args = parser.parse_args()
	except Exception as e:
		print(e)
		sys.exit(1)

	if args.update_gitframe:
		from git_helpers.update_gitframe_bin import update_gitframe_bin
		if args.update_gitframe is True:
			update_gitframe_bin(conf)
		else:
			update_gitframe_bin(conf, args.update_gitframe)
		sys.exit(0)

	if args.debug is True:
		msg.subtitle("Debug mode started")
		conf.set_value("debug", True)
		importlib.reload(msg)

	if args.disable_validator is True:
		msg.subtitle("Validator mode disabled")
		conf.data["validator"]=False
		# if not args.pick_up_release and not args.publish_early_release:
		if not args.pick_up_release:
			msg.user_error(
				"Disable Validator can only be enabled with Pick up Release (--pr tag).",
				"It allows to work quickly with the deploy_release script."
			)
			sys.exit(1)

	if args.close_branch is True:
		from git_helpers.close_branch import close_branch
		if args.deploy_args is None:
			args.deploy_args=[]
		close_branch(*validator(conf.data["validator"]), args.deploy_args)
		sys.exit(0)
		
	elif args.new_project is True:
		from git_helpers.new_project import new_project
		new_project()
		sys.exit(0)

	elif args.new_project:
		from git_helpers.new_project import new_project
		new_project(args.new_project)
		sys.exit(0)

	elif args.automated_new_project:
		import processor.utils.processor_engine as pe
		pe.terminal_setup(conf.data, ["new_project"])
		sys.exit(0)

	elif args.clone_project_to_remote is True:
		from git_helpers.clone_project_to_remote import clone_project_to_remote
		# repo, regex_branches, all_version_tags=validator(conf.data["validator"])

		clone_project_to_remote(Remote_repository())
		sys.exit(0)

	elif args.open_branch is True:
		from git_helpers.open_branch import open_branch
		open_branch(*validator(conf.data["validator"]))
		sys.exit(0)

	elif args.pick_up_release:
		from git_helpers.pick_up_release import pick_up_release
		from git_helpers.create_new_release import create_new_release

		if args.deploy_args is None:
			args.deploy_args=[]

		if args.pick_up_release is True:
			repo, regex_branches, all_version_tags=validator(conf.data["validator"])
			create_new_release(repo, regex_branches, all_version_tags, *args.deploy_args)
		else:
			if conf.data["validator"]:
				repo, regex_branches, all_version_tags=validator(conf.data["validator"])

			pick_up_release(args.pick_up_release, *args.deploy_args)

	elif args.synchronize_project is True:
		validator(conf.data["validator"])
		sys.exit(0)

	elif args.test:
		import processor.utils.processor_engine as pe
		pe.terminal_setup(conf.data, args.test)
		sys.exit(0)

	elif args.update_branch is True:
		from git_helpers.update_branch import update_branch			
		repo, regex_branches, all_version_tags=validator(conf.data["validator"])
		update_branch(all_version_tags)
		sys.exit(0)

	elif args.version is True:
		lspace="  "
		print(lspace+ft.bold("Name: ")+conf.get_value("app_name"))
		print(lspace+ft.bold("Author: ")+conf.get_value("author"))
		print(lspace+ft.bold("License: ")+conf.get_value("license"))
		print(lspace+ft.bold("Version: ")+conf.get_value("version"))
		sys.exit(0)
