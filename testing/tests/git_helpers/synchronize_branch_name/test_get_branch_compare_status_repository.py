#!/usr/bin/env python3
import os, sys
if __name__ != "__main__":
    from testing.utils.test_processor import test_processor, set_test_steps, set_test_vars

def test_get_branch_compare_status_repository(conf):
    set_test_vars(conf, {
        "direpa_test_src": conf["direpa_test_src"],
        "commit": "git commit --allow-empty -m"
    })

    set_test_steps(conf ,"""

        cd {direpa_test_src}

        {step} local_remote_and_local_and_up_to_date
        git checkout -b test
        git tag start_test
        git push origin test
        {cmd}
        _out:up_to_date
      
        {step} local_remote_and_not_local_and_pull_not_local
        git checkout develop
        git branch -D test
        {cmd}
        _out:pull_not_local
    
        {step} not_local_remote_and_local_push
        git branch -rd origin/test
        git checkout -b test
        {cmd}
        _out:push
    
        {step} not_local_remote_and_not_local_and_null
        git checkout develop
        git branch -D test
        {cmd}
        _out:null
    
        {step} remote_and_local_and_up_to_date
        git push origin --delete test
        git checkout -b test
        git push origin test
        {cmd}
        _out:up_to_date
       
        {step} remote_and_not_local_and_pull_not_local
        git checkout develop
        git branch -D test
        {cmd}
        _out:pull_not_local
    
        {step} not_remote_and_local_and_push
        git push origin --delete test
        git checkout -b test
        {cmd}
        _out:push
    
        {step} not_remote_and_not_local_and_null
        git checkout develop
        git branch -D test
        {cmd}
        _out:null
    """)

    test_processor(conf)
    

if __name__ == "__main__":
    direpa_script=os.path.realpath(__file__)
    while os.path.basename(direpa_script) != "testing":
        direpa_script=os.path.dirname(direpa_script)
    sys.path.insert(0,os.path.dirname(direpa_script))

    from git_helpers.synchronize_branch_name import get_branch_compare_status_repository

    if sys.argv[1] == "local_remote_and_local_and_up_to_date":
        print(get_branch_compare_status_repository("local_remote", {"local":True, "local_remote":True, "remote":True }, "test"))

    elif sys.argv[1] == "local_remote_and_not_local_and_pull_not_local":
        print(get_branch_compare_status_repository("local_remote", {"local":False, "local_remote":True, "remote":True }, "test"))

    elif sys.argv[1] == "not_local_remote_and_local_push":
        print(get_branch_compare_status_repository("local_remote", {"local":True, "local_remote":False, "remote":True }, "test"))

    elif sys.argv[1] == "not_local_remote_and_not_local_and_null":
        print(get_branch_compare_status_repository("local_remote", {"local":False, "local_remote":False, "remote":True }, "test"))

    elif sys.argv[1] == "remote_and_local_and_up_to_date":
        print(get_branch_compare_status_repository("remote", {"local":True, "local_remote":True, "remote":True }, "test"))

    elif sys.argv[1] == "remote_and_not_local_and_pull_not_local":
        print(get_branch_compare_status_repository("remote", {"local":False, "local_remote":True, "remote":True }, "test"))

    elif sys.argv[1] == "not_remote_and_local_and_push":
        print(get_branch_compare_status_repository("remote", {"local":True, "local_remote":True, "remote":False }, "test"))

    elif sys.argv[1] == "not_remote_and_not_local_and_null":
        print(get_branch_compare_status_repository("remote", {"local":False, "local_remote":True, "remote":False }, "test"))
