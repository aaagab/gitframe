#!/usr/bin/env python3
import os, sys
if __name__ != "__main__":
    from testing.utils.test_processor import test_processor, set_test_steps, set_test_vars

def test_version(conf):
    # from pprint import pprint
    # pprint(conf)
    set_test_vars(conf, {
        "direpa_test_src": conf["direpa_test_src"],
    })

    set_test_steps(conf,"""
        cd {direpa_test_src}

        {step} bump_version_in_version_txt
        git checkout master
        {cmd}
        _out:1.2.3
        git reset --hard start_master

        {step} get_content_version_file file_not_found
        {cmd}
        _out:× 'version.txt' not found on branch 'master'.
        
        {step} get_content_version_file file_empty
        git checkout master
        echo '' > version.txt
        git add .; git commit -a -m "bump version"
        {cmd}
        _out:× 'version.txt' is empty on branch 'master'.
        git reset --hard start_master

        {step} get_content_version_file from_master
        git checkout master
        echo 2.3.4 > version.txt
        git add .; git commit -a -m "bump version"
        {cmd}
        _out:2.3.4
        git reset --hard start_master

         {step} get_content_version_file success
        git checkout master
        echo 4.4.4 > version.txt
        git add .; git commit -a -m "bump version"
        {cmd}
        _out:4.4.4
        git reset --hard start_master

        {step} increment_version_value major_minor_patch
        {cmd}
        _out:4.0.0
        _out:3.3.0
        _out:3.2.2

        {step} execute_bump_release_version
        {cmd}
        _out:3.2.1

    """)

    test_processor(conf)

if __name__ == "__main__":
    direpa_script=os.path.realpath(__file__)
    while os.path.basename(direpa_script) != "testing":
        direpa_script=os.path.dirname(direpa_script)
    sys.path.insert(0,os.path.dirname(direpa_script))

    if sys.argv[1] == "bump_version_in_version_txt":
        from git_helpers.version import bump_version_in_version_txt
        bump_version_in_version_txt("1.2.3")
        os.system("cat version.txt")
    elif sys.argv[1] == "get_content_version_file":
        from git_helpers.version import get_content_version_file
        if sys.argv[2] in ["file_not_found", "file_empty"]:
            print(get_content_version_file(True))
        elif sys.argv[2] == "from_master":
            print(get_content_version_file(False, "master"))
        elif sys.argv[2] == "success":
            print(get_content_version_file())
    elif sys.argv[1] == "increment_version_value":
        from git_helpers.version import increment_version_value
        import git_helpers.regex_obj as ro
        print(increment_version_value("major", ro.Version_regex("3.2.1")))
        print(increment_version_value("minor", ro.Version_regex("3.2.1")))
        print(increment_version_value("patch", ro.Version_regex("3.2.1")))
    elif sys.argv[1] == "execute_bump_release_version":
        from git_helpers.version import bump_version_for_user
        bump_version_for_user("3.2.1")
    