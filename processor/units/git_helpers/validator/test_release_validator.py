#!/usr/bin/env python3
import os, sys
if __name__ != "__main__":
    from processor.utils.processor_engine import start_processor, set_task_steps, set_task_vars

def test_release_validator(conf):
    set_task_vars(conf, {
        "direpa_task_src": conf["direpa_task_src"],
    })

    set_task_steps(conf,"""
        cd {direpa_task_src}

        {step} force_unique_release_branch_name two_releases_on_local
        {info} Failing Command due to 2 releases on local
        git checkout master
        git checkout -b release-1.0.0
        git checkout -b release-1.2.0
        {cmd} 
        _out:× There are more than one release branch on local ['release-1.0.0', 'release-1.2.0'], please delete one.
        _fail:
        git checkout master
        git branch -D release-1.0.0 release-1.2.0

        {step} force_unique_release_branch_name two_releases_on_remote
        {info} Failing Command due to 2 releases on remote
        git checkout master
        git checkout -b release-1.0.0
        git checkout -b release-1.2.0
        git push origin release-1.0.0 release-1.2.0
        git checkout master
        git branch -D release-1.0.0 release-1.2.0
        {cmd} 
        _out:× There are more than one release branch on remote ['release-1.0.0', 'release-1.2.0'], please delete one
        _fail:
        git push origin --delete release-1.0.0 release-1.2.0

        {step} force_unique_release_branch_name different_name_on_release_and_on_local
        {info} Failing Command due to different name on release and on local
        git checkout master
        git checkout -b release-1.2.0
        git push origin release-1.2.0
        git checkout -b release-1.0.0
        git branch -D release-1.2.0
        {cmd} 
        _out:× local release branch name 'release-1.0.0' and remote release branch name 'release-1.2.0' are different.
        _fail:
        git checkout master
        git branch -D release-1.0.0
        git push origin --delete release-1.2.0

        {step} force_unique_release_branch_name success
        {cmd} 
        _out:√ force_unique_release_branch_name

        {step} validate_release_branch_name release1_1_0
        {info} Failure Release Patch Number should be 0
        git checkout master
        git checkout -b release-1.2.0
        {cmd}
        _out:× Tags are not present and release branch version '1.2.0' is different than '0.1.0' or '1.0.0'
        _fail:
        git checkout master
        git branch -D release-1.2.0

        {step} validate_release_branch_name minor_num_1
        {info} Failure release minor should be 1
        git checkout master
        git tag v1.0.0
        git checkout -b release-1.0.0
        {cmd} 
        _out:× Minor number on release tag branch name should be '1' not '0'
        _fail:
        git checkout master
        git branch -D release-1.0.0
        git tag --delete v1.0.0
        
        {step} validate_release_branch_name major_num_2
        {info} Failure release major should be 2
        git checkout master
        git tag v1.0.0
        git checkout -b release-3.0.0
        {cmd} 
        _out:× Major number on release tag branch name should be '2' not '3'
        _fail:
        git checkout master
        git tag --delete v1.0.0
        git branch -D release-3.0.0

        {step} validate_release_branch_name major_num_2_ok
        {info} Success release major should be 2
        git checkout master
        git tag v1.0.0
        git checkout -b release-2.0.0
        {cmd} 
        # _out:√ validate_release_branch_name
        git checkout master
        git tag --delete v1.0.0
        git branch -D release-2.0.0

    """)

    start_processor(conf)

if __name__ == "__main__":
    direpa_script=os.path.realpath(__file__)
    while os.path.basename(direpa_script) != "processor":
        direpa_script=os.path.dirname(direpa_script)
    sys.path.insert(0,os.path.dirname(direpa_script))

    from git_helpers.get_all_branch_regexes import get_all_branch_regexes
    from git_helpers.remote_repository import Remote_repository
    from git_helpers.get_all_version_tags import get_all_version_tags
    

    regex_branches=get_all_branch_regexes(Remote_repository())
    
    if sys.argv[1] == "force_unique_release_branch_name":
        
        from git_helpers.validator.release import force_unique_release_branch_name
        
        force_unique_release_branch_name(regex_branches)

    elif sys.argv[1] == "validate_release_branch_name":
        from git_helpers.validator.release import validate_release_branch_name
        if sys.argv[2] == "release1_1_0":
            validate_release_branch_name(
                regex_branches,
                get_all_version_tags()    
            )
        elif sys.argv[2] == "minor_num_1":
            validate_release_branch_name(
                regex_branches,
                get_all_version_tags()            
            )
        elif sys.argv[2] == "major_num_2":
            validate_release_branch_name(
                regex_branches,
                get_all_version_tags()            
            )
        elif sys.argv[2] == "major_num_2_ok":
            validate_release_branch_name(
                regex_branches,
                get_all_version_tags()            
            )




