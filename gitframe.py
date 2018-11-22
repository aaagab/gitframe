#!/usr/bin/env python3
import os, sys
from utils.format_text import Format_text as ft

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

def is_direpa_dev_sources(conf, path=""):
	import git_helpers.git_utils as git
	is_direpa_dev_sources=True
	if path:
		if git.has_git_directory(path):

			if os.path.exists(
				os.path.join(
					git.get_root_dir_path(path),
					conf.data["processor"]["filen_launcher"]
					)
				):
				return True
			else:
				return False
		else:
			return False
	else:
		if git.has_git_directory():
			if os.path.exists(
				os.path.join(
					git.get_root_dir_path(),
					conf.data["processor"]["filen_launcher"]
					)
				):
				return True
			else:
				return False
		else:
			return False

def get_direpa_dev_sources(conf):
	if is_direpa_dev_sources(conf):
		if conf.data["direpa_dev_sources"] != os.getcwd():
			conf.set_value("direpa_dev_sources", os.getcwd())
	else:
		if conf.data["direpa_dev_sources"]:
			if not os.path.exists(conf.data["direpa_dev_sources"]):
				msg.user_error(
					"Current 'direpa_dev_sources' '{}' does not exists".format(conf.data["direpa_dev_sources"]),
					"Go to real path development sources and run './gitframe.py --update-gitframe' to set direpa_dev_sources."
				)
				sys.exit(1)
			else:
				if not is_direpa_dev_sources(conf, conf.data["direpa_dev_sources"]):
					msg.user_error(
						"Current 'direpa_dev_sources' '{}' exists but it is not the real path development sources for gitframe.".format(conf.data["direpa_dev_sources"]),
						"Go to real path development sources and run './gitframe.py --update-gitframe' to set direpa_dev_sources."
					)
					sys.exit(1)
		else:
			msg.user_error(
				"'direpa_dev_sources' has not been defined",
				"Go to real path development sources and run './gitframe.py --update-gitframe' to set direpa_dev_sources."
			)
			sys.exit(1)

	return conf.data["direpa_dev_sources"]

