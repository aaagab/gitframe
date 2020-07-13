#!/usr/bin/env python3
from pprint import pprint
import os
import sys

from .get_all_branch_regexes import get_all_branch_regexes
from .get_all_version_tags import get_all_version_tags
from .prompt_for_commit import prompt_for_commit
from .remote_repository import Remote_repository
from .synchronize_branch_type import synchronize_branch_type
from .synchronize_branch_name import synchronize_branch_name
from .validator.check_master_develop_exists import check_master_develop_exists
from .validator.synchronize_tags import synchronize_tags
from .validator.version_tags import version_tags_validator

from . import git_utils as git
from . import msg_helpers as msgh

from ..gpkgs import message as msg


# this file tries to guarantee that the git flow structure is preserved so it runs once at start of each command to detect issues early.
def validator(enabled, commit_message=None):

	# print(enabled)
	# input("ia m here")
	if not git.is_git_project():
		msg.error(
			"Current Path '{}' is not in a git project directory".format(os.getcwd()),
			"cd into another directory or create a new project"
		)
		sys.exit(1)

	if not enabled:
		prompt_for_commit(commit_message=commit_message)
		repo=Remote_repository()
		regex_branches=get_all_branch_regexes(repo)
		all_version_tags=get_all_version_tags()

		return repo, regex_branches, all_version_tags
	else:
		msg.info("Git Frame Validator")

		prompt_for_commit(commit_message=commit_message)

		repo=Remote_repository()
		regex_branches=get_all_branch_regexes(repo)

		check_master_develop_exists(regex_branches)
		synchronize_branch_name(repo, regex_branches, "master")
		synchronize_branch_name(repo, regex_branches, "develop")
		synchronize_branch_type(repo, regex_branches, "features")
		synchronize_branch_type(repo, regex_branches, "support")
		synchronize_branch_type(repo, regex_branches, "hotfix")
		
		synchronize_tags(repo)

		regex_branches=get_all_branch_regexes(repo)

		all_version_tags=get_all_version_tags()
		version_tags_validator(regex_branches, all_version_tags)

		msg.dbg("success", sys._getframe().f_code.co_name)
		return repo, regex_branches, all_version_tags
