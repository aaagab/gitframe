#!/usr/bin/env python3
# author: Gabriel Auger
# version: 2.0.1
# name: gitframe
# license: MIT

__version__ = "2.0.1"

from .git_helpers import git_utils as git
from .git_helpers import msg_helpers as msgh
from .git_helpers import version as version

from .git_helpers.create_new_release import create_new_release
from .git_helpers.clone_project_to_remote import clone_project_to_remote
from .git_helpers.close_branch import close_branch
from .git_helpers.main_validator import validator
from .git_helpers.new_project import new_project
from .git_helpers.open_branch import open_branch
from .git_helpers.pick_up_release import pick_up_release
from .git_helpers.remote_repository import Remote_repository
from .git_helpers.update_branch import update_branch			
from .git_helpers.update_gitframe_bin import update_gitframe_bin


# from .processor.utils import processor_engine as pe

from .gpkgs import message as msg
from .gpkgs.message import ft

from .utils.install_dependencies import install_dependencies
from .utils.json_config import Json_config
