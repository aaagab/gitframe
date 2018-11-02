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
        "direpa_test": conf["direpa_test"],
        "direpa_testgf": conf["direpa_testgf"],
        "direpa_repository": conf["direpa_repository"],
        "diren_src": conf["diren_src"],
        "block_user_input": """
            _out:Enter user name [q to quit]:
            _type:user_name
            _out:Enter user email [q to quit]:
            _type:test@test.com
            _out:Enter origin repository [q to quit]:
        """  
    })

    set_task_steps(conf, """
        {step} start
        mkdir -p {direpa_test}
        cd {direpa_test}
        git init .
        {cmd}
        {block_user_input}
        _type:{direpa_remote_src}
        _out:# Repository set to '{direpa_remote_src}'

        cd {direpa_testgf}
        rm -rf {direpa_test}
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
