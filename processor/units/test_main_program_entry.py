#!/usr/bin/env python3
import os
if __name__ != "__main__":
    from processor.utils.processor_engine import start_processor, set_task_steps, set_task_vars
    from utils.json_config import Json_config
    
    import sys

def test_main_program_entry(conf):
    set_task_vars(conf, {
        'direpa_task_src': conf["direpa_task_src"],
        'direpa_task': conf["direpa_task"],
        'direpa_task_conf': conf["direpa_task_conf"],
        'diren_src': conf["diren_src"],
        'debug_close_branch':conf["filenpa_launcher"]+" -d --cb",
        'new_project':conf["filenpa_launcher"]+" --np",
        'new_project_directory':conf["filenpa_launcher"]+" --np "+conf["diren_src"],
        'clone_project_to_remote':conf["filenpa_launcher"]+" --cp",
        'open_branch':conf["filenpa_launcher"]+" --ob",
        'pick_up_release':conf["filenpa_launcher"]+" --pr 1.0.0",
        'pick_up_release_create':conf["filenpa_launcher"]+" --pr --da='marc=place'",
        'synchronize_project':conf["filenpa_launcher"]+" -d --sp",
        'update_branch':conf["filenpa_launcher"]+" -u",
        'version':conf["filenpa_launcher"]+" -v",
    })

    set_task_steps(conf,"""
        cd {direpa_task_src}
        
        {step} close_branch and debug
        git checkout develop
        {debug_close_branch}
        _out:### Debug mode started
        _out:× You can't close on branch 'develop'.
        _fail:

        {step} new_project
        {new_project}
        _out:× Current Path '{direpa_task_src}' has a .git directory
        _fail:

        {step} new_project_directory
        cd {direpa_task}
        {new_project_directory}
        _out:× Current Path '{direpa_task_src}' has a .git directory
        _fail:
        cd {direpa_task_src}

        {step} clone_project_to_remote
        {clone_project_to_remote}
        _out:× Remote Directory {direpa_task_src}.git Already Exists on remote repository 'Origin'
        _fail:

        {step} open_branch
        {open_branch}
        _out:Choose a Branch Type or 'q' to quit:
        _type:q
        _fail:

        {step} pick_up_release
        git checkout master
        git tag v0.5.0
        git push origin v0.5.0
        git push origin master
        git checkout develop
        git merge --no-edit master
        git push origin develop
        {pick_up_release}
        _out:× There is no tag in the project that matches v1.0.0
        _fail:
        git checkout master
        git reset --hard start_master
        git tag --delete v0.5.0
        git push origin --delete v0.5.0
        git checkout develop
        git reset --hard start_develop
        git push origin -f master
        git push origin -f develop

        {step} pick_up_release create_new_release
        git checkout master
        git tag v0.5.0
        git push origin v0.5.0
        git push origin master
        git checkout -b fts-work_in_progress
        git merge --no-edit master
        git push origin fts-work_in_progress
        {pick_up_release_create}
        _out:Choose an increment type for tag '0.5.0' or 'q' to quit:
        _type:q
        _fail:
        git checkout master
        git reset --hard start_master
        git tag --delete v0.5.0
        git push origin --delete v0.5.0
        git push origin -f master
        git push origin -f fts-work_in_progress
 
        {step} synchronize_project
        {synchronize_project}
        _out:√ validator

        {step} update_branch
        git checkout develop
        {update_branch}
        _out:√ Branch 'develop' updated.

        {step} version
        git checkout develop
        {version}
        _out:Name: gitframe
    """)

    start_processor(conf)

