#!/usr/bin/env python3
import os, sys
if __name__ != "__main__":
    from testing.utils.test_processor import test_processor, set_test_steps, set_test_vars

def test_create_directory_tree(conf): 
    # from pprint import pprint
    # pprint(conf)
    set_test_vars(conf, {
        "direpa_test_src": conf["direpa_test_src"],
        "direpa_testgf": conf["direpa_testgf"],
        "direpa_test": conf["direpa_test"]
    })

    set_test_steps(conf,"""
        mkdir -p {direpa_test_src}
        cd {direpa_test_src}
        {step} draft
        {cmd}
        _out:√ Path '{direpa_test_src}/brainstorming' created.
        _out:√ Path '{direpa_test_src}/documentation' created.
        _out:√ Path '{direpa_test_src}/scripts' created.
        _out:√ Path '{direpa_test_src}/todo' created.
        _out:√ Path '{direpa_test_src}/src' created.

        cd {direpa_testgf}
        rm -rf {direpa_test}        
    """)

    test_processor(conf)

if __name__ == "__main__":
    direpa_script=os.path.realpath(__file__)
    while os.path.basename(direpa_script) != "testing":
        direpa_script=os.path.dirname(direpa_script)
    sys.path.insert(0,os.path.dirname(direpa_script))

    from utils.create_directory_tree import create_directory_tree

    create_directory_tree()
