#!/usr/bin/env python3
import os, sys
if __name__ != "__main__":
    from processor.utils.processor_engine import start_processor, set_task_steps, set_task_vars

def test_version(conf):
    # from pprint import pprint
    # pprint(conf)
    set_task_vars(conf, {
        "direpa_task_src": conf["direpa_task_src"],
    })

    set_task_steps(conf,"""
        cd {direpa_task_src}

        {step} increment_version_value major_minor_patch
        {cmd}
        _out:4.0.0
        _out:3.3.0
        _out:3.2.2

        {step} execute_bump_release_version
        {cmd}
        _out:3.2.1

    """)

    start_processor(conf)

if __name__ == "__main__":
    direpa_script=os.path.realpath(__file__)
    while os.path.basename(direpa_script) != "processor":
        direpa_script=os.path.dirname(direpa_script)
    sys.path.insert(0,os.path.dirname(direpa_script))

    if sys.argv[1] == "increment_version_value":
        from git_helpers.version import increment_version_value
        import git_helpers.regex_obj as ro
        print(increment_version_value("major", ro.Version_regex("3.2.1")))
        print(increment_version_value("minor", ro.Version_regex("3.2.1")))
        print(increment_version_value("patch", ro.Version_regex("3.2.1")))
    elif sys.argv[1] == "execute_bump_release_version":
        from git_helpers.version import bump_version_for_user
        bump_version_for_user("3.2.1")
    