#!/usr/bin/env python3
import os, sys
if __name__ != "__main__":
    from processor.utils.processor_engine import start_processor, set_task_steps, set_task_vars

def test_create_directory_tree(conf): 
    from pprint import pprint
    # pprint(conf)
    set_task_vars(conf, {
        "direpa_task_src": conf["direpa_task_src"],
        "direpa_task_conf": conf["direpa_task_conf"],
        "direpa_task": conf["direpa_task"],
        "user_git": conf["remote"]["user_git"]
    })

    set_task_steps(conf,"""
        mkdir -p {direpa_task_src}
        cd {direpa_task_src}
        {step} draft
        {cmd}
        _out:√ Path '{direpa_task_src}/src' created.
        _out:√ Path '{direpa_task_src}/doc' created.
        _out:√ Path '{direpa_task_src}/mgt' created.
        _out:√ Path '{direpa_task_src}/rel' created.
        _out:√ Path '{direpa_task_src}/mgt/{user_git}' created.
        _out:√ File '{direpa_task_src}/mgt/{user_git}/deploy.py' created.
        _out:√ File '{direpa_task_src}/mgt/{user_git}/bump_version.py' created.
        _out:√ File '{direpa_task_src}/mgt/{user_git}/todo.txt' created.
        _out:√ Symlink '{direpa_task_src}/deploy.py' created.
        _out:√ Symlink '{direpa_task_src}/bump_version.py' created.

        cd {direpa_task_conf}
        rm -rf {direpa_task}        
    """)

    start_processor(conf)

if __name__ == "__main__":
    direpa_script=os.path.realpath(__file__)
    while os.path.basename(direpa_script) != "processor":
        direpa_script=os.path.dirname(direpa_script)
    sys.path.insert(0,os.path.dirname(direpa_script))

    from utils.create_directory_tree import create_directory_tree
    from utils.json_config import Json_config

    from pprint import pprint
    # pprint(Json_config().data)
    user_git=Json_config().data["processor"]["task"]["remote"]["user_git"]
    create_directory_tree(user_git)
