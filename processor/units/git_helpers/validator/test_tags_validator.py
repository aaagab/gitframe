#!/usr/bin/env python3
import os, sys
from pprint import pprint

if __name__ != "__main__":
    from processor.utils.processor_engine import start_processor, set_task_steps, set_task_vars

def test_tags_validator(conf):
    set_task_vars(conf, {
        "direpa_task_src": conf["direpa_task_src"],
        "commit": "git commit --allow-empty -m \"one commit\"",
        "clean_tags": 'git tag | grep -Ev "start_develop|start_master" | xargs git tag -d'
    })

    set_task_steps(conf,"""
        cd {direpa_task_src}

        {step} tags_validator local_tag
        {cmd}
        _out:∆ tag 'start_master' exists on local but not on remote. tag not pushed.
        _out:√ tags_validator

        {step} tags_validator remote_tag
        git tag my_tag
        git push origin my_tag
        git tag --delete my_tag
        {cmd}
        _out:∆ tag 'my_tag' exists on remote but not on local. tag not pulled.
        _out:√ tags_validator
        git push origin --delete my_tag

        {step} tags_validator not_reachable
        {cmd}
        _out:∆ Remote is not reachable, Tags can't be compared from local to remote

         {step} process_tag_not_found release_tag_remote
        {cmd}
        _out:× tag 'v1.0.0' exists on local but not on remote. tag not pushed.
        _out:× Maybe master branch needs to be pushed with the tag.
        _fail:

        {step} process_tag_not_found release_tag_local
        {cmd}
        _out:× tag 'v1.0.0' exists on remote but not on local. tag not pulled.
        _out:× Maybe master branch needs to be pulled with the tag.
        _fail:

        {step} process_tag_not_found hotfix_tag_remote
        {cmd}
        _out:× tag 'v1.0.1' exists on local but not on remote. tag not pushed.
        _out:× Maybe a support branch or master needs to be pushed with the tag.
        _fail:

        {step} process_tag_not_found hotfix_tag_local
        {cmd}
        _out:× tag 'v1.0.1' exists on remote but not on local. tag not pulled.
        _out:× Maybe a support branch or master needs to be pulled with the tag.
        _fail:

        {step} process_tag_not_found early_release_tag_remote
        {cmd}
        _out:× tag 'v1.0.0-alpha-0123532143424' exists on local but not on remote. tag not pushed.
        _out:× Define from which branch this tag has been generated and push the branch with the tag.
        _fail:

        {step} process_tag_not_found early_release_tag_local
        {cmd}
        _out:× tag 'v1.0.0-alpha-0123532143424' exists on remote but not on local. tag not pulled.
        _out:× Define from which branch this tag has been generated and pull the branch with the tag.
        _fail:

        {step} process_tag_not_found start_hotfix_tag_remote
        {cmd}
        _out:× tag 'start-hotfix-1.0.X-repair_function' exists on local but not on remote. tag not pushed.
        _out:× Maybe a hotfix branch needs to be pushed with the tag.
        _fail:

        {step} process_tag_not_found start_hotfix_tag_local
        {cmd}
        _out:× tag 'start-hotfix-1.0.X-repair_function' exists on remote but not on local. tag not pulled.
        _out:× Maybe a hotfix branch needs to be pulled with the tag.
        _fail:

        {step} process_tag_not_found user_tag_remote
        {cmd}
        _out:∆ tag 'my_tag' exists on local but not on remote. tag not pushed.
        
        {step} process_tag_not_found user_tag_local
        {cmd}
        _out:∆ tag 'my_tag' exists on remote but not on local. tag not pulled.
    """)

    start_processor(conf)

if __name__ == "__main__":
    direpa_script=os.path.realpath(__file__)
    while os.path.basename(direpa_script) != "processor":
        direpa_script=os.path.dirname(direpa_script)
    sys.path.insert(0,os.path.dirname(direpa_script))

    if sys.argv[1] == "tags_validator":
        from git_helpers.remote_repository import Remote_repository
        repo=Remote_repository()
        from git_helpers.validator.tags import tags_validator
        
        if sys.argv[2] == "local_tag":
            tags_validator(repo)
        elif sys.argv[2] == "remote_tag":
            tags_validator(repo)
        elif sys.argv[2] == "not_reachable":
            repo.is_reachable=False
            tags_validator(repo)

    elif sys.argv[1] == "process_tag_not_found":
        from git_helpers.validator.tags import process_tag_not_found
        
        if sys.argv[2] == "release_tag_remote":
            process_tag_not_found("v1.0.0", "remote")
        elif sys.argv[2] == "release_tag_local":
            process_tag_not_found("v1.0.0", "local")
        elif sys.argv[2] == "hotfix_tag_remote":
            process_tag_not_found("v1.0.1", "remote")
        elif sys.argv[2] == "hotfix_tag_local":
            process_tag_not_found("v1.0.1", "local")
        elif sys.argv[2] == "early_release_tag_remote":
            process_tag_not_found("v1.0.0-alpha-0123532143424", "remote")
        elif sys.argv[2] == "early_release_tag_local":
            process_tag_not_found("v1.0.0-alpha-0123532143424", "local")
        elif sys.argv[2] == "start_hotfix_tag_remote":
            process_tag_not_found("start-hotfix-1.0.X-repair_function", "remote")
        elif sys.argv[2] == "start_hotfix_tag_local":
            process_tag_not_found("start-hotfix-1.0.X-repair_function", "local")
        elif sys.argv[2] == "user_tag_remote":
            process_tag_not_found("my_tag", "remote")
        elif sys.argv[2] == "user_tag_local":
            process_tag_not_found("my_tag", "local")
        
        
