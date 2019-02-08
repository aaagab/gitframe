#!/usr/bin/env python3
import os, sys
if __name__ != "__main__":
    from processor.utils.processor_engine import start_processor, set_task_steps, set_task_vars

def test_close_hotfix(conf):
    set_task_vars(conf, {
        "direpa_task_src": conf["direpa_task_src"],
        "clean_tag": 'git tag | grep -Ev "start_develop|start_master" | xargs git tag -d',
        "commit": "git commit --allow-empty -m 'empty_commit'",
        "hotfix_branch": "hfx-1.X.X-my-repair"
    })

    set_task_steps(conf,"""
        cd {direpa_task_src}

        {step} close_hotfix hotfix_on_latest_release
        git checkout master
        git tag v1.0.0
        git checkout master
        git checkout -b hfx-1.X.X-my_repair
        {cmd}
        _out:# hfx-1.X.X-my_repair is on latest release
        _out:### close hfx-1.X.X-my_repair on master
        _out:### close hfx-1.X.X-my_repair on develop
        _out:√ hfx-1.X.X-my_repair has been closed.
        _out:# launch script deploy
        _out:1.0.1
        git checkout master
        git tag --delete v1.0.0
        git tag --delete v1.0.1
        git push origin --delete v1.0.1
        git reset --hard start_master

        {step} close_hotfix with_support_branch
        git checkout master
        git tag v1.0.0
        git tag v2.0.0
        git checkout -b spt-1.X.X
        git checkout master
        git checkout -b hfx-1.X.X-my_repair
        {cmd}
        _out:### close hfx-1.X.X-my_repair on spt-1.X.X
        _out:√ hfx-1.X.X-my_repair has been closed.
        _out:# launch script deploy
        _out:1.0.1
        git checkout master
        git tag --delete v1.0.0
        git tag --delete v2.0.0
        git branch -D spt-1.X.X
        git tag --delete v1.0.1
        git push origin --delete v1.0.1
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
    
    if sys.argv[1] == "close_hotfix":
        from git_helpers.branch.hotfix import close_hotfix
        import git_helpers.regex_obj as ro

        from git_helpers.get_all_branch_regexes import get_all_branch_regexes
        from git_helpers.remote_repository import Remote_repository
        from git_helpers.get_all_version_tags import get_all_version_tags
        repo=Remote_repository()
        regex_branches=get_all_branch_regexes(repo)

        close_hotfix(
            repo, 
            ro.Hotfix_regex("hfx-1.X.X-my_repair"), 
            regex_branches, 
            get_all_version_tags())
        
    elif sys.argv[1] == "is_hotfix_on_latest_release":
        import git_helpers.regex_obj as ro
        from git_helpers.branch.hotfix import is_hotfix_on_latest_release

        print(is_hotfix_on_latest_release(ro.Hotfix_regex("hfx-1.X.X-my_repair"), "2.2.3"))
        print(is_hotfix_on_latest_release(ro.Hotfix_regex("hfx-2.X.X-my_repair"), "2.2.3"))
