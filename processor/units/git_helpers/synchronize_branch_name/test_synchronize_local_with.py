#!/usr/bin/env python3
import os, sys
if __name__ != "__main__":
    from processor.utils.processor_engine import start_processor, set_task_steps, set_task_vars

def test_synchronize_local_with(conf):
    set_task_vars(conf, {
        "direpa_task_src": conf["direpa_task_src"],
        "commit": "git commit --allow-empty -m"        
    })

    set_task_steps(conf, """
        {step} cd
        cd {direpa_task_src}
    
        {step} up_to_date
        {cmd}
        _out:# cmp_status: up_to_date
        _out:√ No action needed for 'synchronize' with "master" on "remote"
    
        {step} pull_synchronize_local_remote
        git checkout -b fts-add
        git tag start_feature
        {commit} "1"
        git push origin fts-add
        git reset --hard start_feature
        {cmd}
        _out:# cmp_status: pull
        _out:choice or 'q' to quit:
        _type:2
        git checkout master
        git branch -D fts-add
        git push origin --delete fts-add
        git tag --delete start_feature
    
        {step} pull_synchronize_remote
        git checkout -b fts-add
        git tag start_feature
        {commit} "1"
        git push origin fts-add
        git reset --hard start_feature
        {cmd}
        _out:# cmp_status: pull
        _out:choice or 'q' to quit:
        _type:2
        git checkout master
        git branch -D fts-add
        git push origin --delete fts-add
        git tag --delete start_feature
        
        {step} pull_not_local_synchronize_local_remote_test
        git checkout master
        git checkout -b fts-add
        git push origin fts-add
        git checkout master
        git branch -D fts-add
        {cmd}
        _out:# cmp_status: pull_not_local
        _out:√ No action needed for 'synchronize' with "fts-add" on "local_remote"
        git push origin --delete fts-add

        {step} pull_not_local_synchronize_remote
        git checkout master
        git checkout -b fts-add
        git push origin fts-add
        git checkout master
        git branch -D fts-add
        {cmd}
        _out:# cmp_status: pull_not_local
        _out:√ No action needed for 'synchronize' with "fts-add" on "remote"
        git push origin --delete fts-add
    
        {step} pull_not_local_synchronize_remote not_branch
        cp -r {direpa_task_src} {direpa_task_src}_tmp
        cd {direpa_task_src}_tmp
        git checkout -b fts-add
        git push origin fts-add
        cd {direpa_task_src}
        {cmd}
        _out:# cmp_status: pull_not_local
        _out:choice or 'q' to quit:
        _type:2
        git push origin --delete fts-add
        rm -rf {direpa_task_src}_tmp

        {step} push_synchronize_local_remote
        git checkout -b fts-add
        {commit} "2"
        {cmd}
        _out:# cmp_status: push
        _out:∆ Push is never done to local_remote branches, local is already the newest
        git checkout master
        git branch -D fts-add
    
        {step} push_synchronize_remote
        git checkout -b fts-add
        git push origin fts-add
        {commit} "1"
        {cmd}
        _out:# cmp_status: push
        _out:choice or 'q' to quit:
        _type:2
        git checkout master
        git branch -D fts-add
        git push origin --delete fts-add

        {step} divergent_with_common_ancestor
        git checkout -b fts-add
        cp -r {direpa_task_src} {direpa_task_src}_tmp
        cd {direpa_task_src}_tmp
        {commit} "1"
        git push origin fts-add
        cd {direpa_task_src}
        {commit} "2"
        {cmd}
        _out:# cmp_status: divergent_with_common_ancestor
        _out:√ divergent_with_common_ancestor
        _fail:Normal Exit for divergent_with_common_ancestor
        git checkout master
        git branch -D fts-add
        git push origin --delete fts-add
        rm -rf {direpa_task_src}_tmp
       
        {step} divergent_without_common_ancestor
        cp -r {direpa_task_src} {direpa_task_src}_tmp
        git checkout --orphan fts-add
        {commit} "1"
        cd {direpa_task_src}_tmp
        git checkout -b fts-add
        git push origin fts-add
        cd {direpa_task_src}
        {cmd}
        _out:# cmp_status: divergent_without_common_ancestor
        _out:√ divergent_without_common_ancestor
        _fail:Normal Exit for divergent_without_common_ancestor
        git checkout master
        git branch -D fts-add
        git push origin --delete fts-add
        rm -rf {direpa_task_src}_tmp
    
        {step} null_local_remote
        git checkout master
        {cmd}
        _out:# cmp_status: null
        _out:∆ Branch 'fts-add' does not exist on local nor on local_remote.
        _out:√ No action needed for 'synchronize' with "fts-add" on "local_remote"
    
        {step} null_remote
        {cmd}
        _out:# cmp_status: null
        _out:∆ Branch 'fts-add' does not exist on local nor on remote.
        _out:√ No action needed for 'synchronize' with "fts-add" on "remote"
    """)

    start_processor(conf)

