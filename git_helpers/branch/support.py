#!/usr/bin/env python3

import os
import re
import sys

from .. import git_utils as git
from .. import msg_helpers as msgh
from .. import regex_obj as ro
from ..get_all_branch_regexes import get_branch_type_from_location

from ...gpkgs import message as msg

from ...gpkgs.format_text import ft

def open_support(repo, regex_branches, all_version_tags):
	msgh.subtitle("Open Support Branch")

	if not all_version_tags:
		msg.error("There are no version tags in this project. You can't open a Support Branch")
		sys.exit(1)

	regex_support_branches=get_branch_type_from_location("support", "local", regex_branches)

	tag_to_branch_from=get_tag_for_support(all_version_tags, regex_support_branches)

	if not tag_to_branch_from:
		msg.error("There are no Tags from where to start a support branch. You need to have at least 2 releases before you can create a support branch.")
		sys.exit(1)
	else:
		tag_regex=ro.Version_regex(tag_to_branch_from)
		new_support_branch=ro.Support_regex().get_new_branch_name(tag_regex.major)
		git.checkoutb(new_support_branch+" v"+tag_regex.text)
		git.commit_empty("Creating Branch "+new_support_branch)
		git.push_origin(repo, new_support_branch)

def has_tag_a_support_branch(tag_to_branch, regex_support_branches):
	msg.dbg("info","Search a support branch for tag "+tag_to_branch)

	regex_tag_to_branch=ro.Version_regex(tag_to_branch)
	if regex_support_branches:
		for regex_branch in regex_support_branches:
			if regex_branch.major == regex_tag_to_branch.major:
				return True
		return False
	else:
		return False

def get_tag_for_support(all_version_tags, regex_support_branches):
	# all tag except the latest release for support
	latest_release_tags=git.get_latest_release_for_each_major(all_version_tags)[:-1]

	latest_release_available=[]
	for latest_release_tag in latest_release_tags:
		if not has_tag_a_support_branch(latest_release_tag, regex_support_branches):
			latest_release_available.append(latest_release_tag)

	if not latest_release_tags:
		return ""
	else:
		menu="\n"

		for i, latest_release in enumerate(latest_release_available):
			menu+="    "+str(i+1)+" => "+latest_release+"\n"

		menu+="\n"
		menu+="    Choose a release From Where To branch The Support Branch.\n"
		menu+="    If The release tag you are looking for is not present, it is because it is\n"
		menu+="    either the latest release or a support branch already exists for this tag.\n"
		menu+="    choice or 'q' to quit: "
		
		user_choice=""
		while not user_choice:
			isValid=True
			user_choice = input(menu)
			if user_choice.isdigit():
				if int(user_choice) >= 1 and int(user_choice) <= len(latest_release_available):
					return latest_release_available[int(user_choice)-1]
				else:
					isValid=False
			elif user_choice.lower() == "q":
				sys.exit(1)
			else:
				isValid=False

			if not isValid:
				msg.warning("Wrong input")
				input("  Press Enter To Continue...")
				user_choice=""
				# clear terminal 
				ft.clear_screen()
	
	