#!/usr/bin/env python3
import json
import os
import shutil
import sys

from ..gpkgs import message as msg
from ..gpkgs.gitlib import GitLib
from ..gpkgs import shell_helpers as shell

def is_direpa_dev_sources(path=""):
	git=GitLib(direpa=path)
	if git.is_direpa_git(path):
		filenpa_gpm=os.path.join(git.direpa_root, "gpm.json")
		if os.path.exists(filenpa_gpm):
			with open(filenpa_gpm, "r") as f:
				data=json.load(f)
				if data["name"] == "gitframe":
					return True
	return False

def get_direpa_dev_sources():
	direpa_dev_sources=os.path.join(os.path.expanduser("~"), "fty", "wrk", "g", "gitframe", "78d3adc7fdd546c4ba2630d987237a51", "src")
	if is_direpa_dev_sources() is False:
		if direpa_dev_sources:
			if not os.path.exists(direpa_dev_sources):
				msg.error(
					"Current 'direpa_dev_sources' '{}' does not exists".format(direpa_dev_sources),
					"Go to real path development sources and run './main.py --update --gitframe' to set direpa_dev_sources."
				)
				sys.exit(1)
			else:
				if not is_direpa_dev_sources(direpa_dev_sources):
					msg.error(
						"Current 'direpa_dev_sources' '{}' exists but it is not the real path development sources for gitframe.".format(direpa_dev_sources),
						"Go to real path development sources and run './main.py --update --gitframe' to set direpa_dev_sources."
					)
					sys.exit(1)
		else:
			msg.error(
				"'direpa_dev_sources' has not been defined",
				"Go to real path development sources and run './main.py --update --gitframe' to set direpa_dev_sources."
			)
			sys.exit(1)

	return direpa_dev_sources

def update_gitframe_bin():
	direpa_source_app=get_direpa_dev_sources()
	direpa_bin="{}/fty/bin".format(os.path.expanduser("~"))
	direpa_source_dst=os.path.join(direpa_bin, "gitframe_data", "78d3adc7fdd546c4ba2630d987237a51", "beta")
	if os.path.exists(direpa_source_dst):
		shell.rmtree(direpa_source_dst)

	shutil.copytree(direpa_source_app, direpa_source_dst)
	shutil.rmtree(os.path.join(direpa_source_dst,".git"))

	filenpa_dst_exe=os.path.join(direpa_source_dst, "main.py")
	filepa_gitframe_symlink_dst=os.path.join(direpa_bin, "gitframe")

	if os.path.exists(filepa_gitframe_symlink_dst):
		os.remove(filepa_gitframe_symlink_dst)
	
	os.symlink(
		filenpa_dst_exe,
		filepa_gitframe_symlink_dst
	)