if __name__ == "__main__":
    direpa_script=os.path.realpath(__file__)
    while os.path.basename(direpa_script) != "processor":
        direpa_script=os.path.dirname(direpa_script)
    sys.path.insert(0,os.path.dirname(direpa_script))

    from git_helpers.synchronize_branch_name import synchronize_local_with, get_branch_compare_status_repository, get_branch_on

    class Remote_repository():
        def __init__(self):
            self.is_reachable=True

    repo=Remote_repository()
    
    if sys.argv[1] == "up_to_date":
        synchronize_local_with("remote", "master", 
            get_branch_compare_status_repository(
                "remote",
                get_branch_on(repo, "master"),            
                "master"
            )
        )

    elif sys.argv[1] == "pull_synchronize_remote":
        synchronize_local_with("remote", "fts-add", 
            get_branch_compare_status_repository(
                "remote",
                get_branch_on(repo, "fts-add"),            
                "fts-add"
            )
        )

    elif sys.argv[1] == "pull_synchronize_local_remote":
        synchronize_local_with("local_remote", "fts-add", 
            get_branch_compare_status_repository(
                "local_remote",
                get_branch_on(repo, "fts-add"),            
                "fts-add"
            )
        )
    
    elif sys.argv[1] == "pull_not_local_synchronize_local_remote_master":
        synchronize_local_with("local_remote", "master", 
            get_branch_compare_status_repository(
                "local_remote",
                get_branch_on(repo, "master"),            
                "master"
            )
        )

    elif sys.argv[1] == "pull_not_local_synchronize_local_remote_test":
        synchronize_local_with("local_remote", "fts-add", 
            get_branch_compare_status_repository(
                "local_remote",
                get_branch_on(repo, "fts-add"),            
                "fts-add"
            )
        )

    elif sys.argv[1] == "pull_not_local_synchronize_remote":
        synchronize_local_with("remote", "fts-add", 
            get_branch_compare_status_repository(
                "remote",
                get_branch_on(repo, "fts-add"),            
                "fts-add"
            )
        )

    elif sys.argv[1] == "push_synchronize_local_remote":
        synchronize_local_with("local_remote", "fts-add", 
            get_branch_compare_status_repository(
                "local_remote",
                get_branch_on(repo, "fts-add"),            
                "fts-add"
            )
        )

    elif sys.argv[1] == "push_synchronize_remote":
        synchronize_local_with("remote", "fts-add", 
            get_branch_compare_status_repository(
                "remote",
                get_branch_on(repo, "fts-add"),            
                "fts-add"
            )
        ) 
    
    elif sys.argv[1] == "divergent_with_common_ancestor":
        synchronize_local_with("remote", "fts-add", 
            get_branch_compare_status_repository(
                "remote",
                get_branch_on(repo, "fts-add"),            
                "fts-add"
            )
        )

    elif sys.argv[1] == "divergent_without_common_ancestor":
        synchronize_local_with("remote", "fts-add", 
            get_branch_compare_status_repository(
                "remote",
                get_branch_on(repo, "fts-add"),            
                "fts-add"
            )
        )


    elif sys.argv[1] == "null_local_remote":
        synchronize_local_with("local_remote", "fts-add", 
            get_branch_compare_status_repository(
                "local_remote",
                get_branch_on(repo, "fts-add"),            
                "fts-add"
            )
        )

    elif sys.argv[1] == "null_remote":
        synchronize_local_with("remote", "fts-add", 
            get_branch_compare_status_repository(
                "remote",
                get_branch_on(repo, "fts-add"),            
                "fts-add"
            )
        )


