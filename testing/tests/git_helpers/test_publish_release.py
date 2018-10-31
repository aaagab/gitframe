#!/usr/bin/env python3
import os, sys
if __name__ != "__main__":
    from testing.utils.test_processor import test_processor, set_test_steps, set_test_vars

def test_publish_release(conf):
    set_test_vars(conf, {
        "direpa_test_src": conf["direpa_test_src"],
        "direpa_test": conf["direpa_test"],
    })

    set_test_steps(conf, """
        cd {direpa_test_src}
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

        mkdir -p {direpa_test}/scripts
        echo '#!/bin/bash' > {direpa_test}/scripts/deploy_release.sh
        echo 'echo $1' >> {direpa_test}/scripts/deploy_release.sh
        echo 'echo $2' >> {direpa_test}/scripts/deploy_release.sh
        chmod +x {direpa_test}/scripts/deploy_release.sh

        {cmd}
        _out:# launch script deploy_release
        _out:1.0.1
    """)
            
    test_processor(conf)

if __name__ == "__main__":
    direpa_script=os.path.realpath(__file__)
    while os.path.basename(direpa_script) != "src":
        direpa_script=os.path.dirname(direpa_script)
    sys.path.insert(0,direpa_script)

    from git_helpers.publish_release import publish_release
    from git_helpers.get_all_version_tags import get_all_version_tags
    

    publish_release("1.0.1", get_all_version_tags())
