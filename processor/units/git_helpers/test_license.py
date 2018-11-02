#!/usr/bin/env python3
import os, sys
if __name__ != "__main__":
    from processor.utils.processor_engine import start_processor, set_task_steps, set_task_vars

def test_license(conf):
    set_task_vars(conf, {
        "direpa_test_src": conf["direpa_test_src"],
    })
    
    set_task_steps(conf, """
        cd {direpa_test_src}
        {step} get_license_content mit
        {cmd}
        _out:choice or 'q' to quit:
        _type:1
        _out:Copyright Holders:  [q to quit]:
        _type:Thomas Edison

    """)

    start_processor(conf)

if __name__ == "__main__":
    direpa_script=os.path.realpath(__file__)
    while os.path.basename(direpa_script) != "processor":
        direpa_script=os.path.dirname(direpa_script)
    sys.path.insert(0,os.path.dirname(direpa_script))

    from  git_helpers.license import get_license_content

    if sys.argv[1] == "get_license_content":
        if sys.argv[2] == "mit":
            print(get_license_content())
