#!/usr/bin/env python3
import os
import utils.message as msg
import sys
import testing.utils.test_helpers as th
from testing.utils.test_processor import init_config
from utils.json_config import Json_config
from testing.utils.test_clean import delete_test_and_repo
from utils.format_text import Format_text as ft
import utils.shell_helpers as shell

def test_processor(conf):
    from testing.tests.test_test_processor import test_test_processor
    conf["tmp"]={"test_name":"test_processor", "opt":"--random-options"}
    test_test_processor(conf)

def new_project(conf):
    delete_test_and_repo(conf)
    from testing.tests.git_helpers.test_new_project import test_new_project
    conf["tmp"]={"test_name":"test_new_project"}
    test_new_project(conf)

def set_new_project(conf):
    set_new_project_again=False
    if not os.path.exists(conf["direpa_test_src"]):
        set_new_project_again=True        
    else:
        # get if set for ssh_url or for local_path
        remote_set_for="local_path"
        user_and_group_root_dir=shell.cmd_get_value("sudo stat --format '%U:%G' '{}'".format(conf["remote"]["direpa_src"]).strip())
        if user_and_group_root_dir != conf["user_current"]+":"+conf["user_current"]:
            remote_set_for="ssh_url"

        if remote_set_for != conf["mode"]:
            set_new_project_again=True

    if set_new_project_again:
        delete_test_and_repo(conf)
        from testing.tests.git_helpers.test_set_new_project import test_set_new_project
        conf["tmp"]={"test_name":"test_set_new_project", "opt":"-d --np"}
        test_set_new_project(conf)

    conf["clean_after"]=True    

def message(conf):
    from testing.tests.utils.test_message import test_message
    conf["tmp"]={"test_name":"test_message"}
    test_message(conf)

def regex_obj(conf):
    from testing.tests.git_helpers.test_regex_obj import test_regex_obj
    conf["tmp"]={"test_name":"test_regex_obj"}
    test_regex_obj(conf)

def remote_repository(conf):
    delete_test_and_repo(conf)
    from testing.tests.git_helpers.test_remote_repository import test_remote_repository
    conf["tmp"]={"test_name":"test_remote_repository"}
    test_remote_repository(conf)

def init_local_config(conf):
    delete_test_and_repo(conf)
    from testing.tests.git_helpers.test_init_local_config import test_init_local_config
    conf["tmp"]={"test_name":"test_init_local_config"}
    test_init_local_config(conf)

def git_utils(conf):
    from testing.tests.git_helpers.test_git_utils import test_git_utils
    set_new_project(conf)
    conf["tmp"]={"test_name":"test_git_utils"}
    test_git_utils(conf)

def version(conf):
    from testing.tests.git_helpers.test_version import test_version
    set_new_project(conf)
    conf["tmp"]={"test_name":"test_version"}
    test_version(conf)

def test_validator(conf):
    from testing.tests.git_helpers.validator.test_check_master_develop_exists import test_check_master_develop_exists
    set_new_project(conf)
    conf["tmp"]={"test_name":"test_check_master_develop_exists"}
    test_check_master_develop_exists(conf)
    
    from testing.tests.git_helpers.validator.test_release_validator import test_release_validator
    set_new_project(conf)
    conf["tmp"]={"test_name":"test_release_validator"}
    test_release_validator(conf)
    
    from testing.tests.git_helpers.validator.test_tags_validator import test_tags_validator
    set_new_project(conf)
    conf["tmp"]={"test_name":"test_tags_validator"}
    test_tags_validator(conf)
   
    from testing.tests.git_helpers.validator.test_version_file_validator import test_version_file_validator
    set_new_project(conf)
    conf["tmp"]={"test_name":"test_version_file_validator"}
    test_version_file_validator(conf)
    
    from testing.tests.git_helpers.validator.test_support_validator import test_support_validator
    set_new_project(conf)
    conf["tmp"]={"test_name":"test_support_validator"}
    test_support_validator(conf)

    from testing.tests.git_helpers.validator.test_hotfix_validator import test_hotfix_validator
    set_new_project(conf)
    conf["tmp"]={"test_name":"test_hotfix_validator"}
    test_hotfix_validator(conf)
    
    from testing.tests.git_helpers.validator.test_hotfix_history_json_validator import test_hotfix_history_json_validator
    set_new_project(conf)
    conf["tmp"]={"test_name":"test_hotfix_history_json_validator"}
    test_hotfix_history_json_validator(conf)

    from testing.tests.git_helpers.test_validator import test_validator
    set_new_project(conf)
    conf["tmp"]={"test_name":"test_validator"}
    test_validator(conf)

