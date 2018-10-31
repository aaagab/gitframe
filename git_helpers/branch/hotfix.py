#!/usr/bin/env python3
import os
import sys
import re

import utils.message as msg
from utils.format_text import Format_text as ft
import utils.shell_helpers as shell

from git_helpers.publish_release import publish_release
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
	filen_hotfix_history=conf.get_value("filen_hotfix_history")
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
	hotfix_objs=Json_config(filen_hotfix_history).data

	git.checkout(curr_branch)

	hotfix_obj=get_hotfix_obj(hotfix_objs)
	
	# this part allows to create an hotfix from an existing hotfix
	if hotfix_obj:
		msg.dbg("subtitle", "Create an Hotfix From an Existing One")
		diff_file_content=get_diff_between_commits(hotfix_obj[next(iter(hotfix_obj))]["start_commit"], hotfix_obj[next(iter(hotfix_obj))]["end_commit"])
		diff_file_name=next(iter(hotfix_obj))+".diff"

	# create a new hotfix
	regex_tag_to_branch_from=ro.Version_regex(tag_to_branch_from)
	
	new_hotfix_branch=""
	while True:
		keywords=prompt("Type Few Keywords For new hotfix branch name")
		new_hotfix_branch=ro.Hotfix_regex().get_new_branch_name(regex_tag_to_branch_from.major_minor, keywords)
		if not is_start_hotfix_tag_exists(new_hotfix_branch):
			break
		else:
			msg.user_error("start-"+new_hotfix_branch+" tag already exists. Change your keywords.")

	hotfix_description=""
	if hotfix_obj:
		hotfix_description=hotfix_obj[next(iter(hotfix_obj))]["description"]
	else:
		hotfix_description=prompt("Add Description For "+new_hotfix_branch)
	
	related_support_branch=ro.Support_regex().get_new_branch_name(regex_tag_to_branch_from.major_minor)

	if git.is_branch_on_local(related_support_branch):
		msg.dbg("info", "hotfix from existing support branch")
		git.checkout(related_support_branch)
		git.set_annotated_tags(repo, "start-"+new_hotfix_branch, "entry-point")
		msg.subtitle("Open Hotfix "+new_hotfix_branch+" from "+related_support_branch)
		git.checkoutb(new_hotfix_branch)
	else:
		latest_release_tag=all_version_tags[-1]
		if tag_to_branch_from == latest_release_tag:
			msg.dbg("info", "hotfix from latest release")
			git.checkout("master")
			git.set_annotated_tags(repo, "start-"+new_hotfix_branch, "entry-point")
			msg.subtitle("Open Hotfix "+new_hotfix_branch+" from tag v"+latest_release_tag)
			git.checkoutb(new_hotfix_branch+" v"+latest_release_tag)
		else:
			# create first a support branch and branch from it the hotfix
			msg.dbg("info", "hotfix from new support branch")
			msg.subtitle("Create branch "+related_support_branch)
			git.checkoutb(related_support_branch+" v"+tag_to_branch_from)
			git.commit_empty("Creating Branch "+related_support_branch)
			git.push_origin(repo, related_support_branch)
			git.set_annotated_tags(repo, "start-"+new_hotfix_branch, "entry-point")
			msg.subtitle("Open Hotfix "+new_hotfix_branch+" from "+related_support_branch)
			git.checkoutb(new_hotfix_branch+" "+related_support_branch)

	if hotfix_obj:
		msg.dbg("subtitle", "Creating diff file "+diff_file_name)
		with open(diff_file_name,"w") as f:
			f.write(diff_file_content+'\n')
	
	git.commit_empty("Creating Branch "+new_hotfix_branch)
	create_json_data_hotfix(new_hotfix_branch, hotfix_description, filen_hotfix_history)

	git.push_origin(repo, new_hotfix_branch)

def get_hotfix_obj(hotfix_objs):
	msg.dbg("subtitle", "Search For Existing And Completed Hotfix")
	if hotfix_objs:
		# At least one hotfix needs to be closed
		closed=False
		selected_hotfix_objs=[]
		for i, obj_id in enumerate(hotfix_objs):
			if hotfix_objs[obj_id]["end_tag"]:
				selected_hotfix_objs.append({
					obj_id : hotfix_objs[obj_id]
				})
				closed=True
		
		if not closed:
			msg.dbg("raw_print", "No hotfixes closed")
			return ""

		if not prompt_boolean("Do you want to Duplicate a previous Hotfix?", "n"):
			return ""
	else:
		return ""

	# sort selected obj
	hotfix_major_minor=[]
	regex_hotfix=ro.Hotfix_regex()
	for i, obj in enumerate(selected_hotfix_objs):
		for obj_id in obj:
			regex_hotfix.set_text_if_tag_match(hotfix_objs[obj_id]["start_tag"])
			hotfix_major_minor.append(regex_hotfix.major_minor)

	sorted_indexes=tag_sort_index(hotfix_major_minor)
	sorted_selected_hotfixs_objs=[]
	for i in range(0, len(selected_hotfix_objs)):
		sorted_selected_hotfixs_objs.append(i)

	for i, value in enumerate(sorted_indexes):
		sorted_selected_hotfixs_objs[i]=selected_hotfix_objs[value]
	
	menu="\n"

	for i, obj in enumerate(sorted_selected_hotfixs_objs):
		for obj_id in obj:
			start=hotfix_objs[obj_id]["start_tag"]
			end=hotfix_objs[obj_id]["end_tag"]
			description=hotfix_objs[obj_id]["description"]
			menu+="    "+str(i+1)+" - "+start+" => "+end+"\n"
			menu+="    \tdescription: "+description+"\n\n"

	menu+="\n"
	menu+="    Choose a Hotfix To Duplicate.\n"
	menu+="    choice or 'q' to quit: "
	
	user_choice=""
	while not user_choice:
		isValid=True
		user_choice = input(menu)
		if user_choice.isdigit():
			if int(user_choice) >= 1 and int(user_choice) <= len(sorted_selected_hotfixs_objs):
				return_obj=sorted_selected_hotfixs_objs[int(user_choice)-1]
				msg.dbg("raw_print", next(iter(return_obj)))
				return return_obj
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

