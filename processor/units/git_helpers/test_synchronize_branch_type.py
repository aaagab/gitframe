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

        {step} synchronize_branch_type support_no_branches
        {cmd}
        _out:√ synchronize_branch_type

        {step} synchronize_branch_type support_branch_local
        git checkout master
        git checkout -b spt-2.X.X
        {cmd}
        _out:Choose an action for branch 'spt-2.X.X'.
        _out:choice or 'q' to quit:
        _type:2
        _out:∆ Operation ignored 'synchronize' branch 'spt-2.X.X'        
        _out:√ synchronize_branch_type
        git checkout master
        git branch -D spt-2.X.X

        {step} get_unique_regex_branch_names
        git checkout master
        git checkout -b hfx-1.X.X-a_quick_repair
        git push origin hfx-1.X.X-a_quick_repair
        git branch -rD origin/hfx-1.X.X-a_quick_repair
        git checkout -b fts-super_function
        git push origin fts-super_function
        git checkout -b spt-1.X.X
        git push origin spt-1.X.X
        git checkout master
        git branch -D fts-super_function
        git branch -D spt-1.X.X
        cp -r {direpa_task_src} {direpa_task_src}_tmp
        cd {direpa_task_src}_tmp
        git push origin --delete spt-1.X.X
        cd {direpa_task_src}
        {cmd}
        _out:develop
        _out:fts-super_function
        _out:hfx-1.X.X-a_quick_repair
        _out:master
        _out:spt-1.X.X
        git checkout master
        rm -rf {direpa_task_src}_tmp
        git branch -D hfx-1.X.X-a_quick_repair
        git push origin --delete hfx-1.X.X-a_quick_repair
        git push origin --delete fts-super_function
        git branch -rD origin/spt-1.X.X
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
        synchronize_branch_type(repo, regex_branches, "support")
    
    elif sys.argv[1] == "get_unique_regex_branch_names":
        from git_helpers.synchronize_branch_type import get_unique_regex_branch_names

        for br in get_unique_regex_branch_names(regex_branches):
            print(br.text)
    
