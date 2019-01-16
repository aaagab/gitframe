#!/usr/bin/env python3
import os, sys
if __name__ != "__main__":
    from processor.utils.processor_engine import start_processor, set_task_steps, set_task_vars

def test_get_all_branch_regexes(conf):
    set_task_vars(conf, {
        "direpa_task_src": conf["direpa_task_src"],
    })
    
    set_task_steps(conf, """
        cd {direpa_task_src}

        {step} get_all_branch_regexes
        git checkout master
        git checkout -b spt-1.X.X
        {cmd}
        _out:remote develop ^develop$
        _out:remote master ^master$
        _out:local develop ^develop$
        _out:local master ^master$
        _out:local spt-1.X.X ^spt-\d+\.X\.X$
        _out:local_remote develop ^develop$
        _out:local_remote master ^master$
        git checkout master
        git branch -D spt-1.X.X
    """)

    start_processor(conf)

if __name__ == "__main__":
    direpa_script=os.path.realpath(__file__)
    while os.path.basename(direpa_script) != "processor":
        direpa_script=os.path.dirname(direpa_script)
    sys.path.insert(0,os.path.dirname(direpa_script))

    if sys.argv[1] == "get_all_branch_regexes":
        from git_helpers.get_all_branch_regexes import get_all_branch_regexes
        from git_helpers.remote_repository import Remote_repository
        for branch_regex in get_all_branch_regexes(Remote_repository()):
            print("{} {} {}".format(branch_regex.location, branch_regex.text, branch_regex.string))

    