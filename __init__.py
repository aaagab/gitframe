#!/usr/bin/env python3
# author: Gabriel Auger
# version: 6.0.2
# name: gitframe
# license: MIT

__version__ = "6.0.2"

from .git_helpers import msg_helpers as msgh
from .git_helpers import version as version

from .git_helpers.close_branch import close_branch
from .git_helpers.main_validator import validator
from .git_helpers.set_project import set_project
from .git_helpers.update_gitignore import update_gitignore
from .git_helpers.clone import clone
from .git_helpers.set_origin import set_origin
from .git_helpers.tag import tag
from .git_helpers.open_branch import open_branch
from .git_helpers.update_branch import update_branch			
from .git_helpers.update_gitframe_bin import update_gitframe_bin

from .gpkgs import message as msg
from .gpkgs.message import ft
from .gpkgs.options import Options
from .gpkgs import shell_helpers as shell

from .utils.install_dependencies import install_dependencies
from .utils.json_config import Json_config
