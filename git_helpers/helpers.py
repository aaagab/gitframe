#!/usr/bin/env python3
import os
import re
import sys

from ..gpkgs import message as msg

def get_path(path_elem, exit_not_found=True):
    if not os.path.isabs(path_elem):
        path_elem=os.path.abspath(path_elem)
    path_elem=os.path.normpath(path_elem)
    if exit_not_found is True:
        if not os.path.exists(path_elem):
            msg.error("Path not found '{}'".format(path_elem), exit=1)
    return path_elem