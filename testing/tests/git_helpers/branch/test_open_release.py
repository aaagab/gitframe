#!/usr/bin/env python3
import os, sys
if __name__ != "__main__":
    from testing.utils.test_processor import test_processor, set_test_steps, set_test_vars

def test_open_release(conf):
    set_test_vars(conf, {
        "direpa_test_src": conf["direpa_test_src"],
    })

    set_test_steps(conf,"""
        cd {direpa_test_src}

        {step} open_release no_tag
        {cmd}
        _out:√ git checkout -b release-1.0.0
        _out:√ open_release
        git checkout master
        git branch -D release-1.0.0

        {step} open_release tag_exists
        git checkout master
        echo 1.2.0 > version.txt
        git add .; git commit -a -m "new version"
        {cmd}
        _out:Choose an increment type for tag '1.2.0' or 'q' to quit:
        _type:2
        _out:√ git checkout -b release-1.3.0
        _out:√ git push origin release-1.3.0
        git checkout master
        git reset --hard start_master
        git branch -D release-1.3.0
        git push origin --delete release-1.3.0

        {step} open_release release_branch_exists
        git checkout master
        git checkout -b release-1.0.0
        {cmd}
        _out:× Close the following release branch 'release-1.0.0' and retry the operation.
        _fail:
        git checkout master
        git reset --hard start_master
        git branch -D release-1.0.0

    """)
    
    test_processor(conf)

if __name__ == "__main__":
    direpa_script=os.path.realpath(__file__)
    while os.path.basename(direpa_script) != "testing":
        direpa_script=os.path.dirname(direpa_script)
    sys.path.insert(0,os.path.dirname(direpa_script))

    if sys.argv[1] == "open_release":
        from git_helpers.branch.release import open_release

        from git_helpers.get_all_branch_regexes import get_all_branch_regexes
        from git_helpers.remote_repository import Remote_repository
        repo=Remote_repository()
        regex_branches=get_all_branch_regexes(repo)
        
        open_release(Remote_repository(), regex_branches)

        

