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
	# help="disable gitframe validator. Mainly use for testing",
	help=argparse.SUPPRESS
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
except:
	sys.exit(1)

if args.debug is True:
	msg.subtitle("Debug mode started")
	conf.set_value("debug", True)
	importlib.reload(msg)

if args.disable_validator is True:
	msg.subtitle("Validator mode disabled")
	conf.data["validator"]=False
	if not args.publish_release:
		msg.user_error(
			"Disable Validator can only be enabled with Publish Release (--pr tag).",
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
	repo, regex_branches, all_version_tags=validator(conf.data["validator"])
	clone_project_to_remote(repo)
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

elif args.publish_release:
	from git_helpers.publish_release import publish_release
	if not conf.data["validator"]:
		publish_release(args.publish_release[0])
	else:
		repo, regex_branches, all_version_tags=validator(conf.data["validator"])
		publish_release(args.publish_release[0], all_version_tags)
	sys.exit(0)

elif args.synchronize_project is True:
	validator(conf.data["validator"])
	sys.exit(0)

elif args.test:
	import processor.processor as processor
	processor.main(args.test[0])
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