def update_gitframe_bin(conf, parameters=""):

	from distutils.dir_util import copy_tree
	import shutil
	import git_helpers.git_utils as git

	msg.subtitle("Update Gitframe Bin")
	# msg.info("Make sure you publish a release or early-release when the fix has been applied.")

	direpa_source_app=get_direpa_dev_sources(conf)

	direpa_source_dst=os.path.join(
		conf.data["processor"]["task"]["direpa"],
		conf.data["processor"]["task"]["diren_bin"]
	)

	print(direpa_source_app)
	print(direpa_source_dst)
	# if os.path.exists(direpa_source_dst):
	# 	shutil.rmtree(direpa_source_dst)
	
	# os.makedirs(direpa_source_dst, exist_ok=True)

	# copy_tree(direpa_source_app, direpa_source_dst)
	# shutil.rmtree(os.path.join(direpa_source_dst,".git"))
	# os.remove(os.path.join(direpa_source_dst, "hotfix-history.json"))
	# os.remove(os.path.join(direpa_source_dst, "license.txt"))

	# if no parameters create a new draft
	# if parameters
	# 	if per update per for gitframe
		
	# 	else
	# 		create a draft and then rexecute gitframe with the parameters
	# 		# do I need per yes I can keep it

	if parameters:
		if parameters == "per":
			direpa_previous=os.getcwd()
			if direpa_source_app != direpa_previous:
				os.chdir(direpa_source_app)

			cmd_pd="{} {}".format(
				os.path.join(
					direpa_source_app, 
					conf.data["processor"]["filen_launcher"]
				),
				"--publish-draft"
			)

			cmd_per="{} {}".format(
				conf.data["app_name"],
				"--per"
			)
			
			try:
				os.system(cmd_pd)
				os.system(cmd_per)
			except:
				if direpa_previous != os.getcwd():
					os.chdir(direpa_previous)
				
			if direpa_previous != os.getcwd():
				os.chdir(direpa_previous)

		elif parameters[:4] == "test":
			direpa_previous=os.getcwd()
			if direpa_source_app != direpa_previous:
				os.chdir(direpa_source_app)

			cmd_str="{} {}".format(
				os.path.join(
					direpa_source_app, 
					conf.data["processor"]["filen_launcher"]
				),
				"--publish-draft"
			)
			
			try:
				os.system(cmd_str)
			except:
				if direpa_previous != os.getcwd():
					os.chdir(direpa_previous)
				
			if direpa_previous != os.getcwd():
				os.chdir(direpa_previous)

			cmd_str="{} {}".format(
				conf.data["app_name"],
				parameters
			)
			os.system(cmd_str)
		else:
			direpa_previous=os.getcwd()
			if direpa_source_app != direpa_previous:
				os.chdir(direpa_source_app)

			cmd_str="{} {}".format(
				os.path.join(
					direpa_source_app, 
					conf.data["processor"]["filen_launcher"]
				),
				"--publish-draft"
			)
			
			try:
				os.system(cmd_str)
			except:
				if direpa_previous != os.getcwd():
					os.chdir(direpa_previous)
				
			if direpa_previous != os.getcwd():
				os.chdir(direpa_previous)

			cmd_str="{} {}".format(
				conf.data["app_name"],
				parameters
			)
			os.system(cmd_str)	
	else:
		direpa_previous=os.getcwd()
		if direpa_source_app != direpa_previous:
			os.chdir(direpa_source_app)

		cmd_str="{} {}".format(
			os.path.join(
				direpa_source_app, 
				conf.data["processor"]["filen_launcher"]
			),
			"--publish-draft"
		)
		
		try:
			os.system(cmd_str)
		except:
			if direpa_previous != os.getcwd():
				os.chdir(direpa_previous)
			
		if direpa_previous != os.getcwd():
			os.chdir(direpa_previous)

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
		"--pd",
		"--publish-draft",
		action="store_true",
		dest="publish_draft",
		help="this command works on develop, feature, and release branch. It executes the publish_early_release command but the validator is disabled and it does not keep annotated tags."
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
		"--per",
		"--publish-early-release",
		action="store_true",
		dest="publish_early_release",
		help="this command works on develop, feature, and release branch. It pops up some options to get the right tags and then it publish the version with publish-version"
	)
	parser.add_argument(
		"--pr",
		"--publish-release",
		dest="publish_release",
		help="select a tag to publish a version from. ex: 1.0.0",
		metavar="RELEASE_NUMBER",
		nargs=1
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
		help="this is for gitframe developers only. This command is needed in order to allow development on gitframe with gitframe. It copies the src code to a temporary folder and execute gitframe from this folder with the remaining parameters. ex: ./gitframe.py --ug=\"--per\" will execute /tmp/test-gf/bin/gitframe.py --per. NOTE: --test command does not need --update_gitframe and it must be executed from the main source code.",
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

	if args.update_gitframe is True:
		update_gitframe_bin(conf)
		sys.exit(0)

	if args.update_gitframe:
		update_gitframe_bin(conf, args.update_gitframe)
		sys.exit(0)

	if args.debug is True:
		msg.subtitle("Debug mode started")
		conf.set_value("debug", True)
		importlib.reload(msg)

	if args.disable_validator is True:
		msg.subtitle("Validator mode disabled")
		conf.data["validator"]=False
		if not args.publish_release and not args.publish_early_release:
			msg.user_error(
				"Disable Validator can only be enabled with Publish Release (--pr tag) and Publish Early Release (--per).",
				"It allows to work quickly with the deploy_release script."
			)
			sys.exit(1)

	if args.close_branch is True:
		from git_helpers.close_branch import close_branch
		close_branch(*validator(conf.data["validator"]))
		sys.exit(0)
		
	elif args.new_project is True:
		from git_helpers.new_project import new_project
		new_project()
		sys.exit(0)

	elif args.new_project:
		from git_helpers.new_project import new_project
		new_project(args.new_project)
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

	elif args.publish_early_release is True:
		from git_helpers.publish_early_release import publish_early_release
		repo, regex_branches, all_version_tags=validator(conf.data["validator"])
		publish_early_release(repo, regex_branches)
		sys.exit(0)

	elif args.publish_draft is True:
		from git_helpers.get_all_branch_regexes import get_all_branch_regexes
		from git_helpers.publish_early_release import publish_early_release
		from pprint import pprint

		class Remote_repository:
		    def __init__(self):
		        self.is_reachable=False

		repo=Remote_repository()

		publish_early_release(repo, get_all_branch_regexes(repo), "draft")
		sys.exit(0)



	elif args.publish_release:
		from git_helpers.publish_release import publish_release
		if not conf.data["validator"]:
			publish_release(args.publish_release[0], "release")
		else:
			repo, regex_branches, all_version_tags=validator(conf.data["validator"])
			publish_release(args.publish_release[0], "release", all_version_tags)
		sys.exit(0)

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
