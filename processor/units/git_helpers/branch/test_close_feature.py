#!/usr/bin/env python3
import os, sys
if __name__ != "__main__":
    from processor.utils.processor_engine import start_processor, set_task_steps, set_task_vars

def test_close_feature(conf):
    set_task_vars(conf, {
        "direpa_task_src": conf["direpa_task_src"],
    })
    
    set_task_steps(conf, """
        cd {direpa_task_src}

        {step} close_feature no_release
        git checkout develop
        git checkout -b feature-new_function
        git push origin feature-new_function
        {cmd}
        _out:√ git merge --no-edit --no-ff feature-new_function
        _out:√ git branch --delete feature-new_function
        _out:√ git push origin --delete feature-new_function
        _out:√ git push origin develop
        _out:√ feature-new_function has been closed on develop
        git checkout develop
        git reset --hard start_develop
        git push origin --force develop

        {step} close_feature has_a_release_branch
        git checkout develop
        git checkout -b release-1.0.0
        git checkout develop
        git checkout -b feature-new_function
        {cmd}
        _out:× A Feature Branch can't be closed when a release Branch is still open. Close the Branch "release-1.0.0" and retry the operation.
        _fail:
        git checkout develop
        git branch -D release-1.0.0
    """)

    start_processor(conf)

if __name__ == "__main__":
    direpa_script=os.path.realpath(__file__)
    while os.path.basename(direpa_script) != "processor":
        direpa_script=os.path.dirname(direpa_script)
    sys.path.insert(0,os.path.dirname(direpa_script))

    from git_helpers.branch.feature import close_feature
    import git_helpers.regex_obj as ro
    from git_helpers.get_all_branch_regexes import get_all_branch_regexes
    from git_helpers.remote_repository import Remote_repository
    from git_helpers.get_all_version_tags import get_all_version_tags
    repo=Remote_repository()
    regex_branches=get_all_branch_regexes(repo)
    
                
    if sys.argv[1] == "close_feature":
        close_feature(repo, 
            ro.Feature_regex("feature-new_function"), 
            regex_branches, 
            get_all_version_tags())
