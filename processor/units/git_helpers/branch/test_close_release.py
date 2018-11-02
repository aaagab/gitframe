#!/usr/bin/env python3
import os, sys
if __name__ != "__main__":
    from processor.utils.processor_engine import start_processor, set_task_steps, set_task_vars

def test_close_release(conf):
    set_task_vars(conf, {
        "direpa_test_src": conf["direpa_test_src"],
    })

    set_task_steps(conf,"""
        cd {direpa_test_src}

        {step} close_release latest_release_has_hotfix
        git checkout master
        echo 2.0.0 > "version.txt"
        git add .; git commit -a -m "version changed"
        git tag v2.0.0
        git checkout -b hotfix-2.0.X-repair
        git checkout master
        git checkout -b release-2.1.0
        {cmd}
        _out:× An hotfix is already present on latest release, you must close the hotfix before you can close the release branch 'release-2.1.0'
        _fail:
        git checkout master
        git reset --hard start_master
        git branch -D hotfix-2.0.X-repair
        git branch -D release-2.1.0
        git tag --delete v2.0.0
        
        {step} close_release success
        git checkout master
        echo 2.0.0 > "version.txt"
        git add .; git commit -a -m "version changed"
        git tag v2.0.0
        git checkout -b release-2.1.0
        {cmd}
        _out:All developpers involved in the project should approve this action. Do you want to Continue? [Y/n/q]:
        _type:Y
        _out:release-2.1.0 has to be deleted on local and remote.
        _out:Continue? [Y/n/q]:
        _type:Y
        _fail:
        git checkout master
        git reset --hard start_master
        git push origin -f master
        git tag --delete v2.0.0

        {step} has_latest_release_an_hotfix
        {cmd}
        _out:True
        _out:False
        _out:False

    """)
    
    start_processor(conf)

if __name__ == "__main__":
    direpa_script=os.path.realpath(__file__)
    while os.path.basename(direpa_script) != "processor":
        direpa_script=os.path.dirname(direpa_script)
    sys.path.insert(0,os.path.dirname(direpa_script))
    import git_helpers.regex_obj as ro

    if sys.argv[1] == "close_release":
        from git_helpers.branch.release import close_release
        from git_helpers.get_all_branch_regexes import get_all_branch_regexes
        from git_helpers.remote_repository import Remote_repository
        from git_helpers.get_all_version_tags import get_all_version_tags
        repo=Remote_repository()
        regex_branches=get_all_branch_regexes(repo)
        
        close_release(
            repo, 
            ro.Release_regex("release-2.1.0"), 
            regex_branches, 
            get_all_version_tags())

    if sys.argv[1] == "has_latest_release_an_hotfix":
        from git_helpers.branch.release import has_latest_release_an_hotfix
        print(has_latest_release_an_hotfix(['2.0.0'], [ro.Hotfix_regex('hotfix-2.0.X-repair')]))
        print(has_latest_release_an_hotfix(['3.0.0'], [ro.Hotfix_regex('hotfix-2.0.X-repair')]))
        print(has_latest_release_an_hotfix(['2.0.0'], []))
