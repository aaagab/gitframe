#!/usr/bin/env python3
import os, sys
if __name__ != "__main__":
    from testing.utils.test_processor import test_processor, set_test_steps, set_test_vars
    from utils.json_config import Json_config
    
def test_new_project(conf):
    # from pprint import pprint
    # pprint(conf)

    set_test_vars(conf, {
        "direpa_remote_src": conf["remote"]["direpa_src"],
        "direpa_par_remote_src": conf["remote"]["direpa_par_src"],
        "direpa_testgf": conf["direpa_testgf"],
        "direpa_test": conf["direpa_test"],
        "direpa_test_src": conf["direpa_test_src"],
        "direpa_repository": conf["direpa_repository"],
        "diren_src": conf["diren_src"],
        "block_user_input": """
            _out:Do you want to create directory? [Y/n/q]:
            _type:y 
            _out:√ Path '{direpa_testgf}/test' created.
            _out:Enter user name [q to quit]:
            _type:user_name
            _out:Enter user email [q to quit]:
            _type:test@test.com
            _out:Enter origin repository [q to quit]:
            _type:{direpa_remote_src}
            _out:Do you Want To Add a License [Y/n/q]:
            _type:Y
            _out:choice or 'q' to quit:
            _type:1
            _out:Copyright Holders:  [q to quit]:
            _type:Thomas Edison
        """    
    })

    set_test_steps(conf,"""
        mkdir -p "repository/src"

        {step} test_path_is_not_file file
        touch {direpa_testgf}/file.txt
        {cmd}
        _out:× Path '{direpa_testgf}/file.txt' is not a directory.
        _fail:
        rm {direpa_testgf}/file.txt

        {step} test_path_is_not_file directory
        {cmd}

        {step} test_path_syntax space
        {cmd}
        _fail: space in path

        {step} test_path_syntax hash
        {cmd}
        _fail: hash in path

        {step} test_path_syntax conform
        {cmd}

        {step} create_directory success
        {cmd}
        _out:Do you want to create directory? [Y/n/q]:
        _type:Y
        _out:√ Path '{direpa_testgf}/draft' created.
        rm -rf draft

        {step} create_directory fail
        mkdir draft
        {cmd}
        _out:Do you want to create directory? [Y/n/q]:
        _type:Y
        _out:× cannot create path '{direpa_testgf}/draft'
        _fail:
        rm -rf draft

        {step} test_file_not_exist
        touch draft.txt
        {cmd}
        _out:× File '{direpa_testgf}/draft.txt' already exists.
        _fail:
        rm draft.txt

        {step} new_project empty_path_exists has_git
        mkdir -p "mock_project"
        cd "mock_project"
        touch file1.txt
        touch file2.txt
        git init
        {cmd}
        _out:# path exists
        _out:× Current Path '{direpa_testgf}/mock_project' has a .git directory
        _fail:
        cd {direpa_testgf}
        rm -rf mock_project

        {step} new_project empty_path_exists no_git
        mkdir -p "mock_project"
        cd "mock_project"
        touch file1.txt
        touch file2.txt
        {cmd}
        _out:Path '{direpa_testgf}/mock_project' already exists, Do you want to add git to directory anyway? [Y/n/q]:
        _type:n
        _fail:
        cd {direpa_testgf}
        rm -rf mock_project

        {step} new_project empty_path_exists repo_has_directory
        mkdir -p "mock_project"
        cd "mock_project"
        touch file1.txt
        touch file2.txt
        mkdir -p {direpa_remote_src}
        cd {direpa_remote_src}
        git init .
        cd -
        {cmd}
        _out:Path '{direpa_testgf}/mock_project' already exists, Do you want to add git to directory anyway? [Y/n/q]:
        _type:Y
        _out:Enter user name [q to quit]:
        _type:user_name
        _out:Enter user email [q to quit]:
        _type:test@test.com
        _out:Enter origin repository [q to quit]:
        _type:{direpa_remote_src}
        _out:Do you Want To Add a License [Y/n/q]:
        _type:Y
        _out:choice or 'q' to quit:
        _type:1
        _out:Copyright Holders:  [q to quit]:
        _type:Thomas Edison
        _out:× Remote Directory mock_project.git Already Exists on remote repository 'Origin'
        _out:# directory 'mock_project' cleaned.
        _fail:
        cd {direpa_testgf}
        rm -rf mock_project

        {step} new_project abs_path_not_exist no_parent_directory
        {cmd}
        _out:# path is absolute
        _out:× Path parent directory '{direpa_testgf}/marty' does not exist.        
        _fail:

        {step} new_project relative_path_not_exist reachable_with_directory
        mkdir -p {direpa_remote_src}
        {cmd}
        {block_user_input}
        _out:× Remote Directory test.git Already Exists on remote repository 'Origin'
        _out:× Clone test.git from Remote or Change application name
        _out:# directory 'test' cleaned.
        _fail:
        rm -rf {direpa_remote_src}

        {step} new_project relative_path_not_exist not_reachable
        {cmd}
        _out:Do you want to create directory? [Y/n/q]:
        _type:y 
        _out:√ Path '{direpa_testgf}/test' created.
        _out:Enter user name [q to quit]:
        _type:user_name
        _out:Enter user email [q to quit]:
        _type:test@test.com
        _out:Enter origin repository [q to quit]:
        _type:/tmp/unknown/test/src.git
        _out:Do you Want To Add a License [Y/n/q]:
        _type:Y
        _out:choice or 'q' to quit:
        _type:1
        _out:Copyright Holders:  [q to quit]:
        _type:Thomas Edison
        _out:∆ Remote Path '/tmp/unknown/test' is not reachable.
        _out:∆ Remote Repository '/tmp/unknown/test/src.git' may not exist.
        _out:∆ Clone your project when connectivity is back.
        _out:√ New Project test initialized.
        rm -rf {direpa_repository}
        rm -rf {direpa_test}

        {step} new_project relative_path_not_exist reachable
        mkdir -p {direpa_par_remote_src}
        {cmd}
        _out:Do you want to create directory? [Y/n/q]:
        _type:y 
        _out:√ Path '{direpa_testgf}/test' created.
        _out:Enter user name [q to quit]:
        _type:user_name
        _out:Enter user email [q to quit]:
        _type:test@test.com
        _out:Enter origin repository [q to quit]:
        _type:{direpa_remote_src}
        _out:Do you Want To Add a License [Y/n/q]:
        _type:Y
        _out:choice or 'q' to quit:
        _type:1
        _out:Copyright Holders:  [q to quit]:
        _type:Thomas Edison
        _out:√ Remote Path '{direpa_par_remote_src}' is reachable.
        _out:∆ Remote Repository '{direpa_remote_src}' does not exist.
        _out:√ git clone --bare {direpa_test_src} {direpa_remote_src}
        _out:√ New Project test initialized.
        rm -rf {direpa_repository}
        rm -rf {direpa_test}
    """)

    test_processor(conf)

