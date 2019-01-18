#!/usr/bin/env python3
import os, sys
if __name__ != "__main__":
    from processor.utils.processor_engine import start_processor, set_task_steps, set_task_vars

def test_create_new_release(conf):
    set_task_vars(conf, {
        "direpa_task_src": conf["direpa_task_src"],
        "direpa_task": conf["direpa_task"],
        "filenpa_deploy": conf["filenpa_deploy"]
    })

    set_task_steps(conf, """
        cd {direpa_task_src}
        git checkout master

        echo '#!/bin/bash' > {filenpa_deploy}
        echo 'echo $1' >> {filenpa_deploy}
        echo 'echo $2' >> {filenpa_deploy}
        chmod +x {filenpa_deploy}

        {step} non_deploy_args non_authorized
        git checkout master
        {cmd}
        _out:  × Non-authorized branch type 'master'
        _fail:

        {step} non_deploy_args authorized no_version_at_start
        git checkout -b fts-work_in_progress
        {cmd}
        _out:Type release version to start with(ex:0.1.0) [q to quit]:
        _type:marc
        _out:∆ Version release must be of the form '\d+\.\d+\.\d+'
        _out:Type release version to start with(ex:0.1.0) [q to quit]:
        _type:0.1.0
        _out:Is this a recommended release version [y/N/q]:
        _type:n
        git checkout master
        git branch -d fts-work_in_progress

        {step} non_deploy_args has_already_versions hotfixes stop
        git checkout master
        git tag -a v1.3.7 -m 'release_1'
        git tag -a v2.5.1 -m 'release_2'
        git checkout -b hfx-2.X.X-repair
        git checkout -b fts-work_in_progress
        {cmd}
        _out:Choose an increment type for tag '2.5.1' or 'q' to quit:
        _type:1
        _out:Do you want to continue anyway [Y/n/q]:
        _type:n
        _out:∆ Gitframe Create a new release cancelled
        _fail:
        git checkout master
        git branch -d hfx-2.X.X-repair
        git branch -d fts-work_in_progress
        git tag --delete v1.3.7
        git tag --delete v2.5.1

        {step} deploy_args has_already_versions hotfixes continue
        git checkout master
        git tag -a v1.3.7 -m 'release_1'
        git tag -a v2.5.1 -m 'release_2'
        git checkout -b hfx-2.X.X-repair
        git checkout -b fts-work_in_progress
        {cmd}
        _out:Choose an increment type for tag '2.5.1' or 'q' to quit:
        _type:1
        _out:Do you want to continue anyway [Y/n/q]:
        _type:Y
        _out:√ git checkout -b spt-2.X.X v2.5.1
        _out:Is this a recommended release version [y/N/q]:
        _type:Y
        _out:√ git tag -a v3.0.0-r -m 'release'
        _out:3.0.0-r
        _out:publish=now
        git checkout master
        git branch -d hfx-2.X.X-repair
        git branch -d fts-work_in_progress
        git branch -d spt-2.X.X
        git tag --delete v1.3.7
        git tag --delete v2.5.1
        git tag --delete v3.0.0-r

    """)
            
    start_processor(conf)

if __name__ == "__main__":
    direpa_script=os.path.realpath(__file__)
    while os.path.basename(direpa_script) != "processor":
        direpa_script=os.path.dirname(direpa_script)
    sys.path.insert(0,os.path.dirname(direpa_script))

    from git_helpers.create_new_release import create_new_release
    
    if sys.argv[1] == "non_deploy_args":
        create_new_release()
    elif sys.argv[1] == "deploy_args":
        create_new_release("","","","publish=now test=here")

