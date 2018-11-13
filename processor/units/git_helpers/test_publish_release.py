#!/usr/bin/env python3
import os, sys
if __name__ != "__main__":
    from processor.utils.processor_engine import start_processor, set_task_steps, set_task_vars

def test_publish_release(conf):
    set_task_vars(conf, {
        "direpa_task_src": conf["direpa_task_src"],
        "direpa_scripts": conf["direpa_scripts"],
        "filenpa_deploy_release": conf["filenpa_deploy_release"]
    })

    set_task_steps(conf, """
        cd {direpa_task_src}
        git checkout master

        # create a file
        echo "I created you" > myfile.txt
        git add .
        git commit -a -m 'added myfile.txt' 
        
        # create a release
        echo 1.0.1 > version.txt
        git add .
        git commit -a -m 'version.txt'
        git tag -a v1.0.1 -m 'release'

        mkdir -p {direpa_scripts}
        echo '#!/bin/bash' > {filenpa_deploy_release}
        echo 'echo $1' >> {filenpa_deploy_release}
        echo 'echo $2' >> {filenpa_deploy_release}
        chmod +x {filenpa_deploy_release}

        {step} notReleaseOrEarlyRelease
        {cmd}
        _out:× Release tag authorized forms:
        _fail:
    
        {step} release noVchar
        {cmd}
        _out:# release
        _out:× There is no tag in the project that matches v1.0.0
        _fail:

        {step} release withVchar
        {cmd}
        _out:# release
        _out:× There is no tag in the project that matches v1.0.0
        _fail:

        {step} early_release fail
        {cmd}
        _out:# early_release 
        _out:× There is no tag in the project that matches v1.0.0-beta-1541085957
        _fail:

        {step} early_release success
        git tag -a v1.0.0-beta-1541085957 -m 'early-release'
        {cmd}
        _out:# early_release
        _out:# launch script deploy_release
        _out:1.0.0-beta-1541085957
        _out:early_release

        {step} release success
        {cmd}
        _out:# launch script deploy_release
        _out:1.0.1
    """)
            
    start_processor(conf)

if __name__ == "__main__":
    direpa_script=os.path.realpath(__file__)
    while os.path.basename(direpa_script) != "processor":
        direpa_script=os.path.dirname(direpa_script)
    sys.path.insert(0,os.path.dirname(direpa_script))

    from git_helpers.publish_release import publish_release
    from git_helpers.get_all_version_tags import get_all_version_tags
    
    if sys.argv[1] == "notReleaseOrEarlyRelease":
        publish_release("myCustomTag", get_all_version_tags())
    elif sys.argv[1] == "release":
        if sys.argv[2] == "noVchar":
            publish_release("1.0.0", get_all_version_tags())
        elif sys.argv[2] == "withVchar":
            publish_release("v1.0.0", get_all_version_tags())
        elif sys.argv[2] == "success":
            publish_release("1.0.1", get_all_version_tags())
    elif sys.argv[1] == "early_release":
        publish_release("v1.0.0-beta-1541085957", get_all_version_tags())

