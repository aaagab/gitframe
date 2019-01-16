#!/usr/bin/env python3
import os, sys
if __name__ != "__main__":
    from processor.utils.processor_engine import start_processor, set_task_steps, set_task_vars

def test_open_draft(conf):
    set_task_vars(conf, {
        "direpa_task_src": conf["direpa_task_src"],
    })
    
    set_task_steps(conf, """
        cd {direpa_task_src}

        {step} open_draft branch_exists_on_local
        git checkout develop
        git checkout -b dft-quick_test
        {cmd}
        _out:Enter Draft Branch Keyword(s) [q to quit]:
        _type:quick test
        _out:× Branch dft-quick_test already exists on local.
        _fail:
        git checkout master
        git branch -D dft-quick_test

        {step} open_draft create_and_push
        git checkout develop
        {cmd}
        _out:Enter Draft Branch Keyword(s) [q to quit]:
        _type:quick test
        _out:√ open_draft
        git checkout master
        git branch -D dft-quick_test
    """)

    start_processor(conf)

if __name__ == "__main__":
    direpa_script=os.path.realpath(__file__)
    while os.path.basename(direpa_script) != "processor":
        direpa_script=os.path.dirname(direpa_script)
    sys.path.insert(0,os.path.dirname(direpa_script))

    from git_helpers.remote_repository import Remote_repository
    from git_helpers.branch.draft import open_draft

    if sys.argv[1] == "open_draft":
        open_draft(Remote_repository())
