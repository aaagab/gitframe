#!/usr/bin/env python3
import os, sys
if __name__ != "__main__":
    from processor.utils.processor_engine import start_processor, set_task_steps, set_task_vars

def test_synchronize_branch_name(conf):
    set_task_vars(conf, {
        "direpa_task_src": conf["direpa_task_src"],
    })
    
    set_task_steps(conf, """
        cd {direpa_task_src}

        {step} regex_branches local
        git checkout master
        git checkout -b feature-add
        {cmd}
        _out:# True_False_False
        _out:# cmp_status: push
        _out:choice or 'q' to quit:
        _type: 2
        git checkout master
        git branch -D feature-add

        {step} regex_branches all_location
        git checkout master
        git checkout -b feature-add
        git push origin feature-add
        {cmd}
        _out:# True_True_True
        _out:# cmp_status: up_to_date
        _out:√ No action needed for 'synchronize' with "feature-add" on "remote"
        git checkout master
        git branch -D feature-add
        git push origin --delete feature-add

        {step} remote_x_local_remote_and_local
        git checkout -b feature-add
        git tag start_test
        git push origin feature-add
        {cmd}
        _out:# True_True_True
        _out:### synchronize_local_with 'remote' for 'feature-add'
        _out:# cmp_status: up_to_date
        _out:√ No action needed for 'synchronize' with "feature-add" on "remote"
        git checkout master
        git branch -D feature-add


        {step} remote_x_local_remote_and_not_local
        git checkout master
        git checkout -b feature-add
        git push origin feature-add
        git checkout master
        git branch -D feature-add
        {cmd}
        _out:# False_True_True
        _out:∆ Branch 'feature-add' is on local_remote but not on local. No need to checkout.
        _out:### synchronize_local_with 'remote' for 'feature-add'
        _out:# cmp_status: pull_not_local
        git push origin --delete feature-add
    
        {step} remote_x_not_local_remote_and_local
        git checkout master
        git checkout -b feature-add
        git push origin feature-add
        git branch -rd origin/feature-add
        {cmd}
        _out:# True_False_True
        _out:∆ Branch exists on local and on remote but not on local_remote.
        _fail:
        git checkout master
        git push origin --delete feature-add
        git branch -D feature-add
    
        {step} remote_x_not_local_remote_and_not_local
        git checkout master
        git checkout -b feature-add
        git push origin feature-add
        git checkout master
        git branch -rd origin/feature-add
        git branch -D feature-add
        {cmd}
        _out:# False_False_True
        _out:### synchronize_local_with 'remote' for 'feature-add'
        _out:# cmp_status: pull_not_local
        _out:choice or 'q' to quit:
        _type:2
        git push origin --delete feature-add
    
        {step} no_remote_x_online_local_remote_and_local_not_master_x_delete_local_and_local_remote
        git checkout master
        git checkout -b feature-add
        git push origin feature-add
        cp -r {direpa_task_src} {direpa_task_src}_tmp
        cd {direpa_task_src}_tmp
        git push origin --delete feature-add
        cd {direpa_task_src}
        {cmd}
        _out:# True_True_False 
        _out:# Git Pretty 'feature-add'
        _out:Do you want to delete 'feature-add' from local? [y/N/q]:
        _type:n
        _out:# Git Pretty 'origin/feature-add'
        _out:Do you want to delete 'feature-add' from local_remote? [y/N/q]:
        _type:n
        _out:### synchronize_local_with 'remote' for 'feature-add'
        _out:choice or 'q' to quit:
        _type:2
        rm -rf {direpa_task_src}_tmp
        git checkout master
        git branch -rd origin/feature-add
        git branch -D feature-add
    
        {step} no_remote_x_online_local_remote_and_not_local_not_master_x_delete_local_remote
        git checkout master
        git checkout -b feature-add
        git push origin feature-add
        cp -r {direpa_task_src} {direpa_task_src}_tmp
        cd {direpa_task_src}_tmp
        git push origin --delete feature-add
        cd {direpa_task_src}
        rm -rf {direpa_task_src}_tmp
        git checkout master
        git branch -D feature-add
        {cmd}
        _out:# False_True_False 
        _out:# Git Pretty 'origin/feature-add'
        _out:Do you want to delete 'feature-add' from local_remote? [y/N/q]:
        _type:n
        _out:### get_branch_compare_status_repository 'local_remote' for 'feature-add'
        _out:# cmp_status: pull_not_local
        _out:∆ Branch 'feature-add' is on local_remote but not on local. No need to checkout.
        _out:### get_branch_compare_status_repository 'remote' for 'feature-add'
        _out:### synchronize_local_with 'remote' for 'feature-add'
        _out:# cmp_status: null
        _out:∆ Branch 'feature-add' does not exist on local nor on remote.
        git checkout master
        git branch -rd origin/feature-add
        
        {step} no_remote_x_online_not_local_remote_and_local
        git checkout master
        git checkout -b feature-add
        {cmd}
        _out:# True_False_False
        _out:### get_branch_compare_status_repository 'remote' for 'feature-add'
        _out:### synchronize_local_with 'remote' for 'feature-add'
        _out:# cmp_status: push
        _out:choice or 'q' to quit:
        _type:2
        git checkout master
        git branch -D feature-add
    
        {step} no_remote_x_online_not_local_remote_and_not_local
        git checkout develop
        {cmd}
        _out:# False_False_False
        _out:∆ Branch does not exists on local, local_remote and remote.
        _out:∆ No action needed for 'synchronize' on 'feature-add'
    
        {step} no_remote_x_offline_local_remote_and_local
        git checkout master
        git checkout -b feature-add
        git push origin feature-add
        cp -r {direpa_task_src} {direpa_task_src}_tmp
        cd {direpa_task_src}_tmp
        git push origin --delete feature-add
        cd {direpa_task_src}
        rm -rf {direpa_task_src}_tmp        
        {cmd}
        _out:# True_True_False
        _out:### get_branch_compare_status_repository 'local_remote' for 'feature-add'
        _out:### synchronize_local_with 'local_remote' for 'feature-add'
        _out:# cmp_status: up_to_date
        git checkout master
        git branch -rd origin/feature-add
        git branch -D feature-add
    
        {step} no_remote_x_offline_local_remote_and_not_local
        git checkout master
        git checkout -b feature-add
        git push origin feature-add
        cp -r {direpa_task_src} {direpa_task_src}_tmp
        cd {direpa_task_src}_tmp
        git push origin --delete feature-add
        cd {direpa_task_src}
        rm -rf {direpa_task_src}_tmp        
        git checkout master
        git branch -D feature-add
        {cmd}
        _out:# False_True_False
        _out:∆ Remote is not reachable thus it is not possible to compare local branch with remote branch.
        _out:### get_branch_compare_status_repository 'local_remote' for 'feature-add'
        _out:### synchronize_local_with 'local_remote' for 'feature-add'
        _out:# cmp_status: pull_not_local
        _out:∆ Branch 'feature-add' is on local_remote but not on local. No need to checkout.
        git checkout master
        git branch -rd origin/feature-add
        
        {step} no_remote_x_offline_not_local_remote_and_local
        git checkout master
        git checkout -b feature-add
        {cmd}
        _out:# True_False_False
        _out:∆ Branch only exists on local and remote is not reachable.
        git checkout master
        git branch -D feature-add
    
        {step} no_remote_x_offline_not_local_remote_and_not_local
        {cmd}
        _out:# False_False_False
        _out:∆ Branch does not exists on local, local_remote and remote can't be verified due to offline mode.
    """)
    
    start_processor(conf)
    

