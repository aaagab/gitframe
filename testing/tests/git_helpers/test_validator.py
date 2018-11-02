#!/usr/bin/env python3
import os, sys
if __name__ != "__main__":
    from testing.utils.test_processor import test_processor, set_test_steps, set_test_vars

def test_validator(conf):
    set_test_vars(conf, {
        "direpa_test_src": conf["direpa_test_src"],
    })

    set_test_steps(conf,"""
        cd {direpa_test_src}

        {step} validator
        {cmd}
        _out:√ validator
    """)

    test_processor(conf)

if __name__ == "__main__":
    direpa_script=os.path.realpath(__file__)
    while os.path.basename(direpa_script) != "testing":
        direpa_script=os.path.dirname(direpa_script)
    sys.path.insert(0,os.path.dirname(direpa_script))

    from git_helpers.main_validator import validator

    print(validator(True))
        