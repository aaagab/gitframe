#!/usr/bin/env python3
import os, sys
if __name__ != "__main__":
    from testing.utils.test_processor import test_processor, set_test_steps, set_test_vars

def test_open_support(conf):
    set_test_vars(conf, {
        "direpa_test_src": conf["direpa_test_src"],
    })
    
    set_test_steps(conf, """
        cd {direpa_test_src}

        {step} open_support no_tags
        {cmd}
        _out:× There are no version tags in this project. You can't open a Support Branch
        _fail:

        {step} open_support no_tag_to_branch_from
        git tag v1.0.3
        {cmd}
        _out:× There are no Tags from where to start a support branch. You need to have at least 2 releases before you can create a support branch.
        _fail:
        git tag --delete v1.0.3

        {step} open_support success
        git tag v1.0.3
        git tag v2.0.0
        {cmd}
        _out:Choose a release From Where To branch The Support Branch.
        _out:choice or 'q' to quit:
        _type:1
        _out:√ git checkout -b support-1.0.X v1.0.3
        _out:√ git push origin support-1.0.X
        git tag --delete v1.0.3
        git tag --delete v2.0.0
        git checkout develop
        git branch -D support-1.0.X
        git push origin --delete support-1.0.X

        {step} get_tag_for_support
        {cmd}
        _out:Choose a release From Where To branch The Support Branch.
        _out:choice or 'q' to quit: 
        _type:1
        _out:1.0.1

        {step} has_tag_a_support_branch True
        {cmd}
        _out:True

        {step} has_tag_a_support_branch False
        {cmd}
        _out:False
    """)

    test_processor(conf)

if __name__ == "__main__":
    direpa_script=os.path.realpath(__file__)
    while os.path.basename(direpa_script) != "src":
        direpa_script=os.path.dirname(direpa_script)
    sys.path.insert(0,direpa_script)

    if sys.argv[1] == "open_support":
        from git_helpers.remote_repository import Remote_repository
        from git_helpers.branch.support import open_support

        from git_helpers.get_all_branch_regexes import get_all_branch_regexes
        from git_helpers.remote_repository import Remote_repository
        from git_helpers.get_all_version_tags import get_all_version_tags
        repo=Remote_repository()
        regex_branches=get_all_branch_regexes(repo)
                
        open_support(
            repo,
            regex_branches,
            get_all_version_tags()            
        )

    elif sys.argv[1] == "get_tag_for_support":
        from git_helpers.branch.support import get_tag_for_support
        import git_helpers.regex_obj as ro
        print(get_tag_for_support(
            ['1.0.0', '1.0.1', '2.0.0', '2.0.3', '3.0.0', '3.1.0'],
            [
                ro.Support_regex("support-2.0.X")
            ]
        ))
    elif sys.argv[1] == "has_tag_a_support_branch":
        from git_helpers.branch.support import has_tag_a_support_branch
        import git_helpers.regex_obj as ro
        if sys.argv[2] == "True":
            print(has_tag_a_support_branch(
                "1.2.1",
                [
                    ro.Support_regex("support-1.2.X"),
                    ro.Support_regex("support-2.1.X")
                ]
            ))
        elif sys.argv[2] == "False":
            print(has_tag_a_support_branch(
                "1.2.1",
                [
                    ro.Support_regex("support-2.1.X")
                ]
            ))
        