#!/usr/bin/env python3
from enum import Enum
import os
import sys

from ..gpkgs.gitlib import GitLib, SwitchDir
from ..gpkgs import shell_helpers as shell

class LineEnding(bytes, Enum):
    CRLF=b'\r\n'
    LF=b'\n'

def set_eol(
    ending:LineEnding,
    direpa_project:str|None=None,
    isglobal:bool=False,
    parse:bool=False,
):
    git=GitLib(direpa=direpa_project)

    if git.direpa_root is None:
        raise Exception(f"Not a git directory '{direpa_project}'")
    
    filenpa_attributes=os.path.join(git.direpa_root, ".gitattributes")
    if os.path.exists(filenpa_attributes) is False:
        with open(filenpa_attributes, "w") as f:
            f.write(f"* text=auto{ending.value.decode()}")

    if ending == LineEnding.LF:
        cmd=["git", "config"]
        if isglobal is True:
            cmd.append("--global")
        if sys.platform == "win32":
            cmd.extend(["core.autocrlf", "false"])
        elif sys.platform == "linux":
            cmd.extend(["core.autocrlf", "input"])
        git.cmd(cmd)
    elif ending == LineEnding.CRLF:
        cmd=["git", "config"]
        if isglobal is True:
            cmd.append("--global")
        cmd.extend(["core.autocrlf", "true"])
        git.cmd(cmd)

    cmd=["git", "config"]
    if isglobal is True:
        cmd.append("--global")
    cmd.extend(["core.eol", ending.name.lower()])
    git.cmd(cmd)

    if parse is True:
        with SwitchDir(gitlib=git):
            output=shell.cmd_get_value("git ls-files")
            if output is None:
                raise Exception(f"No files found at '{git.direpa_root}'")
            for filen in output.splitlines():
                filenpa_tmp=os.path.normpath(os.path.join(git.direpa_root, filen))
                print(filenpa_tmp)
                content:bytes
                with open(filenpa_tmp, "rb") as f:
                    content=f.read()
                if ending == LineEnding.LF:
                    content=content.replace(LineEnding.CRLF.value, LineEnding.LF.value)
                elif ending == LineEnding.CRLF:
                    content=content.replace(LineEnding.LF.value, LineEnding.CRLF.value)
                with open(filenpa_tmp, "wb") as f:
                    f.write(content)
                