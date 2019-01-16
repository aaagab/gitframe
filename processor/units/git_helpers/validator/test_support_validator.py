#!/usr/bin/env python3
import os, sys
if __name__ != "__main__":
    from processor.utils.processor_engine import start_processor, set_task_steps, set_task_vars

def test_support_validator(conf):
    set_task_vars(conf, {
        "direpa_task_src": conf["direpa_task_src"],
    })

    set_task_steps(conf,"""
        cd {direpa_task_src}

        {step} find_related_tag_for_support_branch_name notfound
        {info} support version not found in tags
        {cmd}
        _out:× Support Branch name 'spt-0.X.X' does not contain tag from one of the latest releases '1.2.0, 2.1.0, 3.1.0' that matches its Major Number
        _fail:

        {step} find_related_tag_for_support_branch_name found_error
        {info} support branch on latest release
        {cmd}
        _out:× Support branch name major 'spt-3.X.X' can't be equal to Latest release Major from '3.1.0'
        _fail:

        {step} find_related_tag_for_support_branch_name found_success
        {cmd}
        _out:√ find_related_tag_for_support_branch_name

    """)

    start_processor(conf)

if __name__ == "__main__":
    direpa_script=os.path.realpath(__file__)
    while os.path.basename(direpa_script) != "processor":
        direpa_script=os.path.dirname(direpa_script)
    sys.path.insert(0,os.path.dirname(direpa_script))

    from git_helpers.get_all_branch_regexes import get_all_branch_regexes
    from git_helpers.remote_repository import Remote_repository
    repo=Remote_repository()
    regex_branches=get_all_branch_regexes(repo)

    if sys.argv[1] == "find_related_tag_for_support_branch_name":
        from git_helpers.validator.support import find_related_tag_for_support_branch_name
        import git_helpers.regex_obj as ro
        if sys.argv[2] == "notfound":
            find_related_tag_for_support_branch_name(
                ro.Support_regex("spt-0.X.X"),
                ['1.0.0', '1.1.0', '1.2.0', '2.0.0', '2.1.0', '3.0.0', '3.1.0']
            )
        elif sys.argv[2] == "found_error":
            find_related_tag_for_support_branch_name(
                ro.Support_regex("spt-3.X.X"),
                ['1.0.0', '1.1.0', '1.2.0', '2.0.0', '2.1.0', '3.0.0', '3.1.0']
            )  
            
        elif sys.argv[2] == "found_success":
            find_related_tag_for_support_branch_name(
                ro.Support_regex("spt-2.X.X"),
                ['1.0.0', '1.1.0', '1.2.0', '2.0.0', '2.1.0', '3.0.0', '3.1.0']
            )
        