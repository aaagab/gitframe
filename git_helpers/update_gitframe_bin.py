#!/usr/bin/env python3
from distutils.dir_util import copy_tree
import os
import shutil
import sys

from . import git_utils as git
from . import msg_helpers as msgh

from ..gpkgs import message as msg


def is_direpa_dev_sources(conf, path=""):
	is_direpa_dev_sources=True
	if path:
		if git.is_git_project(path):

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
		if git.is_git_project():
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
				msg.error(
					"Current 'direpa_dev_sources' '{}' does not exists".format(conf.data["direpa_dev_sources"]),
					"Go to real path development sources and run './gitframe.py --update-gitframe' to set direpa_dev_sources."
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

def update_gitframe_bin(conf, parameters=""):

	msgh.subtitle("Update Gitframe Bin")

	direpa_source_app=get_direpa_dev_sources(conf)

	direpa_previous=os.getcwd()

	direpa_bin="/data/bin"
	direpa_source_dst=os.path.join(direpa_bin, "gitframe_data","draft")
	if os.path.exists(direpa_source_dst):
		shutil.rmtree(direpa_source_dst)

	os.makedirs(direpa_source_dst)

	copy_tree(direpa_source_app, direpa_source_dst)
	shutil.rmtree(os.path.join(direpa_source_dst,".git"))
	shutil.rmtree(os.path.join(direpa_source_dst,".env"))
	shutil.rmtree(os.path.join(direpa_source_dst,".pytest_cache"))
	shutil.rmtree(os.path.join(direpa_source_dst,".vscode"))
	filenpa_private_config=os.path.join(direpa_source_dst, "config", "private_config.json")
	if os.path.exists(filenpa_private_config):
		os.remove(filenpa_private_config)

	filenpa_dst_exe=os.path.join(direpa_source_dst, "gitframe.py")
	filepa_gitframe_symlink_dst=os.path.join(direpa_bin, "gitframe")

	if os.path.exists(filepa_gitframe_symlink_dst):
		os.remove(filepa_gitframe_symlink_dst)

	os.symlink(
		filenpa_dst_exe,
		filepa_gitframe_symlink_dst
	)

	if direpa_source_app != direpa_previous:
		os.chdir(direpa_source_app)

	if parameters:
		other_parameters=False
		os.system("{} {}".format(
			"gitframe",
			parameters
		))