def get_all_branch_regexes(conf):
    from testing.tests.git_helpers.test_get_all_branch_regexes import test_get_all_branch_regexes
    set_new_project(conf)
    conf["tmp"]={"test_name":"test_get_all_branch_regexes"}
    test_get_all_branch_regexes(conf)

def synchronize_branch_name(conf):
    from testing.tests.git_helpers.synchronize_branch_name.test_get_value_from_menu import test_get_value_from_menu
    set_new_project(conf)
    conf["tmp"]={"test_name":"test_get_value_from_menu"}
    test_get_value_from_menu(conf)

    from testing.tests.git_helpers.synchronize_branch_name.test_get_branch_on import test_get_branch_on
    set_new_project(conf)
    conf["tmp"]={"test_name":"test_get_branch_on"}
    test_get_branch_on(conf)

    from testing.tests.git_helpers.synchronize_branch_name.test_execute_action import test_execute_action
    set_new_project(conf)
    conf["tmp"]={"test_name":"test_execute_action"}
    test_execute_action(conf)

    from testing.tests.git_helpers.synchronize_branch_name.test_get_branch_compare_status_repository import test_get_branch_compare_status_repository
    set_new_project(conf)
    conf["tmp"]={"test_name":"test_get_branch_compare_status_repository"}
    test_get_branch_compare_status_repository(conf)
    
    from testing.tests.git_helpers.synchronize_branch_name.test_synchronize_local_with import test_synchronize_local_with
    set_new_project(conf)
    conf["tmp"]={"test_name":"test_synchronize_local_with"}
    test_synchronize_local_with(conf)

    from testing.tests.git_helpers.synchronize_branch_name.test_synchronize_branch_name import test_synchronize_branch_name
    set_new_project(conf)
    conf["tmp"]={"test_name":"test_synchronize_branch_name"}
    test_synchronize_branch_name(conf)

def synchronize_branch_type(conf):
    from testing.tests.git_helpers.test_synchronize_branch_type import test_synchronize_branch_type
    set_new_project(conf)
    conf["tmp"]={"test_name":"test_synchronize_branch_type"}
    test_synchronize_branch_type(conf)

def open_branch(conf):
    from testing.tests.git_helpers.branch.test_open_feature import test_open_feature
    set_new_project(conf)
    conf["tmp"]={"test_name":"test_open_feature"}    
    test_open_feature(conf)

    from testing.tests.git_helpers.branch.test_open_support import test_open_support
    set_new_project(conf)
    conf["tmp"]={"test_name":"test_open_support"}    
    test_open_support(conf)

    from testing.tests.git_helpers.branch.test_open_release import test_open_release
    set_new_project(conf)
    conf["tmp"]={"test_name":"test_open_release"}    
    test_open_release(conf)
    
    from testing.tests.git_helpers.branch.test_open_hotfix import test_open_hotfix
    set_new_project(conf)
    conf["tmp"]={"test_name":"open_branch_hotfix"}    
    test_open_hotfix(conf)

def close_branch(conf):
    from testing.tests.git_helpers.branch.test_close_feature import test_close_feature
    set_new_project(conf)
    conf["tmp"]={"test_name":"test_close_feature"}
    test_close_feature(conf)

    from testing.tests.git_helpers.branch.test_close_release import test_close_release
    set_new_project(conf)
    conf["tmp"]={"test_name":"test_close_release"}
    test_close_release(conf)

    from testing.tests.git_helpers.branch.test_close_hotfix import test_close_hotfix
    set_new_project(conf)
    conf["tmp"]={"test_name":"test_close_hotfix"}
    test_close_hotfix(conf)

def get_all_version_tags(conf):
    from testing.tests.git_helpers.test_get_all_version_tags import test_get_all_version_tags
    set_new_project(conf)
    conf["tmp"]={"test_name":"test_get_all_version_tags"}
    test_get_all_version_tags(conf)

