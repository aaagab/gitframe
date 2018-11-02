#!/usr/bin/env python3
import os, sys
if __name__ != "__main__":
    from processor.utils.processor_engine import start_processor, set_task_steps, set_task_vars

def test_synchronize_local_with(conf):
    set_task_vars(conf, {
        "direpa_test_src": conf["direpa_test_src"],
        "commit": "git commit --allow-empty -m"        
    })

    set_task_steps(conf, """
        {step} cd
        cd {direpa_test_src}
    
        {step} up_to_date
        {cmd}
        _out:# cmp_status: up_to_date
        _out:√ No action needed for 'synchronize' with "master" on "remote"
    
        {step} pull_synchronize_local_remote
        git checkout -b feature-add
        git tag start_feature
        {commit} "1"
        git push origin feature-add
        git reset --hard start_feature
        {cmd}
        _out:# cmp_status: pull
        _out:choice or 'q' to quit:
        _type:2
    
        {step} pull_synchronize_remote
        {cmd}
        _out:# cmp_status: pull
        _out:choice or 'q' to quit:
        _type:2
        
        {step} pull_not_local_synchronize_local_remote_master
        git branch -D master
        {cmd}
        _out:# cmp_status: pull_not_local
        _out:choice or 'q' to quit:
        _type:1
    
        {step} pull_not_local_synchronize_local_remote_test
        git checkout master
        git branch -D feature-add
        {cmd}
        _out:# cmp_status: pull_not_local
        _out:√ No action needed for 'synchronize' with "feature-add" on "local_remote"
    
        {step} pull_not_local_synchronize_remote
        {cmd}
        _out:# cmp_status: pull_not_local
        _out:choice or 'q' to quit:
        _type:2
       
        {step} push_synchronize_local_remote
        git checkout feature-add
        {commit} "2"
        {cmd}
        _out:# cmp_status: push
        _out:∆ Push is never done to local_remote branches, local is already the newest
    
        {step} push_synchronize_remote
        {cmd}
        _out:# cmp_status: push
        _out:choice or 'q' to quit:
        _type:2
       
        {step} divergent_with_common_ancestor
        git reset --hard start_feature
        {commit} "4"
        {cmd}
        _out:# cmp_status: divergent_with_common_ancestor
        _out:√ divergent_with_common_ancestor
        _fail:Normal Exit for divergent_with_common_ancestor
    
        {step} divergent_without_common_ancestor
        git checkout master
        git branch -D feature-add
        git checkout --orphan feature-add
        {commit} "5"
        {cmd}
        _out:# cmp_status: divergent_without_common_ancestor
        _out:√ divergent_without_common_ancestor
        _fail:Normal Exit for divergent_without_common_ancestor
    
        {step} null_local_remote
        git checkout master
        git branch -D feature-add
        git push origin --delete feature-add
        {cmd}
        _out:# cmp_status: null
        _out:∆ Branch 'feature-add' does not exist on local nor on local_remote.
        _out:√ No action needed for 'synchronize' with "feature-add" on "local_remote"
    
        {step} null_remote
        {cmd}
        _out:# cmp_status: null
        _out:∆ Branch 'feature-add' does not exist on local nor on remote.
        _out:√ No action needed for 'synchronize' with "feature-add" on "remote"
    """)

    start_processor(conf)

if __name__ == "__main__":
    direpa_script=os.path.realpath(__file__)
    while os.path.basename(direpa_script) != "processor":
        direpa_script=os.path.dirname(direpa_script)
    sys.path.insert(0,os.path.dirname(direpa_script))

    from git_helpers.synchronize_branch_name import synchronize_local_with

    class Remote_repository():
        def __init__(self):
            self.is_reachable=True

    repo=Remote_repository()
        
    if sys.argv[1] == "up_to_date":
        synchronize_local_with("remote", "master", repo)

    elif sys.argv[1] == "pull_synchronize_remote":
        synchronize_local_with("remote", "feature-add", repo)

    elif sys.argv[1] == "pull_synchronize_local_remote":
        synchronize_local_with("local_remote", "feature-add", repo)
    
    elif sys.argv[1] == "pull_not_local_synchronize_local_remote_master":
        synchronize_local_with("local_remote", "master", repo)

    elif sys.argv[1] == "pull_not_local_synchronize_local_remote_test":
        synchronize_local_with("local_remote", "feature-add", repo)

    elif sys.argv[1] == "pull_not_local_synchronize_remote":
        synchronize_local_with("remote", "feature-add", repo)

    elif sys.argv[1] == "push_synchronize_local_remote":
        synchronize_local_with("local_remote", "feature-add", repo)

    elif sys.argv[1] == "push_synchronize_remote":
        synchronize_local_with("remote", "feature-add", repo) 
    
    elif sys.argv[1] == "divergent_with_common_ancestor":
        synchronize_local_with("remote", "feature-add", repo)

    elif sys.argv[1] == "divergent_without_common_ancestor":
        synchronize_local_with("remote", "feature-add", repo)


    elif sys.argv[1] == "null_local_remote":
        synchronize_local_with("local_remote", "feature-add", repo)

    elif sys.argv[1] == "null_remote":
        synchronize_local_with("remote", "feature-add", repo)