if __name__ == "__main__":
    direpa_script=os.path.realpath(__file__)
    while os.path.basename(direpa_script) != "testing":
        direpa_script=os.path.dirname(direpa_script)
    sys.path.insert(0,os.path.dirname(direpa_script))

    from git_helpers.new_project import new_project
    from git_helpers.remote_repository import Remote_repository

    from utils.json_config import Json_config
    from pprint import pprint
    conf=Json_config().data
    
    if sys.argv[1] == "new_project":
        if sys.argv[2] == "empty_path_exists":
            new_project()
        elif sys.argv[2] == "abs_path_not_exist":
            conf=Json_config().data
            abs_path=os.path.join(conf["test"]["direpa_root"], "marty", "future")
            new_project(abs_path)
        elif sys.argv[2] == "relative_path_not_exist":
            conf=Json_config().data
            # print(conf["test"]["direpa_root"])
            # abs_path=os.path.join(conf["test"]["direpa_root"], "draft")
            new_project("test")      
    elif sys.argv[1] == "test_path_is_not_file":
        from git_helpers.new_project import test_path_is_not_file
        if sys.argv[2] == "file":
            test_path_is_not_file(os.path.join(conf["test"]["direpa_root"], "file.txt"))      
        elif sys.argv[2] == "directory":
            test_path_is_not_file(conf["test"]["direpa_root"])      
    elif sys.argv[1] == "test_path_syntax":
        from git_helpers.new_project import test_path_syntax
        if sys.argv[2] == "space":
            test_path_syntax("/my path/withspaces")      
        elif sys.argv[2] == "hash":
            test_path_syntax("#mypath")      
        elif sys.argv[2] == "conform":
            test_path_syntax("mypath-_1234./other/directory")      
    elif sys.argv[1] == "create_directory":
        from utils.json_config import Json_config
        conf=Json_config().data
        
        from git_helpers.new_project import create_directory
        create_directory(os.path.join(conf["test"]["direpa_root"],"draft"))
    elif sys.argv[1] == "test_file_not_exist":
        from utils.json_config import Json_config
        conf=Json_config().data
        
        from git_helpers.new_project import test_file_not_exist
        test_file_not_exist(os.path.join(conf["test"]["direpa_root"],"draft.txt"))

