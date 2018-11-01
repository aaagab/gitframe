#!/usr/bin/env python3
import os, sys
if __name__ != "__main__":
    from testing.utils.test_processor import test_processor, set_test_steps, set_test_vars

def test_get_branch_on(conf):
    set_test_vars(conf, {
        "direpa_test_src": conf["direpa_test_src"],
    })

    set_test_steps(conf, """
        cd {direpa_test_src}

        {step} online_and_local_and_local_remote_and_remote
        git checkout -b test
        git push origin test
        {cmd}
        _out:# branch_on True_True_True

        {step} online_and_local_and_local_remote_and_not_remote
        cp -r {direpa_test_src} {direpa_test_src}_tmp
        cd {direpa_test_src}_tmp
        git push origin --delete test
        cd {direpa_test_src}
        {cmd}
        _out:# branch_on True_True_False

        {step} online_and_local_and_not_local_remote_and_remote
        git push origin test
        git branch -rD origin/test        
        {cmd}
        _out:# branch_on True_False_True

        {step} online_and_local_and_not_local_remote_and_not_remote
        git push origin --delete test
        {cmd}
        _out:# branch_on True_False_False

        {step} online_and_not_local_and_local_remote_and_remote
        git push origin test
        git checkout develop
        git branch -D test
        {cmd}
        _out:# branch_on False_True_True

        {step} online_and_not_local_and_local_remote_and_not_remote
        cd {direpa_test_src}_tmp
        git push origin --delete test
        cd {direpa_test_src}
        {cmd}
        _out:# branch_on False_True_False

        {step} online_and_not_local_and_not_local_remote_and_remote
        git checkout test
        git push origin test
        git checkout develop
        git branch -D test
        git branch -rD origin/test
        {cmd}
        _out:# branch_on False_False_True

        {step} online_and_not_local_and_not_local_remote_and_not_remote
        git push origin --delete test
        {cmd}
        _out:# branch_on False_False_False

        {step} offline_and_local_and_local_remote_and_not_remote
        git checkout -b test
        git push origin test
        cd {direpa_test_src}_tmp
        git push origin --delete test
        cd {direpa_test_src}
        {cmd}
        _out:# branch_on True_True_False

        {step} offline_and_local_and_not_local_remote_and_not_remote
        git branch -rD origin/test
        {cmd}
        _out:# branch_on True_False_False

        {step} offline_and_not_local_and_local_remote_and_not_remote
        git push origin test
        git checkout develop
        git branch -D test
        {cmd}
        _out:# branch_on False_True_False

        {step} offline_and_not_local_and_not_local_remote_and_not_remote
        git branch -rD origin/test
        {cmd}
        _out:# branch_on False_False_False

        rm -rf {direpa_test_src}_tmp

    """)
    test_processor(conf)

if __name__ == "__main__":
    direpa_script=os.path.realpath(__file__)
    while os.path.basename(direpa_script) != "testing":
        direpa_script=os.path.dirname(direpa_script)
    sys.path.insert(0,os.path.dirname(direpa_script))

    from git_helpers.synchronize_branch_name import get_branch_on

    class Remote_repository():
        def __init__(self):
            self.is_reachable=True

    repo=Remote_repository()
        
    if sys.argv[1] == "online_and_local_and_local_remote_and_remote":
        print(get_branch_on(repo, "test"))

    if sys.argv[1] == "online_and_local_and_local_remote_and_not_remote":
        print(get_branch_on(repo, "test"))

    if sys.argv[1] == "online_and_local_and_not_local_remote_and_remote":
        print(get_branch_on(repo, "test"))

    if sys.argv[1] == "online_and_local_and_not_local_remote_and_not_remote":
        print(get_branch_on(repo, "test"))

    if sys.argv[1] == "online_and_not_local_and_local_remote_and_remote":
        print(get_branch_on(repo, "test"))

    if sys.argv[1] == "online_and_not_local_and_local_remote_and_not_remote":
        print(get_branch_on(repo, "test"))

    if sys.argv[1] == "online_and_not_local_and_not_local_remote_and_remote":
        print(get_branch_on(repo, "test"))

    if sys.argv[1] == "online_and_not_local_and_not_local_remote_and_not_remote":
        print(get_branch_on(repo, "test"))

    repo.is_reachable=False
    if sys.argv[1] == "offline_and_local_and_local_remote_and_not_remote":
        print(get_branch_on(repo, "test"))

    if sys.argv[1] == "offline_and_local_and_not_local_remote_and_not_remote":
        print(get_branch_on(repo, "test"))

    if sys.argv[1] == "offline_and_not_local_and_local_remote_and_not_remote":
        print(get_branch_on(repo, "test"))

    if sys.argv[1] == "offline_and_not_local_and_not_local_remote_and_not_remote":
        print(get_branch_on(repo, "test"))
