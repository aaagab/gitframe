#!/usr/bin/env python3
# author: Gabriel Auger
# version: 11.2.0
# name: gitframe
# license: MIT

__version__= "11.2.0"

from .dev.set_project import set_project
from .dev.update_gitignore import update_gitignore
from .dev.update_branches import update_branches
from .dev.clone import clone_to_directory, clone_to_repository
from .dev.tag import tag
from .dev.update_gitframe_bin import update_gitframe_bin

from .gpkgs.nargs import Nargs
from .gpkgs.bump_version import VersionFile, ManagedFile, IncrementType
