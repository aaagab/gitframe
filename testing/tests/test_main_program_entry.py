#!/usr/bin/env python3
import os
if __name__ != "__main__":
    from testing.utils.test_processor import test_processor, set_test_steps, set_test_vars
    from utils.json_config import Json_config
    
    import sys

def test_main_program_entry(conf):
    set_test_vars(conf, {
        'direpa_test_src': conf["direpa_test_src"],
        'direpa_test': conf["direpa_test"],
        'direpa_testgf': conf["direpa_testgf"],
        'diren_src': conf["diren_src"],
        'debug_close_branch':conf["direpa_app"]+"/"+conf["filen_app"]+" -d --cb",
        'new_project':conf["direpa_app"]+"/"+conf["filen_app"]+" --np",
        'new_project_directory':conf["direpa_app"]+"/"+conf["filen_app"]+" --np "+conf["diren_src"],
        'clone_project_to_remote':conf["direpa_app"]+"/"+conf["filen_app"]+" --cp",
        'open_branch':conf["direpa_app"]+"/"+conf["filen_app"]+" --ob",
        'publish_early_release':conf["direpa_app"]+"/"+conf["filen_app"]+" --per",
        'publish_release':conf["direpa_app"]+"/"+conf["filen_app"]+" --pr 1.0.0",
        'synchronize_project':conf["direpa_app"]+"/"+conf["filen_app"]+" -d --sp",
        'update_branch':conf["direpa_app"]+"/"+conf["filen_app"]+" -u",
        'version':conf["direpa_app"]+"/"+conf["filen_app"]+" -v",
    })

    set_test_steps(conf,"""
        cd {direpa_test_src}
        
        {step} close_branch and debug
        git checkout develop
        {debug_close_branch}
        _out:-->> # Debug mode started # <<--
        _out:× You can't close on branch 'develop'.
        _fail:

        {step} new_project
        {new_project}
        _out:× Current Path '{direpa_test_src}' has a .git directory
        _fail:

        {step} new_project_directory
        cd {direpa_test}
        {new_project_directory}
        _out:× Current Path '{direpa_test_src}' has a .git directory
        _fail:
        cd {direpa_test_src}

        {step} clone_project_to_remote
        {clone_project_to_remote}
        _out:× Remote Directory {direpa_test_src}.git Already Exists on remote repository 'Origin'
        _fail:

        {step} open_branch
        {open_branch}
        _out:Choose a Branch Type or 'q' to quit:
        _type:q
        _fail:

        {step} publish_early_release
        {publish_early_release}
        _out:∆  Create a script file deploy_release.sh or deploy_release.py
        _fail:
        git tag -l | grep -Ev "start_develop|start_master" | xargs -n 1 git push --delete origin
        git tag | grep -Ev "start_develop|start_master" | xargs git tag -d

        {step} publish_release
        git checkout master
        echo 0.5.0 > version.txt
        git add .; git commit -am "new version"
        git tag v0.5.0
        git push origin v0.5.0
        git push origin master
        git checkout develop
        git merge --no-edit master
        git push origin develop
        {publish_release}
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

    test_processor(conf)

