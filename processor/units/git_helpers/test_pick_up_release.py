#!/usr/bin/env python3
import os, sys
if __name__ != "__main__":
    from processor.utils.processor_engine import start_processor, set_task_steps, set_task_vars

def test_pick_up_release(conf):
    set_task_vars(conf, {
        "direpa_task_src": conf["direpa_task_src"],
        "direpa_task": conf["direpa_task"],
        "filenpa_deploy": conf["filenpa_deploy"]
    })

    set_task_steps(conf, """
        cd {direpa_task_src}
        git checkout master

        # create a file
        echo "I created you" > myfile.txt
        git add .
        git commit -a -m 'added myfile.txt' 
        
        # create a release
        git tag -a v1.0.1 -m 'release'

        echo '#!/bin/bash' > {filenpa_deploy}
        echo 'echo $1' >> {filenpa_deploy}
        echo 'echo $2' >> {filenpa_deploy}
        chmod +x {filenpa_deploy}

        {step} notRelease
        {cmd}
        _out:× Release tag authorized forms:
        _fail:
    
        {step} release noVchar
        {cmd}
        _out:× There is no tag in the project that matches v1.0.0
        _fail:

        {step} release withVchar
        {cmd}
        _out:× There is no tag in the project that matches v1.0.0
        _fail:

        {step} release success
        {cmd}
        _out:# launch script deploy
        _out:1.0.1

        {step} release deploy_args
        {cmd}
        _out:# launch script deploy
        _out:1.0.1
        _out:this_is_a_deploy_arg
    """)
            
    start_processor(conf)

if __name__ == "__main__":
    direpa_script=os.path.realpath(__file__)
    while os.path.basename(direpa_script) != "processor":
        direpa_script=os.path.dirname(direpa_script)
    sys.path.insert(0,os.path.dirname(direpa_script))

    from git_helpers.pick_up_release import pick_up_release

    if sys.argv[1] == "notRelease":
        pick_up_release("myCustomTag")
    elif sys.argv[1] == "release":
        if sys.argv[2] == "noVchar":
            pick_up_release("1.0.0")
        elif sys.argv[2] == "withVchar":
            pick_up_release("v1.0.0")
        elif sys.argv[2] == "success":
            pick_up_release("1.0.1")
        elif sys.argv[2] == "deploy_args":
            pick_up_release("1.0.1", "this_is_a_deploy_arg")
