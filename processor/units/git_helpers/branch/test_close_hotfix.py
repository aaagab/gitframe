#!/usr/bin/env python3
import os, sys
if __name__ != "__main__":
    from processor.utils.processor_engine import start_processor, set_task_steps, set_task_vars

def test_close_hotfix(conf):
    set_task_vars(conf, {
        "direpa_task_src": conf["direpa_task_src"],
        "clean_tag": 'git tag | grep -Ev "start_develop|start_master" | xargs git tag -d',
        "commit": "git commit --allow-empty -m 'empty_commit'",
        "hotfix_branch": "hotfix-1.0.X-my-repair"
    })

    set_task_steps(conf,"""
        cd {direpa_task_src}

        {step} close_hotfix hotfix_on_latest_release has_release_branch
        git checkout master
        echo 1.0.0 > version.txt
        git add .; git commit -a -m "version"
        git tag v1.0.0
        git checkout -b release-1.0.0
        git checkout master
        git checkout -b hotfix-1.0.X-my_repair
        git tag start-hotfix-1.0.X-my_repair
        {cmd}
        _out:# hotfix-1.0.X-my_repair is on latest release
        _out:### close hotfix-1.0.X-my_repair on master
        _out:### close hotfix-1.0.X-my_repair on release-1.0.0
        _out:### close hotfix-1.0.X-my_repair on develop
        _out:√ hotfix-1.0.X-my_repair has been closed.
        _out:∆  Create a script file deploy_release.sh or deploy_release.py
        _fail:
        git checkout master
        git tag --delete v1.0.0
        git tag --delete start-hotfix-1.0.X-my_repair
        git reset --hard start_master

        {step} close_hotfix hotfix_not_on_latest_release with_support_branch
        git checkout master
        echo 2.0.0 > version.txt
        git add .; git commit -a -m "version"
        git tag v1.0.0
        git tag v2.0.0
        git checkout -b support-1.0.X
        git checkout master
        git checkout -b hotfix-1.0.X-my_repair
        git tag start-hotfix-1.0.X-my_repair
        {cmd}
        _out:### close hotfix-1.0.X-my_repair on support-1.0.X
        _out:√ hotfix-1.0.X-my_repair has been closed.
        _out:∆  Create a script file deploy_release.sh or deploy_release.py
        _fail:
        git checkout master
        git tag --delete v1.0.0
        git tag --delete v2.0.0
        git tag --delete start-hotfix-1.0.X-my_repair
        git branch -D support-1.0.X
        git reset --hard start_master

        {step} update_json_data_hotfix_on_close success
        git checkout master
        git tag v1.0.3
        {cmd}
        _out:√ update_json_data_hotfix_on_close
        git tag --delete v1.0.3
        git reset --hard start_master

        {step} is_hotfix_on_latest_release
        {cmd}
        _out:False
        _out:True
        
    """)

    start_processor(conf)

if __name__ == "__main__":
    direpa_script=os.path.realpath(__file__)
    while os.path.basename(direpa_script) != "processor":
        direpa_script=os.path.dirname(direpa_script)
    sys.path.insert(0,os.path.dirname(direpa_script))
    
    from utils.json_config import Json_config
    fname=Json_config().get_value("filen_hotfix_history")
    
    data={
        "hotfix-1.0.X-my-repair": {
            "description": "This is my new great hotfix",
            "end_commit": "",
            "end_tag": "",
            "start_commit": "5d5fd7df8cb675791b0e581b8526b2ea86134ad5",
            "start_tag": "start-hotfix-1.0.X-my_repair"
        }
    }

    if sys.argv[1] == "close_hotfix":
        from git_helpers.branch.hotfix import close_hotfix
        import git_helpers.regex_obj as ro

        from git_helpers.get_all_branch_regexes import get_all_branch_regexes
        from git_helpers.remote_repository import Remote_repository
        from git_helpers.get_all_version_tags import get_all_version_tags
        repo=Remote_repository()
        regex_branches=get_all_branch_regexes(repo)

        Json_config(fname).set_file_with_data(data)
        os.system("git add .; git commit -a -m 'updated hotfix.json'")
        close_hotfix(
            repo, 
            ro.Hotfix_regex("hotfix-1.0.X-my_repair"), 
            regex_branches, 
            get_all_version_tags())
        
    elif sys.argv[1] == "is_hotfix_on_latest_release":
        import git_helpers.regex_obj as ro
        from git_helpers.branch.hotfix import is_hotfix_on_latest_release

        print(is_hotfix_on_latest_release(ro.Hotfix_regex("hotfix-1.0.X-my_repair"), "2.2.3"))
        print(is_hotfix_on_latest_release(ro.Hotfix_regex("hotfix-2.2.X-my_repair"), "2.2.3"))

    elif sys.argv[1] == "update_json_data_hotfix_on_close":
        from git_helpers.branch.hotfix import update_json_data_hotfix_on_close

        Json_config(fname).set_file_with_data(data)
        update_json_data_hotfix_on_close("hotfix-1.0.X-my_repair", fname, "1.0.3")
        os.system("cat "+fname)
        
        
    
