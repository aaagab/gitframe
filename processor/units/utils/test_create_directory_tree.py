#!/usr/bin/env python3
import os, sys
if __name__ != "__main__":
    from processor.utils.processor_engine import start_processor, set_task_steps, set_task_vars

def test_create_directory_tree(conf): 
    # from pprint import pprint
    # pprint(conf)
    set_task_vars(conf, {
        "direpa_task_src": conf["direpa_task_src"],
        "direpa_task_conf": conf["direpa_task_conf"],
        "direpa_task": conf["direpa_task"]
    })

    set_task_steps(conf,"""
        mkdir -p {direpa_task_src}
        cd {direpa_task_src}
        {step} draft
        {cmd}
        _out:√ Path '{direpa_task_src}/brainstorming' created.
        _out:√ Path '{direpa_task_src}/documentation' created.
        _out:√ Path '{direpa_task_src}/scripts' created.
        _out:√ Path '{direpa_task_src}/todo' created.
        _out:√ Path '{direpa_task_src}/src' created.

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

    create_directory_tree()
