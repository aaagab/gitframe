#!/usr/bin/env python3
import os, sys
if __name__ != "__main__":
    from processor.utils.processor_engine import start_processor, set_task_steps, set_task_vars

def test_synchronize_branch_type(conf):
    set_task_vars(conf, {
        "direpa_task_src": conf["direpa_task_src"],
    })
    
    set_task_steps(conf, """
        cd {direpa_task_src}

        {step} synchronize_branch_type release_no_branches
        {cmd}
        _out:√ synchronize_branch_type

        {step} synchronize_branch_type release_branche_local
        git checkout master
        git checkout -b release-2.0.0
        {cmd}
        _out:Choose an action for branch 'release-2.0.0'.
        _out:choice or 'q' to quit:
        _type:2
        _out:∆ Operation ignored 'synchronize' branch 'release-2.0.0'        
        _out:√ synchronize_branch_type
        git checkout master
        git branch -D release-2.0.0

        {step} get_unique_regex_branch_names
        git checkout master
        git checkout -b release-2.0.0
        git push origin release-2.0.0
        git checkout -b hotfix-1.0.X-a_quick_repair
        git push origin hotfix-1.0.X-a_quick_repair
        git branch -rD origin/hotfix-1.0.X-a_quick_repair
        git checkout -b feature-super_function
        git push origin feature-super_function
        git checkout -b support-1.0.X
        git push origin support-1.0.X
        git checkout master
        git branch -D feature-super_function
        git branch -D support-1.0.X
        cp -r {direpa_task_src} {direpa_task_src}_tmp
        cd {direpa_task_src}_tmp
        git push origin --delete support-1.0.X
        cd {direpa_task_src}
        {cmd}
        _out:develop
        _out:feature-super_function
        _out:hotfix-1.0.X-a_quick_repair
        _out:master
        _out:release-2.0.0
        _out:support-1.0.X
        git checkout master
        rm -rf {direpa_task_src}_tmp
        git branch -D release-2.0.0
        git push origin --delete release-2.0.0
        git branch -D hotfix-1.0.X-a_quick_repair
        git push origin --delete hotfix-1.0.X-a_quick_repair
        git push origin --delete feature-super_function
        git branch -rD origin/support-1.0.X
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
        
    if sys.argv[1] == "synchronize_branch_type":
        from git_helpers.synchronize_branch_type import synchronize_branch_type
        synchronize_branch_type(repo, regex_branches, "release")
    
    elif sys.argv[1] == "get_unique_regex_branch_names":
        from git_helpers.synchronize_branch_type import get_unique_regex_branch_names

        for br in get_unique_regex_branch_names(regex_branches):
            print(br.text)
    
