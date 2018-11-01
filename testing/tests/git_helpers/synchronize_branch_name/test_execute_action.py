#!/usr/bin/env python3
import os, sys
if __name__ != "__main__":
    from testing.utils.test_processor import test_processor, set_test_steps, set_test_vars

def test_execute_action(conf):
    set_test_vars(conf, {
        "direpa_test_src": conf["direpa_test_src"]
    })

    set_test_steps(conf, """
        cd {direpa_test_src}

        {step} exit
        {cmd}
        _out:× Operation cancelled 'synchronize' branch 'master'
        _fail:exit

        {step} ignore
        {cmd}
        _out:∆ Operation ignored 'synchronize' branch 'master'

        {step} pull 
        {cmd}
        _out:√ git pull origin master

        {step} push
        {cmd}
        _out:√ git push origin master

        {step} merge
        {cmd}
        _out:√ git merge --no-edit master

        {step} fetch 
        {cmd}
        _out:√ git fetch origin master
    """)

    test_processor(conf)

if __name__ == "__main__":
    direpa_script=os.path.realpath(__file__)
    while os.path.basename(direpa_script) != "testing":
        direpa_script=os.path.dirname(direpa_script)
    sys.path.insert(0,os.path.dirname(direpa_script))

    from git_helpers.synchronize_branch_name import execute_action
        
    if sys.argv[1] == "exit":
        execute_action("exit", "master")
    
    elif sys.argv[1] == "ignore":
        execute_action("ignore", "master")
    
    elif sys.argv[1] == "pull":
        execute_action("pull", "master")
    
    elif sys.argv[1] == "push":
        execute_action("push", "master")
    
    elif sys.argv[1] == "merge":
        execute_action("merge", "master")

    elif sys.argv[1] == "fetch":
        execute_action("fetch", "master")