if __name__ == "__main__":
    direpa_script=os.path.realpath(__file__)
    while os.path.basename(direpa_script) != "processor":
        direpa_script=os.path.dirname(direpa_script)
    sys.path.insert(0,os.path.dirname(direpa_script))

    from git_helpers.synchronize_branch_name import synchronize_branch_name
    from git_helpers.remote_repository import Remote_repository

    repo=Remote_repository()

    from git_helpers.get_all_branch_regexes import get_all_branch_regexes
    regex_branches=get_all_branch_regexes(repo)

    if sys.argv[1] == "regex_branches":
        synchronize_branch_name(repo, regex_branches, "feature-add")

    elif sys.argv[1] == "remote_x_local_remote_and_local":
        synchronize_branch_name(repo, regex_branches, "feature-add")

    elif sys.argv[1] == "remote_x_local_remote_and_not_local":
        synchronize_branch_name(repo, regex_branches, "feature-add")

    elif sys.argv[1] == "remote_x_not_local_remote_and_local":
        synchronize_branch_name(repo, regex_branches, "feature-add")

    elif sys.argv[1] == "remote_x_not_local_remote_and_not_local":
        synchronize_branch_name(repo, regex_branches, "feature-add")

    elif sys.argv[1] == "no_remote_x_online_local_remote_and_local_not_master_x_delete_local_and_local_remote":
        synchronize_branch_name(repo, regex_branches, "feature-add")

    elif sys.argv[1] == "no_remote_x_online_local_remote_and_not_local_not_master_x_delete_local_remote":
        synchronize_branch_name(repo, regex_branches, "feature-add")

    elif sys.argv[1] == "no_remote_x_online_not_local_remote_and_local":
        synchronize_branch_name(repo, regex_branches, "feature-add")

    elif sys.argv[1] == "no_remote_x_online_not_local_remote_and_not_local":
        synchronize_branch_name(repo, regex_branches, "feature-add")

    repo.is_reachable=False

    if sys.argv[1] == "no_remote_x_offline_local_remote_and_local":
        synchronize_branch_name(repo, regex_branches, "feature-add")

    elif sys.argv[1] == "no_remote_x_offline_local_remote_and_not_local":
        synchronize_branch_name(repo, regex_branches, "feature-add")

    elif sys.argv[1] == "no_remote_x_offline_not_local_remote_and_local":
        synchronize_branch_name(repo, regex_branches, "feature-add")

    elif sys.argv[1] == "no_remote_x_offline_not_local_remote_and_not_local":
        synchronize_branch_name(repo, regex_branches, "feature-add")



