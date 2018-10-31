#!/usr/bin/env python3
import os, sys
if __name__ != "__main__":
    from testing.utils.test_processor import test_processor, set_test_steps, set_test_vars

def test_license(conf):
    set_test_vars(conf, {
        "direpa_test_src": conf["direpa_test_src"],
    })
    
    set_test_steps(conf, """
        cd {direpa_test_src}
        {step} get_license_content mit
        {cmd}
        _out:choice or 'q' to quit:
        _type:1
        _out:Copyright Holders:  [q to quit]:
        _type:Thomas Edison

    """)

    test_processor(conf)

if __name__ == "__main__":
    direpa_script=os.path.realpath(__file__)
    while os.path.basename(direpa_script) != "src":
        direpa_script=os.path.dirname(direpa_script)
    sys.path.insert(0,direpa_script)

    from  git_helpers.license import get_license_content

    if sys.argv[1] == "get_license_content":
        if sys.argv[2] == "mit":
            print(get_license_content())
