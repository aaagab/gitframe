#!/usr/bin/env python3
import os, sys
if __name__ != "__main__":
    from processor.utils.processor_engine import start_processor, set_task_steps, set_task_vars

def test_version_tags_validator(conf):
    set_task_vars(conf, {
        "direpa_task_src": conf["direpa_task_src"],
    })

    set_task_steps(conf,"""
        cd {direpa_task_src}

        {step} version_tags_validator support
        git checkout master
        git tag v1.0.0
        git checkout master
        git checkout -b spt-0.X.X
        git tag v0.5.0
        {cmd}
        _out:√ find_related_tag_for_support_branch_name
        _out:√ version_tags_validator
        git checkout master
        git reset --hard start_master
        git checkout develop
        git reset --hard start_develop
        git tag --delete v1.0.0
        git tag --delete v0.5.0
        git branch -D spt-0.X.X

        {step} version_tags_validator hotfix
        git checkout master
        git tag v1.0.0
        git checkout -b hfx-1.X.X-my_repair
        {cmd}
        _out:√ hotfix 'hfx-1.X.X-my_repair' comes from latest release '1.0.0'
        _out:√ version_tags_validator
        git checkout master
        git reset --hard start_master
        git checkout develop
        git reset --hard start_develop
        git tag --delete v1.0.0
        git branch -D hfx-1.X.X-my_repair

        {step} version_tags_validator no_release_tags hotfix_branch_not_allowed
        git checkout master
        git checkout -b hfx-1.X.X-my_repair
        {cmd}
        _out:× The project has no release tags
        _out:×  Branch 'hfx-1.X.X-my_repair' shouldn't exist.
        _fail:
        git checkout master
        git reset --hard start_master
        git branch -D hfx-1.X.X-my_repair

    """)

    start_processor(conf)

if __name__ == "__main__":
    direpa_script=os.path.realpath(__file__)
    while os.path.basename(direpa_script) != "processor":
        direpa_script=os.path.dirname(direpa_script)
    sys.path.insert(0,os.path.dirname(direpa_script))
    
    if sys.argv[1] == "version_tags_validator":
        from git_helpers.validator.version_tags import version_tags_validator

        from git_helpers.get_all_version_tags import get_all_version_tags
        from git_helpers.get_all_branch_regexes import get_all_branch_regexes
        from git_helpers.remote_repository import Remote_repository
        repo=Remote_repository()
        regex_branches=get_all_branch_regexes(repo)

        version_tags_validator(regex_branches, get_all_version_tags())