def create_json_data_hotfix(branch_name, hotfix_description, fname):
	hotfix_objs=Json_config(fname).data

	hotfix_objs.update({
		branch_name : {
			"description": hotfix_description,
			"start_tag": "start-"+branch_name,
			"end_tag": "",
			"start_commit": git.get_commit_from_tag("start-"+branch_name),
			"end_commit": ""
		}
	})

	Json_config(fname).set_file_with_data(hotfix_objs)
	git.commit("Adding entry to "+fname+" for "+branch_name)

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

def close_hotfix(repo, regex_branch, regex_branches, all_version_tags):
	conf = Json_config()
	filen_hotfix_history=conf.get_value("filen_hotfix_history")
	msg.subtitle("Close Branch "+regex_branch.text)

	update_branch(all_version_tags, regex_branch)

	latest_release_tag=all_version_tags[-1]
	
	if is_hotfix_on_latest_release(regex_branch, latest_release_tag):
	
		msg.dbg("info", regex_branch.text+" is on latest release")

		# git.checkout("master")
		release_version=version.increment_version_value(
			"patch", 
			ro.Version_regex(latest_release_tag)
		)

		# git.checkout(regex_branch.text)
		version.bump_tag_file(release_version)
		git.set_annotated_tags(repo, "v"+release_version, "hotfix")
		update_json_data_hotfix_on_close(regex_branch.text, filen_hotfix_history, release_version)

		msg.dbg("subtitle", "close "+regex_branch.text+" on master")
		git.checkout("master")
		git.merge_noff(regex_branch.text)
		git.push_origin(repo, "master")
		
		regex_release_branch=get_branch_type_from_location("release", "local", regex_branches)
		if regex_release_branch:
			# close on release
			msg.dbg("subtitle", "close "+regex_branch.text+" on "+regex_release_branch[0].text)
			git.checkout(regex_release_branch[0].text)
			git.merge_noff(regex_branch.text)
			git.push_origin(repo, regex_release_branch[0].text)

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
		support_branch=ro.Support_regex().get_new_branch_name(regex_branch.major_minor)

		msg.dbg("subtitle", "close "+regex_branch.text+" on "+support_branch)
		git.checkout(support_branch)

		release_version=version.increment_version_value(
			"patch", 
			ro.Version_regex(version.get_content_version_file())
		)
		git.checkout(regex_branch.text)
		version.bump_tag_file(release_version)
		git.set_annotated_tags(repo, "v"+release_version, "hotfix")
		update_json_data_hotfix_on_close(regex_branch.text, filen_hotfix_history, release_version)

		git.checkout(support_branch)
		git.merge_noff(regex_branch.text)
		git.push_origin(repo, support_branch)

		git.delete_local_branch(regex_branch.text)
		git.delete_origin_branch(repo, regex_branch.text)

	msg.success(regex_branch.text+" has been closed.")
	publish_release(release_version, get_all_version_tags())

def update_json_data_hotfix_on_close(branch_name, fname, release_version):
	msg.dbg("subtitle", "updating "+fname)
	msg.dbg("info", " for "+branch_name+" with version "+release_version)
	hotfix_objs=Json_config(fname).data	

	obj_found=False
	for index in hotfix_objs:
		if hotfix_objs[index]["start_tag"] == "start-"+branch_name:
			obj_found=True
			hotfix_objs[index]["end_tag"]="v"+release_version
			hotfix_objs[index]["end_commit"]=git.get_commit_from_tag("v"+release_version)
			Json_config(fname).set_file_with_data(hotfix_objs)
			git.commit("Updating "+fname+" for "+branch_name+" with "+release_version)
			break

	msg.dbg("success", sys._getframe().f_code.co_name)
	
def is_hotfix_on_latest_release(regex_hotfix_branch, latest_release_tag):
	regex_latest_release_tag=ro.Version_regex(latest_release_tag)
	if regex_hotfix_branch.major_minor == regex_latest_release_tag.major_minor:
		return True
	else:
		return False

def is_start_hotfix_tag_exists(hotfix_branch_name):
	results=shell.cmd_get_value("git tag")
	start_hotfix_tags=[]
	if results:
		for result in results.split('\n'):
			if "start-"+hotfix_branch_name == result:
				return True
		return False
	else:
		return False

def get_diff_between_commits(start_commit, end_commit):
	all_commits=shell.cmd_get_value("git rev-list --all")

	if not start_commit in all_commits:
		msg.user_error("Start commit: "+start_commit+" does not exist. Can't get diff between two commits.")
		sys.exit(1)

	if not end_commit in all_commits:
		msg.user_error("End commit: "+end_commit+" does not exist. Can't get diff between two commits.")
		sys.exit(1)

	diff_file_content=shell.cmd_get_value("git diff "+start_commit+"..."+end_commit)

	if diff_file_content:
		msg.dbg("success","diff_file has content")
		return diff_file_content
	else:
		msg.user_error(
			"There was no content added between '{}' and '{}'".format(start_commit, end_commit),
			"Diff file content is empty."
			)
		sys.exit(1)
	