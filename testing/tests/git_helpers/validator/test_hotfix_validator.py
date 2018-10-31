#!/usr/bin/env python3
import os, sys
from pprint import pprint

if __name__ != "__main__":
    from testing.utils.test_processor import test_processor, set_test_steps, set_test_vars

def test_hotfix_validator(conf):
    from utils.json_config import Json_config
    hotfix_json=Json_config().get_value("filen_hotfix_history")    
    
    set_test_vars(conf, {
        "direpa_test_src": conf["direpa_test_src"],
        "commit": "git commit --allow-empty -m \"one commit\"",
        "hotfix_json": hotfix_json,
        "clean_tags": 'git tag | grep -Ev "start_develop|start_master" | xargs git tag -d'
    })


    set_test_steps(conf,"""
        cd {direpa_test_src}

        {step} check_hotfix_is_either_on_master_or_on_support no_support_branch
        {cmd}
        _out:× Hotfix branch 'hotfix-1.0.X-repair' does not come from master and no support branches are also present.
        _fail:

        {step} check_hotfix_is_either_on_master_or_on_support not_from_support_not_from_master
        {cmd}
        _out:× Hotfix branch 'hotfix-1.0.X-repair' does not come from a support branch nor from master.
        _fail:

        {step} check_hotfix_is_either_on_master_or_on_support from_support
        {cmd}
        _out:√ hotfix 'hotfix-1.0.X-repair' comes from support branch 'support-1.0.X'

        {step} check_hotfix_is_either_on_master_or_on_support from_latest
        {cmd}
        _out:√ hotfix 'hotfix-3.1.X-repair' comes from latest release '3.1.0'
    """)

    test_processor(conf)

if __name__ == "__main__":
    direpa_script=os.path.realpath(__file__)
    while os.path.basename(direpa_script) != "src":
        direpa_script=os.path.dirname(direpa_script)
    sys.path.insert(0,direpa_script)

    if sys.argv[1] == "check_hotfix_is_either_on_master_or_on_support":
        from git_helpers.validator.hotfix import check_hotfix_is_either_on_master_or_on_support
        import git_helpers.regex_obj as ro

        if sys.argv[2] == "no_support_branch":
            check_hotfix_is_either_on_master_or_on_support(
                ro.Hotfix_regex("hotfix-1.0.X-repair"),
                ['1.0.0', '1.1.0', '1.2.0', '2.0.0', '2.1.0', '3.0.0', '3.1.0'],
                []
            )
        elif sys.argv[2] == "not_from_support_not_from_master":
            check_hotfix_is_either_on_master_or_on_support(
                ro.Hotfix_regex("hotfix-1.0.X-repair"),
                ['1.0.0', '1.1.0', '1.2.0', '2.0.0', '2.1.0', '3.0.0', '3.1.0'],
                [
                    ro.Support_regex('support-1.2.X')
                ]
            )
        elif sys.argv[2] == "from_support":
            check_hotfix_is_either_on_master_or_on_support(
                ro.Hotfix_regex("hotfix-1.0.X-repair"),
                ['1.0.0', '1.1.0', '1.2.0', '2.0.0', '2.1.0', '3.0.0', '3.1.0'],
                [
                    ro.Support_regex('support-1.0.X')
                ]
            )
        elif sys.argv[2] == "from_latest":
            check_hotfix_is_either_on_master_or_on_support(
                ro.Hotfix_regex("hotfix-3.1.X-repair"),
                ['1.0.0', '1.1.0', '1.2.0', '2.0.0', '2.1.0', '3.0.0', '3.1.0'],
                [
                    ro.Support_regex('support-1.2.X')
                ]
            )
            