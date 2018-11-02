#!/usr/bin/env python3
import os, sys
if __name__ != "__main__":
    from testing.utils.test_processor import test_processor, set_test_steps, set_test_vars

def test_version_file_validator(conf):
    set_test_vars(conf, {
        "direpa_test_src": conf["direpa_test_src"],
    })

    set_test_steps(conf,"""
        cd {direpa_test_src}

        {step} version_file_validator no_master_version_file_value
        git tag v1.0.0
        git checkout -b support-1.0.X
        git checkout -b hotfix-1.0.X-my_repair
        {cmd}
        _out:× Master branch version.txt has a no value whereas:
        _out:× There is at least a release tag 'v1.0.0'
        _out:× At least one support branch is present '[support-1.0.X]'
        _out:× At least one hotfix branch is present '[hotfix-1.0.X-my_repair]'
        _fail:
        git checkout master
        git reset --hard start_master
        git tag --delete v1.0.0
        git branch -D support-1.0.X hotfix-1.0.X-my_repair

        {step} version_file_validator version_file_empty
        git checkout master
        echo 1.0.0 > version.txt
        git add .; git commit -a -m "modified version.txt"
        git tag v1.0.0
        {cmd}
        _out:× 'version.txt' not found on branch 'develop'.
        _fail:
        git checkout master
        git reset --hard start_master
        git tag --delete v1.0.0
        
        {step} version_file_validator version_not_valid
        git checkout master
        echo x1.0.0 > version.txt
        git add .; git commit -a -m "modified version.txt"
        git tag v1.0.0
        git checkout develop
        echo 1.0.0 > version.txt
        git add .; git commit -a -m "modified version.txt"
        {cmd}
        _out:× Version value in version.txt is equal to 'x1.0.0'
        _out:× It should be equal to the form ^\d+\.\d+\.\d+$
        _fail:
        git checkout master
        git reset --hard start_master
        git checkout develop
        git reset --hard start_develop
        git tag --delete v1.0.0

        {step} version_file_validator version_value_not_latest develop
        git checkout master
        echo 1.0.0 > version.txt
        git add .; git commit -a -m "modified version.txt"
        git checkout develop
        echo 1.0.0 > version.txt
        git add .; git commit -a -m "modified version.txt"
        git tag v1.1.0
        {cmd}
        _out:× Value '1.0.0' in version.txt from develop branch is different than latest release tag 'v1.1.0'
        _fail:
        git checkout master
        git reset --hard start_master
        git checkout develop
        git reset --hard start_develop
        git tag --delete v1.1.0

        {step} version_file_validator support
        git checkout master
        echo 1.0.0 > version.txt
        git add .; git commit -a -m "modified version.txt"
        git checkout develop
        echo 1.0.0 > version.txt
        git add .; git commit -a -m "modified version.txt"
        git tag v1.0.0
        git checkout master
        git checkout -b support-0.5.X
        echo 0.5.0 > version.txt
        git add .; git commit -a -m "modified version.txt"
        git tag v0.5.0
        {cmd}
        _out:√ find_related_tag_for_support_branch_name
        _out:√ version_file_validator
        git checkout master
        git reset --hard start_master
        git checkout develop
        git reset --hard start_develop
        git tag --delete v1.0.0
        git tag --delete v0.5.0
        git branch -D support-0.5.X

        {step} version_file_validator hotfix
        git checkout master
        echo 1.0.0 > version.txt
        git add .; git commit -a -m "modified version.txt"
        git checkout develop
        echo 1.0.0 > version.txt
        git add .; git commit -a -m "modified version.txt"
        git tag v1.0.0
        git checkout master
        git checkout -b hotfix-1.0.X-my_repair
        {cmd}
        _out:√ hotfix 'hotfix-1.0.X-my_repair' comes from latest release '1.0.0'
        _out:√ version_file_validator
        git checkout master
        git reset --hard start_master
        git checkout develop
        git reset --hard start_develop
        git tag --delete v1.0.0
        git branch -D hotfix-1.0.X-my_repair

        {step} version_file_validator release
        git checkout master
        echo 1.0.0 > version.txt
        git add .; git commit -a -m "modified version.txt"
        git checkout develop
        echo 1.0.0 > version.txt
        git add .; git commit -a -m "modified version.txt"
        git tag v1.0.0
        git checkout master
        git checkout -b release-1.1.0
        echo 1.1.0 > version.txt
        git add .; git commit -a -m "modified version.txt"
        {cmd}
        _out:√ branch release-1.1.0 name matches with its version.txt 1.1.0
        _out:√ version_file_validator
        git checkout master
        git reset --hard start_master
        git checkout develop
        git reset --hard start_develop
        git tag --delete v1.0.0
        git branch -D release-1.1.0

        {step} version_file_validator no_release_tags empty_master_version_txt
        git checkout master
        echo "" > version.txt
        git add .; git commit -a -m "modified version.txt"
        {cmd}
        _out:× The project has no release tags
        _out:×  Branch 'master' shouldn't have a version.txt file.
        _fail:
        git checkout master
        git reset --hard start_master

        {step} version_file_validator no_release_tags hotfix_branch_not_allowed
        git checkout master
        git checkout -b hotfix-1.0.X-my_repair
        {cmd}
        _out:× The project has no release tags
        _out:×  Branch 'hotfix-1.0.X-my_repair' shouldn't exist.
        _fail:
        git checkout master
        git reset --hard start_master
        git branch -D hotfix-1.0.X-my_repair

        {step} match_branch_name_with_version_value support_false
        {cmd}
        _out:× branch support-1.0.X name does not match with its version.txt 1.1.0
        _fail:

        {step} match_branch_name_with_version_value hotfix_true
        {cmd}
        _out:√ branch hotfix-1.1.X-my_repair name matches with its version.txt 1.1.0

        {step} match_branch_name_with_version_value release_false
        {cmd}
        _out:× branch release-1.2.0 name does not match with its version.txt 1.1.0
        _fail:

        {step} match_branch_name_with_version_value release_true
        {cmd}
        _out:√ branch release-1.1.0 name matches with its version.txt 1.1.0

    """)

    test_processor(conf)

