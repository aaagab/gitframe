#!/usr/bin/env python3
import os, sys
if __name__ != "__main__":
    from testing.utils.test_processor import test_processor, set_test_steps, set_test_vars

def test_publish_early_release(conf):
    set_test_vars(conf, {
        "direpa_test_src": conf["direpa_test_src"],
        "direpa_test": conf["direpa_test"],
    })
    
    set_test_steps(conf, """
        {step} prepare for publish_release
        cd {direpa_test_src}
        # {create_deploy_release}
        mkdir -p {direpa_test}/scripts
        echo '#!/bin/bash' > {direpa_test}/scripts/deploy_release.sh
        echo 'echo $1' >> {direpa_test}/scripts/deploy_release.sh
        echo 'echo $2' >> {direpa_test}/scripts/deploy_release.sh
        chmod +x {direpa_test}/scripts/deploy_release.sh
     
        {step} publish_early_release on_release
        git checkout -b release-2.1.0
        echo 2.1.0 > version.txt
        git add .
        git commit -a -m "add version file"
        {cmd}
        _out:# branch_type: release
        _out:Choose an early release type for tag '2.1.0' or 'q' to quit:
        _type:3
        _out:# launch script deploy_release
        git checkout master
        git branch -D release-2.1.0
        git reset --hard start_develop

        {step} publish_early_release on_feature no_release_branch no_version_value 
        git checkout master
        git checkout -b feature-worker
        {cmd}
        _out:# branch_type: feature                                                          
        _out:# no release branches existing
        _out:# no version_value
        _out:# launch script deploy_release
        git checkout master
        git branch -D feature-worker

        {step} publish_early_release on_feature no_release_branch version_value 
        git checkout master
        echo 2.3.0 > version.txt
        git add .
        git commit -a -m "add version file"
        git checkout -b feature-worker
        {cmd}
        _out:# branch_type: feature                                                          
        _out:# no release branches existing
        _out:# version_value
        _out:Choose an increment type for tag '2.3.0' or 'q' to quit:
        _type:1
        _out:# launch script deploy_release
        git checkout master
        git branch -D feature-worker
        git reset --hard start_develop

        {step} publish_early_release on_feature release_branch
        git checkout -b release-3.1.0
        echo 3.1.0 > version.txt
        git add .
        git commit -a -m "add version file"
        git checkout master
        git checkout -b feature-worker
        {cmd}
        _out:# branch_type: feature                                                          
        _out:# release branches existing
        _out:Choose an increment type for tag '3.1.0' or 'q' to quit:
        _type:2
        _out:# launch script deploy_release
        git checkout master
        git branch -D feature-worker
        git branch -D release-3.1.0
        
        {step} publish_early_release on_develop
        git checkout develop
        {cmd}
        _out:# branch_type: develop
        _out:# no release branches existing
        _out:# no version_value
        _out:# launch script deploy_release

        {step} publish_early_release on_master
        git checkout master
        {cmd}
        _out:× Publish early version only applies to 'develop', 'feature' or 'release' branch type.
        _fail:

        rm {direpa_test}/scripts/deploy_release.sh
    """)

    test_processor(conf)

if __name__ == "__main__":
    direpa_script=os.path.realpath(__file__)
    while os.path.basename(direpa_script) != "testing":
        direpa_script=os.path.dirname(direpa_script)
    sys.path.insert(0,os.path.dirname(direpa_script))

    from git_helpers.publish_early_release import publish_early_release
    from git_helpers.get_all_branch_regexes import get_all_branch_regexes
    from git_helpers.remote_repository import Remote_repository

    repo=Remote_repository()
    regex_branches=get_all_branch_regexes(repo)

    publish_early_release(
        Remote_repository(), 
        regex_branches)