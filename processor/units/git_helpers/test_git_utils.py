#!/usr/bin/env python3
import os, sys
if __name__ != "__main__":
    from processor.utils.processor_engine import start_processor, set_task_steps, set_task_vars

def test_git_utils(conf):
    set_task_vars(conf, {
        "direpa_test_src": conf["direpa_test_src"],
        "commit": "git commit --allow-empty -m",
        "clean_compare": "git checkout develop; git reset --hard start_develop; git branch -D test",
        "direpa_testgf": conf["direpa_testgf"]
    })

    set_task_steps(conf,"""
        cd {direpa_test_src}

        {step} get_latest_release_for_each_major
        {cmd}
        _out:['1.2.0', '2.1.0', '3.1.0']

        {step} get_branch_compare_status up_to_date
        git checkout develop
        git checkout -b test
        {cmd}
        _out:up_to_date
        {clean_compare}
    
        {step} get_branch_compare_status pull
        git checkout develop
        git checkout -b test
        {commit} "empty"
        {cmd}
        _out:pull
        {clean_compare}
    
        {step} get_branch_compare_status push
        git checkout develop
        git checkout -b test
        git checkout develop
        {commit} "empty"
        {cmd}
        _out:push
        {clean_compare}
    
        {step} get_branch_compare_status divergent_with_common_ancestor
        git checkout develop
        git checkout -b test
        git checkout develop
        {commit} "empty1"
        git checkout test
        {commit} "empty2"
        {cmd}
        _out:divergent_with_common_ancestor
        {clean_compare}
    
        {step} get_branch_compare_status divergent_without_common_ancestor
        git checkout develop
        git checkout --orphan test
        {commit} "empty"
        {cmd}
        _out:divergent_without_common_ancestor
        {clean_compare}

        {step} has_git_directory no_directory
        {cmd}
        _out:False

        {step} has_git_directory directory
        cd {direpa_testgf}
        git init
        {cmd}
        _out:True
        rm -rf .git
        cd -

    """)

    start_processor(conf)

if __name__ == "__main__":
    direpa_script=os.path.realpath(__file__)
    while os.path.basename(direpa_script) != "processor":
        direpa_script=os.path.dirname(direpa_script)
    sys.path.insert(0,os.path.dirname(direpa_script))

    import git_helpers.git_utils as git
    
    if sys.argv[1] == "get_latest_release_for_each_major":
        print(git.get_latest_release_for_each_major(
            ['1.0.0', '1.1.0', '1.2.0', '2.0.0', '2.1.0', '3.0.0', '3.1.0']
        ))
    elif sys.argv[1] == "get_branch_compare_status":
        print(git.get_branch_compare_status("develop", "test"))

    elif sys.argv[1] == "has_git_directory":
        from utils.json_config import Json_config
        conf=Json_config().data
        
        if sys.argv[2] == "no_directory":
            print(git.has_git_directory(conf["processor"]["task"]["direpa_root"]))
        elif sys.argv[2] == "directory":
            print(git.has_git_directory())
    