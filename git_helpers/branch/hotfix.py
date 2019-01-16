#!/usr/bin/env python3
import os
import sys
import re

import utils.message as msg
from utils.format_text import Format_text as ft
import utils.shell_helpers as shell

from git_helpers.pick_up_release import pick_up_release
import git_helpers.git_utils as git
import git_helpers.version as version
from git_helpers.get_all_version_tags import get_all_version_tags, tag_sort_index
from git_helpers.get_all_branch_regexes import get_branch_type_from_location
from utils.json_config import Json_config
from utils.prompt import prompt, prompt_boolean
from pprint import pprint
import git_helpers.regex_obj as ro

from git_helpers.update_branch import update_branch

def open_hotfix(repo, all_version_tags):
	conf = Json_config()
	msg.subtitle("Open Hotfix Branch")

	if not all_version_tags:
		msg.user_error(
			"There are no tags in this project. You can't open a Hotfix Branch",
			"You need to have published at least 1 release before you can create a hotfix branch."
		)
		sys.exit(1)
	
	tag_to_branch_from=get_tag_for_hotfix(all_version_tags)

	curr_branch=git.get_active_branch_name()
	git.checkout("master")

	git.checkout(curr_branch)

	# create a new hotfix
	regex_tag_to_branch_from=ro.Version_regex(tag_to_branch_from)
	
	new_hotfix_branch=""
	while True:
		keywords=prompt("Type Few Keywords For new hotfix branch name")
		new_hotfix_branch=ro.Hotfix_regex().get_new_branch_name(regex_tag_to_branch_from.major, keywords)

		if git.is_branch_on_local(new_hotfix_branch):
			msg.user_error(
				"Branch "+new_hotfix_branch+" already exists on local.",
				"Please git checkout -b "+new_hotfix_branch+" or choose a new branch name."    
			)
		else:
			break

	related_support_branch=ro.Support_regex().get_new_branch_name(regex_tag_to_branch_from.major)

	if git.is_branch_on_local(related_support_branch):
		msg.dbg("info", "hotfix from existing support branch")
		git.checkout(related_support_branch)
		msg.subtitle("Open Hotfix "+new_hotfix_branch+" from "+related_support_branch)
		git.checkoutb(new_hotfix_branch)
	else:
		latest_release_tag=all_version_tags[-1]
		if tag_to_branch_from == latest_release_tag:
			msg.dbg("info", "hotfix from latest release")
			git.checkout("master")
			msg.subtitle("Open Hotfix "+new_hotfix_branch+" from tag v"+latest_release_tag)
			git.checkoutb(new_hotfix_branch+" v"+latest_release_tag)
		else:
			# create first a support branch and branch from it the hotfix
			msg.dbg("info", "hotfix from new support branch")
			msg.subtitle("Create branch "+related_support_branch)
			git.checkoutb(related_support_branch+" v"+tag_to_branch_from)
			git.commit_empty("Creating Branch "+related_support_branch)
			git.push_origin(repo, related_support_branch)
			msg.subtitle("Open Hotfix "+new_hotfix_branch+" from "+related_support_branch)
			git.checkoutb(new_hotfix_branch+" "+related_support_branch)

	git.commit_empty("Creating Branch "+new_hotfix_branch)

	git.push_origin(repo, new_hotfix_branch)

def get_tag_for_hotfix(all_version_tags):
	latest_release_tags=git.get_latest_release_for_each_major(all_version_tags)
	
	menu="\n"

	for i, latest_release in enumerate(latest_release_tags):
		menu+="    "+str(i+1)+" => "+latest_release+"\n"

	menu+="\n"
	menu+="    Choose a release From Where To branch The Hotfix.\n"
	menu+="    choice or 'q' to quit: "
	
	user_choice=""
	while not user_choice:
		isValid=True
		user_choice = input(menu)
		if user_choice.isdigit():
			if int(user_choice) >= 1 and int(user_choice) <= len(latest_release_tags):
				return latest_release_tags[int(user_choice)-1]
			else:
				isValid=False
		elif user_choice.lower() == "q":
			sys.exit(1)
		else:
			isValid=False

		if not isValid:
			msg.user_error("Wrong input")
			input("  Press Enter To Continue...")
			user_choice=""
			# clear terminal 
			ft.clear_screen()

def close_hotfix(repo, regex_branch, regex_branches, all_version_tags, deploy_args=[]):
	conf = Json_config()
	msg.subtitle("Close Branch "+regex_branch.text)

	update_branch(all_version_tags, regex_branch)

	latest_release_tag=all_version_tags[-1]
	
	if is_hotfix_on_latest_release(regex_branch, latest_release_tag):

		msg.dbg("info", regex_branch.text+" is on latest release")

		release_version=version.increment_version_value(
			"patch", 
			ro.Version_regex(latest_release_tag)
		)

		print()
		if prompt_boolean("Is this a recommended release version"):
			release_version=release_version+"-r"

		version.bump_version_for_user(release_version)
		git.set_annotated_tags(repo, "v"+release_version, "hotfix")

		msg.dbg("subtitle", "close "+regex_branch.text+" on master")
		git.checkout("master")
		git.merge_noff(regex_branch.text)
		git.push_origin(repo, "master")
		
		# close on develop
		msg.dbg("subtitle", "close "+regex_branch.text+" on develop")
		git.checkout("develop")
		git.merge_noff(regex_branch.text)
		git.push_origin(repo, "develop")

		git.delete_local_branch(regex_branch.text)
		git.delete_origin_branch(repo, regex_branch.text)

	else: # hotfix is on a support branch
		msg.dbg("subtitle", "Hotfix is not on the latest release")
		msg.dbg("subtitle", "Check for a related support branch")
		
		support_branch=ro.Support_regex().get_new_branch_name(regex_branch.major)

		msg.dbg("subtitle", "close "+regex_branch.text+" on "+support_branch)
		git.checkout(support_branch)

		latest_release_tags=git.get_latest_release_for_each_major(all_version_tags)

		latest_release_tag_spt=""
		for tag in latest_release_tags:
			reg_version=ro.Version_regex(tag)
			if regex_branch.major == reg_version.major:
				latest_release_tag_spt=reg_version.major_minor_patch
				break

		release_version=version.increment_version_value(
			"patch", 
			ro.Version_regex(latest_release_tag_spt)
		)

		release_version=release_version+"-r"
		
		git.checkout(regex_branch.text)
		version.bump_version_for_user(release_version)
		git.set_annotated_tags(repo, "v"+release_version, "hotfix")

		git.checkout(support_branch)
		git.merge_noff(regex_branch.text)
		git.push_origin(repo, support_branch)

		git.delete_local_branch(regex_branch.text)
		git.delete_origin_branch(repo, regex_branch.text)

	msg.success(regex_branch.text+" has been closed.")
	pick_up_release(release_version, deploy_args)

	msg.dbg("success", sys._getframe().f_code.co_name)
	
def is_hotfix_on_latest_release(regex_hotfix_branch, latest_release_tag):
	regex_latest_release_tag=ro.Version_regex(latest_release_tag)
	if regex_hotfix_branch.major == regex_latest_release_tag.major:
		return True
	else:
		return False