#!/usr/bin/env python3
import json
from pprint import pprint
import os
import shutil
import sys

from . import git_utils as git
from . import msg_helpers as msgh

from ..gpkgs import message as msg


def is_direpa_dev_sources(conf, path=""):
	if git.is_git_project(path):
		filenpa_gpm=os.path.join(git.get_root_dir_path(path), "gpm.json")
		if os.path.exists(filenpa_gpm):
			with open(filenpa_gpm, "r") as f:
				data=json.load(f)
				if data["name"] == "gitframe":
					return True
	return False

def get_direpa_dev_sources(conf):
	if is_direpa_dev_sources(conf):
		if conf.data["direpa_dev_sources"] != os.getcwd():
			conf.set_value("direpa_dev_sources", os.getcwd())
	else:
		if conf.data["direpa_dev_sources"]:
			if not os.path.exists(conf.data["direpa_dev_sources"]):
				msg.error(
					"Current 'direpa_dev_sources' '{}' does not exists".format(conf.data["direpa_dev_sources"]),
					"Go to real path development sources and run './main.py --update-gitframe' to set direpa_dev_sources."
				)
				sys.exit(1)
			else:
				if not is_direpa_dev_sources(conf, conf.data["direpa_dev_sources"]):
					msg.error(
						"Current 'direpa_dev_sources' '{}' exists but it is not the real path development sources for gitframe.".format(conf.data["direpa_dev_sources"]),
						"Go to real path development sources and run './gitframe.py --update-gitframe' to set direpa_dev_sources."
					)
					sys.exit(1)
		else:
			msg.error(
				"'direpa_dev_sources' has not been defined",
				"Go to real path development sources and run './gitframe.py --update-gitframe' to set direpa_dev_sources."
			)
			sys.exit(1)

	return conf.data["direpa_dev_sources"]

def update_gitframe_bin(conf, parameters=None):
	msg.info("Update Gitframe Bin")
	# input(os.getcwd())


	direpa_source_app=get_direpa_dev_sources(conf)
	# print("direpa_source", direpa_source_app)

	direpa_previous=os.getcwd()
	# print("direpa_previous", direpa_previous)


	direpa_bin="{}/fty/bin".format(os.path.expanduser("~"))
	direpa_source_dst=os.path.join(direpa_bin, "gitframe_data","beta")
	if os.path.exists(direpa_source_dst):
		shutil.rmtree(direpa_source_dst)

	os.makedirs(direpa_source_dst)

	shutil.copy_tree(direpa_source_app, direpa_source_dst)
	shutil.rmtree(os.path.join(direpa_source_dst,".git"))
	shutil.rmtree(os.path.join(direpa_source_dst,".env"))
	shutil.rmtree(os.path.join(direpa_source_dst,".pytest_cache"))
	shutil.rmtree(os.path.join(direpa_source_dst,".vscode"))
	filenpa_private_config=os.path.join(direpa_source_dst, "config", "private_config.json")
	if os.path.exists(filenpa_private_config):
		os.remove(filenpa_private_config)

	filenpa_dst_exe=os.path.join(direpa_source_dst, "main.py")
	filepa_gitframe_symlink_dst=os.path.join(direpa_bin, "gitframe")

	if os.path.exists(filepa_gitframe_symlink_dst):
		os.remove(filepa_gitframe_symlink_dst)
	
	os.symlink(
		filenpa_dst_exe,
		filepa_gitframe_symlink_dst
	)


	# if direpa_source_app != direpa_previous:
		# os.chdir(direpa_previous)

	if parameters:
		other_parameters=False
		os.system("pwd; {} {}".format(
			"gitframe",
			parameters
		))
