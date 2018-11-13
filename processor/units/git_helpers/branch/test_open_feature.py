#!/usr/bin/env python3
import os, sys
if __name__ != "__main__":
    from processor.utils.processor_engine import start_processor, set_task_steps, set_task_vars

def test_open_feature(conf):
    set_task_vars(conf, {
        "direpa_task_src": conf["direpa_task_src"],
    })
    
    set_task_steps(conf, """
        cd {direpa_task_src}

        {step} open_feature branch_exists_on_local
        git checkout develop
        git checkout -b feature-new_function
        {cmd}
        _out:Enter Feature Name [q to quit]:
        _type:new function
        _out:× Branch feature-new_function already exists on local.
        _fail:
        git checkout master
        git branch -D feature-new_function

        {step} open_feature create_and_push
        git checkout develop
        {cmd}
        _out:Enter Feature Name [q to quit]:
        _type:new function
        _out:√ git push origin feature-new_function
        _out:√ open_feature
        git checkout master
        git branch -D feature-new_function
        git push origin --delete feature-new_function
    """)

    start_processor(conf)

if __name__ == "__main__":
    direpa_script=os.path.realpath(__file__)
    while os.path.basename(direpa_script) != "processor":
        direpa_script=os.path.dirname(direpa_script)
    sys.path.insert(0,os.path.dirname(direpa_script))

    from git_helpers.remote_repository import Remote_repository
    from git_helpers.branch.feature import open_feature

    if sys.argv[1] == "open_feature":
        open_feature(Remote_repository())
