#!/usr/bin/env python3
import sys, os
import utils.message as msg

from git_helpers.validator.release import force_unique_release_branch_name, validate_release_branch_name
from git_helpers.validator.support import check_one_branch_support_max_per_major
from git_helpers.validator.hotfix_history_json import hotfix_history_json_validator
from git_helpers.validator.check_master_develop_exists import check_master_develop_exists
from git_helpers.validator.tags import tags_validator

from git_helpers.synchronize_branch_type import synchronize_branch_type
from git_helpers.synchronize_branch_name import synchronize_branch_name

from git_helpers.get_all_version_tags import get_all_version_tags

from utils.json_config import Json_config

from git_helpers.prompt_for_commit import prompt_for_commit

from git_helpers.remote_repository import Remote_repository

from git_helpers.get_all_branch_regexes import get_all_branch_regexes

from git_helpers.validator.version_file import version_file_validator

import git_helpers.git_utils as git

from pprint import pprint

# this file tries to guarantee that the git flow structure is preserved so it runs once at start of each command to detect issues early.
def validator(enabled):
	if not git.has_git_directory():
		msg.user_error(
			"Current Path '"+os.getcwd()+"' has no .git directory",
			"cd into another directory or create a new project"
		)
		sys.exit(1)

	if not enabled:
		repo=Remote_repository()
		regex_branches=get_all_branch_regexes(repo)
		all_version_tags=get_all_version_tags()

		return repo, regex_branches, all_version_tags
	else:
		msg.title("Git Frame Validator")

		prompt_for_commit()

		repo=Remote_repository()
		regex_branches=get_all_branch_regexes(repo)

		check_master_develop_exists(regex_branches)
		force_unique_release_branch_name(regex_branches)
		synchronize_branch_name(repo, regex_branches, "master")
		synchronize_branch_name(repo, regex_branches, "develop")

		synchronize_branch_type(repo, regex_branches, "feature")
		synchronize_branch_type(repo, regex_branches, "support")
		synchronize_branch_type(repo, regex_branches, "release")
		synchronize_branch_type(repo, regex_branches, "hotfix")
		
		tags_validator(repo)
		sys.exit()

		# update branches after synchronization
		regex_branches=get_all_branch_regexes(repo)

		# support and hotfix validator can only be executed after all the other branches have been synchronized
		all_version_tags=get_all_version_tags()
		check_one_branch_support_max_per_major(regex_branches, all_version_tags)
		version_file_validator(regex_branches, all_version_tags)
		hotfix_history_json_validator(regex_branches)
		validate_release_branch_name(regex_branches, all_version_tags)

		msg.dbg("success", sys._getframe().f_code.co_name)
		return repo, regex_branches, all_version_tags
