#!/usr/bin/env python3
import os, sys
from pprint import pprint

if __name__ != "__main__":
    from processor.utils.processor_engine import start_processor, set_task_steps, set_task_vars

def test_synchronize_tags(conf):
    set_task_vars(conf, {
        "direpa_task_src": conf["direpa_task_src"],
        "commit": "git commit --allow-empty -m \"one commit\"",
        "clean_tags": 'git tag | grep -Ev "start_develop|start_master" | xargs git tag -d'
    })

    set_task_steps(conf,"""
        cd {direpa_task_src}

        {step} synchronize_tags local_tag
        {cmd}
        _out:∆ tag 'start_master' exists on local but not on remote. tag not pushed.
        _out:√ synchronize_tags

        {step} synchronize_tags remote_tag
        git tag my_tag
        git push origin my_tag
        git tag --delete my_tag
        {cmd}
        _out:∆ tag 'my_tag' exists on remote but not on local. tag not pulled.
        _out:√ synchronize_tags
        git push origin --delete my_tag

        {step} synchronize_tags not_reachable
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

    if sys.argv[1] == "synchronize_tags":
        from git_helpers.remote_repository import Remote_repository
        repo=Remote_repository()
        from git_helpers.validator.synchronize_tags import synchronize_tags
        
        if sys.argv[2] == "local_tag":
            synchronize_tags(repo)
        elif sys.argv[2] == "remote_tag":
            synchronize_tags(repo)
        elif sys.argv[2] == "not_reachable":
            repo.is_reachable=False
            synchronize_tags(repo)

    elif sys.argv[1] == "process_tag_not_found":
        from git_helpers.validator.synchronize_tags import process_tag_not_found
        
        if sys.argv[2] == "release_tag_remote":
            process_tag_not_found("v1.0.0", "remote")
        elif sys.argv[2] == "release_tag_local":
            process_tag_not_found("v1.0.0", "local")
        elif sys.argv[2] == "hotfix_tag_remote":
            process_tag_not_found("v1.0.1", "remote")
        elif sys.argv[2] == "hotfix_tag_local":
            process_tag_not_found("v1.0.1", "local")
        elif sys.argv[2] == "user_tag_remote":
            process_tag_not_found("my_tag", "remote")
        elif sys.argv[2] == "user_tag_local":
            process_tag_not_found("my_tag", "local")
        
        