def _license(conf):
    from testing.tests.git_helpers.test_license import test_license
    conf["tmp"]={"test_name":"test_license"}
    test_license(conf)

def publish_release(conf):
    from testing.tests.git_helpers.test_publish_release import test_publish_release
    set_new_project(conf)
    conf["tmp"]={"test_name":"test_publish_release"}
    test_publish_release(conf)

def publish_early_release(conf):
    from testing.tests.git_helpers.test_publish_early_release import test_publish_early_release
    set_new_project(conf)
    conf["tmp"]={"test_name":"test_publish_early_release"}
    test_publish_early_release(conf)

def update_branch(conf):
    from testing.tests.git_helpers.test_update_branch import test_update_branch
    set_new_project(conf)
    conf["tmp"]={"test_name":"test_update_branch"}
    test_update_branch(conf)

def main_program_entry(conf):
    from testing.tests.test_main_program_entry import test_main_program_entry
    set_new_project(conf)
    conf["tmp"]={"test_name":"test_main_program_entry"}
    test_main_program_entry(conf)

def create_directory_tree(conf):
    delete_test_and_repo(conf)
    from testing.tests.utils.test_create_directory_tree import test_create_directory_tree
    conf["tmp"]={"test_name":"test_create_directory_tree"}
    test_create_directory_tree(conf)

def clone_project(conf):
    delete_test_and_repo(conf)
    from testing.tests.git_helpers.test_clone_project import test_clone_project
    conf["tmp"]={"test_name":"test_clone_project"}
    test_clone_project(conf)

def test_gitframe(mode):
    if not mode in ["ssh_url", "local_path"]:
        msg.user_error("test_gitframe mode must be 'ssh_url' or 'local_path'.")
        sys.exit(1)

    if not os.environ.get("DISPLAY"):
        msg.user_error("gitframe --test only works with an X session.")
        sys.exit(1)

    main_conf = Json_config().set_value("debug", True)

    conf={
        "launching_window_hex_id": th.get_active_window_hex_id(),
        "mode": mode
    }

    conf.update(init_config(os.path.dirname( os.path.realpath(__file__) )))

    sp=th.Sudo_pass()

    if mode == "ssh_url":
        sp.get_sudo_pass()
        conf["sudo_pass"]=sp.get_sudo_pass()
        th.setup_mock_repository(conf)    
        
    th.enable_sudo(sp)

    ft.clear_scrolling_history()
    th.clean_logs(conf)

    try:
        test_processor(conf)
        
        message(conf)

        regex_obj(conf)

        init_local_config(conf)

        remote_repository(conf)

        delete_test_and_repo(conf)
        clone_project(conf)

        new_project(conf)

        create_directory_tree(conf)

        delete_test_and_repo(conf)
        set_new_project(conf)

        git_utils(conf)

        test_validator(conf)

        get_all_branch_regexes(conf)

        synchronize_branch_name(conf)

        synchronize_branch_type(conf)

        update_branch(conf)

        version(conf)
        
        open_branch(conf)
        
        close_branch(conf)

        get_all_version_tags(conf)

        _license(conf)

        publish_early_release(conf)

        publish_release(conf)

        main_program_entry(conf)
        
        if conf["num_test_failures"] > 0:
            msg.subtitle("Tests Result")
            msg.user_error("Test '"+conf["filen_app"]+"' Failed")
        else:
            msg.subtitle("Tests Result")
            msg.success("Test '"+conf["filen_app"]+"' Succeeded")
    except KeyboardInterrupt:
        print("Program Exited Ctrl+C")
        sys.exit(1)
    except SystemExit:
        msg.subtitle("Tests Result")
        msg.user_error("Predictable Error in "+os.path.basename(__file__))
        msg.user_error("Test '"+conf["filen_app"]+"' Failed")
        sys.exit(1)
    except:
        msg.subtitle("Tests Result")
        msg.app_error("not Predictable Error in "+os.path.basename(__file__))
        msg.user_error("Test '"+conf["filen_app"]+"' Failed")
        sys.exit(1)
    finally:
        conf["current_window_hex_id"]=th.get_active_window_hex_id()
        th.open_logs(conf)
