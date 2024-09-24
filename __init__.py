#!/usr/bin/env python3
# author: Gabriel Auger
# version: 12.1.0
# name: gitframe
# license: MIT

__version__= "12.1.0"

from .dev.set_eol import set_eol, LineEnding
from .dev.set_project import set_project
from .dev.update_gitignore import update_gitignore
from .dev.update_branches import update_branches
from .dev.clone import clone_to_directory, clone_to_repository
from .dev.tag import tag
from .dev.update_gitframe_bin import update_gitframe_bin
from .dev.update_mgt import update_mgt

from .gpkgs.gitlib import GitLib as _GitLib
from .gpkgs import shell_helpers as _shell

from .gpkgs.nargs import Nargs
from .gpkgs.bump_version import VersionFile, ManagedFile, IncrementType
