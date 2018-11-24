#!/usr/bin/env python3
import os, sys
if __name__ != "__main__":
    from processor.utils.processor_engine import start_processor, set_task_steps, set_task_vars
    import utils.shell_helpers as shell
    import re

def test_init_local_config(conf):
    # from pprint import pprint
    # pprint(conf)
    set_task_vars(conf, {
        "direpa_remote_src": conf["remote"]["direpa_src"],
        "direpa_task": conf["direpa_task"],
        "direpa_task_conf": conf["direpa_task_conf"],
        "direpa_repository": conf["direpa_repository"],
        "user_git": conf["remote"]["user_git"],
        "diren_src": conf["diren_src"],
        "block_user_input": """
            _out:Enter git user name [q to quit]:
            _type:{user_git}
            _out:Enter git user email [q to quit]:
            _type:test@test.com
            _out:Enter origin repository [q to quit]:
        """  
    })

    set_task_steps(conf, """
        {step} start
        mkdir -p {direpa_task}
        cd {direpa_task}
        git init .
        {cmd}
        {block_user_input}
        _type:{direpa_remote_src}
        _out:# Repository set to '{direpa_remote_src}'

        cd {direpa_task_conf}
        rm -rf {direpa_task}
        rm -rf {direpa_repository}
    """)

    start_processor(conf)

if __name__ == "__main__":
    direpa_script=os.path.realpath(__file__)
    while os.path.basename(direpa_script) != "processor":
        direpa_script=os.path.dirname(direpa_script)
    sys.path.insert(0,os.path.dirname(direpa_script))

    from git_helpers.init_local_config import init_local_config

    init_local_config()