if __name__ == "__main__":
    direpa_script=os.path.realpath(__file__)
    while os.path.basename(direpa_script) != "testing":
        direpa_script=os.path.dirname(direpa_script)
    sys.path.insert(0,os.path.dirname(direpa_script))

    
    if sys.argv[1] == "version_file_validator":
        from git_helpers.validator.version_file import version_file_validator

        from git_helpers.get_all_version_tags import get_all_version_tags
        from git_helpers.get_all_branch_regexes import get_all_branch_regexes
        from git_helpers.remote_repository import Remote_repository
        repo=Remote_repository()
        regex_branches=get_all_branch_regexes(repo)

        version_file_validator(regex_branches, get_all_version_tags())

    elif sys.argv[1] == "match_branch_name_with_version_value":
        from git_helpers.validator.version_file import match_branch_name_with_version_value
        import git_helpers.regex_obj as ro
        
        if sys.argv[2] == "support_false":
            match_branch_name_with_version_value(
                ro.Support_regex("support-1.0.X"), 
                ro.Version_regex("1.1.0")
            )
        elif sys.argv[2] == "hotfix_true":
             match_branch_name_with_version_value(
                ro.Hotfix_regex("hotfix-1.1.X-my_repair"), 
                ro.Version_regex("1.1.0")
            )
        elif sys.argv[2] == "release_false":
             match_branch_name_with_version_value(
                ro.Release_regex("release-1.2.0"), 
                ro.Version_regex("1.1.0")
            )
        elif sys.argv[2] == "release_true":
             match_branch_name_with_version_value(
                ro.Release_regex("release-1.1.0"), 
                ro.Version_regex("1.1.0")
            )
