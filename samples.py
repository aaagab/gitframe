#!/usr/bin/env python3
import importlib
import json
import os 
import tempfile
from pprint import pprint
import sys

if __name__ == "__main__":
    direpa_script=os.path.dirname(os.path.realpath(__file__))
    direpa_script_parent=os.path.dirname(direpa_script)
    module_name=os.path.basename(direpa_script)
    sys.path.insert(0, direpa_script_parent)
    pkg = importlib.import_module(module_name)
    del sys.path[0]


    filenpa_main=os.path.join(direpa_script, "main.py")

    direpa_project=os.path.join(tempfile.gettempdir(), "gitframe")
    if os.path.exists(direpa_project):
        pkg._shell.rmtree(direpa_project)
    os.makedirs(direpa_project)
    direpa_repository=os.path.join(direpa_project, "repo")
    direpa_repository_git=os.path.join(direpa_project, "repo", "src.git")
    os.makedirs(direpa_repository)
    direpa_src=os.path.join(direpa_project, "src")
    os.makedirs(direpa_src)
    direpa_mgt=os.path.join(direpa_project, "mgt")
    os.makedirs(direpa_mgt)

    open(os.path.join(direpa_src, "todo.txt"), "w").close()
    open(os.path.join(direpa_src, "settings.json"), "w").close()
    with open(os.path.join(direpa_src, ".gitignore"), "w") as f:
        f.write(f"settings.json\n")

    with open(os.path.join(direpa_src, "gpm.json"), "w") as f:
        f.write(json.dumps(dict(version="1.0.0")))

    pkg_name="dummy"
    uuid4="3a47bbee931440f996da25166e8652fc"
    username="john.doe"
    email="john.doe@email.com"
    
    pkg._shell.cmd_prompt([
        filenpa_main,
        "--set-project",
        direpa_src,
        "--username",
        username,
        "--email",
        email,
        "--init",
        "--shared",
        "group",
        "--branches",
        "dev",
    ])

    pkg._shell.cmd_prompt([
        filenpa_main,
        "--clone",
        direpa_src,
        "--to-directory",
        direpa_repository,
        "--package",
        "dummy",
        "--diren-git",
        "test",
        "--remote",
        "origin"
    ])

    pkg._shell.cmd_prompt([
        filenpa_main,
        "--clone",
        direpa_src,
        "--to-repository",
        direpa_repository,
        "--package",
        "dummy",
        "--uuid4",
        uuid4,
        "--remote",
        "origin"
    ])

    pkg._shell.cmd_prompt([
        filenpa_main,
        "--update",
        "--branches",
        direpa_src,
        "--msg",
        "edit",
    ])

    pkg._shell.cmd_prompt([
        filenpa_main,
        "--update",
        "--gitignore",
        direpa_src,
    ])

    pkg._shell.cmd_prompt([
        filenpa_main,
        "--tag",
        "--path-src",
        direpa_src,
        "--file",
        "gpm.json",
        "--increment",
        "patch",
        "--msg",
        "edit",
        "--pull",
    ])

    pkg._shell.cmd_prompt([
        filenpa_main,
        "--set-project",
        direpa_mgt,
        "--username",
        username,
        "--email",
        email,
        "--init",
    ])

    pkg._shell.cmd_prompt([
        filenpa_main,
        "--clone",
        direpa_mgt,
        "--to-repository",
        direpa_repository,
        "--package",
        "dummy",
        "--uuid4",
        uuid4,
    ])

    pkg._shell.cmd_prompt([
        filenpa_main,
        "--update",
        "--branches",
        direpa_mgt,
        "--msg",
        "edit",
    ])

    open(os.path.join(direpa_mgt, "todo.txt"), "w").close()

    pkg._shell.cmd_prompt([
        filenpa_main,
        "--update",
        "--mgt",
        direpa_src,
        "--msg",
        "edit",
    ])

    open(os.path.join(direpa_mgt, "update.txt"), "w").close()

    pkg._shell.cmd_prompt([
        filenpa_main,
        "--update",
        "--mgt",
        direpa_project,
        "--msg",
        "edit",
    ])


    # pkg._shell.cmd_prompt([
    #     filenpa_main,
    #     "--update",
    #     "--gitframe",
    # ])
