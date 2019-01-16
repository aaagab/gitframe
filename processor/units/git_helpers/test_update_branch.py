#!/usr/bin/env python3
import os, sys
if __name__ != "__main__":
    from processor.utils.processor_engine import start_processor, set_task_steps, set_task_vars

def test_update_branch(conf):
    set_task_vars(conf, {
        "direpa_task_src": conf["direpa_task_src"],
        "commit": "git commit --allow-empty -m",        
    })
    
    set_task_steps(conf, """
        cd {direpa_task_src}

        {step} update_branch master
        git checkout master
        {cmd}
        _out:√ Branch 'master' updated.

        {step} update_branch feature up_to_date
        git checkout develop
        git checkout -b fts-my_function
        {cmd}
        _out:# up_to_date
        _out:√ Branch 'fts-my_function' updated.
        git checkout develop
        git branch -D fts-my_function

        {step} update_branch feature up_to_date
        git checkout develop
        git checkout -b fts-my_function
        git checkout develop
        {commit} "empty"
        git checkout fts-my_function
        {cmd}
        _out:# pull
        _out:√ git merge --no-edit --no-ff develop
        _out:√ Branch 'fts-my_function' updated.
        git checkout develop
        git reset --hard start_develop
        git branch -D fts-my_function

        {step} update_branch feature divergent_no_ancestor
        git checkout develop
        git checkout --orphan fts-my_function
        {commit} "empty"
        {cmd}
        _out:# divergent_without_common_ancestor
        _out× Compare Status for 'fts-my_function' and 'develop' is 'divergent_without_common_ancestor'
        _fail:
        git checkout develop
        git branch -D fts-my_function

        {step} update_branch hotfix from_master up_to_date
        git checkout master
        git tag v2.0.0
        git checkout -b hfx-2.X.X-my_repair
        {cmd}
        _out:# Linked branch: master
        _out:# up_to_date
        _out:√ Branch 'hfx-2.X.X-my_repair' updated.        
        git checkout develop
        git branch -D hfx-2.X.X-my_repair
        git tag --delete v2.0.0

        {step} update_branch hotfix from_support up_to_date
        git checkout master
        git tag v1.0.0
        git tag v2.0.0
        git checkout -b spt-1.X.X
        git checkout -b hfx-1.X.X-my_repair
        {cmd}
        _out:# Linked branch: spt-1.X.X
        _out:# up_to_date
        _out:√ Branch 'hfx-1.X.X-my_repair' updated.        
        git checkout develop
        git branch -D hfx-1.X.X-my_repair
        git branch -D spt-1.X.X
        git tag --delete v1.0.0
        git tag --delete v2.0.0
    """)

    start_processor(conf)

if __name__ == "__main__":
    direpa_script=os.path.realpath(__file__)
    while os.path.basename(direpa_script) != "processor":
        direpa_script=os.path.dirname(direpa_script)
    sys.path.insert(0,os.path.dirname(direpa_script))
    
    from git_helpers.get_all_version_tags import get_all_version_tags

    if sys.argv[1] == "update_branch":
        from git_helpers.update_branch import update_branch
        update_branch(get_all_version_tags())
