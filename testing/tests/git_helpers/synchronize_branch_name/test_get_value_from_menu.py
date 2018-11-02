#!/usr/bin/env python3
import os, sys
if __name__ != "__main__":
    from testing.utils.test_processor import test_processor, set_test_steps, set_test_vars

def test_get_value_from_menu(conf):
    set_test_steps(conf,"""
        {step} get_value_from_menu     
        {cmd}
        _out:choice or 'q' to quit:
        _type:1
        _out:merge
        _out:choice or 'q' to quit:
        _type:2
        _out:ignore
        _out:choice or 'q' to quit:
        _type:3
        _out:exit
        _out:choice or 'q' to quit:
        _type:4
        _out:× Wrong input
        _type:y
        _type:q
        _fail:Quit Menu
    """)

    test_processor(conf)

if __name__ == "__main__":
    direpa_script=os.path.realpath(__file__)
    while os.path.basename(direpa_script) != "testing":
        direpa_script=os.path.dirname(direpa_script)
    sys.path.insert(0,os.path.dirname(direpa_script))

    from git_helpers.synchronize_branch_name import get_value_from_menu

    if sys.argv[1] == "get_value_from_menu":
        print(get_value_from_menu(["merge", "ignore", "exit"],"master"))
        print(get_value_from_menu(["merge", "ignore", "exit"],"master"))
        print(get_value_from_menu(["merge", "ignore", "exit"],"master"))
        print(get_value_from_menu(["merge", "ignore", "exit"],"master"))
   