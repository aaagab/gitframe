#!/usr/bin/env python3
import os, sys
from pprint import pprint

if __name__ != "__main__":
    from processor.utils.processor_engine import start_processor, set_task_steps, set_task_vars

def test_check_master_develop_exists(conf):
    set_task_vars(conf, {
        "direpa_test_src": conf["direpa_test_src"],
        "diren_src": conf["diren_src"],
    })

    set_task_steps(conf,"""
        cd {direpa_test_src}

        {step} check_master_develop_exists
        cp -r {direpa_test_src} {direpa_test_src}_tmp
        cd {direpa_test_src}_tmp        
        git checkout master
        git branch -D develop
        {cmd}
        _out:× Branch "develop" does not exist as a local branch.
        _fail:
        rm -rf {direpa_test_src}_tmp

    """)

    start_processor(conf)

if __name__ == "__main__":
    direpa_script=os.path.realpath(__file__)
    while os.path.basename(direpa_script) != "processor":
        direpa_script=os.path.dirname(direpa_script)
    sys.path.insert(0,os.path.dirname(direpa_script))

    from git_helpers.get_all_branch_regexes import get_all_branch_regexes
    from git_helpers.remote_repository import Remote_repository
    from git_helpers.validator.check_master_develop_exists import check_master_develop_exists

    regex_branches=get_all_branch_regexes(Remote_repository())
    check_master_develop_exists(regex_branches)
        