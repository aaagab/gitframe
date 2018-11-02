#!/usr/bin/env python3
import os, sys
from pprint import pprint

if __name__ != "__main__":
    from processor.utils.processor_engine import start_processor, set_task_steps, set_task_vars

def test_hotfix_history_json_validator(conf):
    from utils.json_config import Json_config
    hotfix_json=Json_config().get_value("filen_hotfix_history")    
    
    set_task_vars(conf, {
        "direpa_test_src": conf["direpa_test_src"],
        "commit": "git commit --allow-empty -m \"one commit\"",
        "hotfix_json": hotfix_json,
        "clean_tags": 'git tag | grep -Ev "start_develop|start_master" | xargs git tag -d',
        "reset_master": 'git checkout master; git reset --hard start_master'
    })


    set_task_steps(conf,"""
        cd {direpa_test_src}

        {step} hotfix_history_json_validator no_json_file
        git checkout master
        rm {hotfix_json}
        {cmd}
        _out:× {hotfix_json} should be present on master
        _fail:
        {reset_master}

        {step} hotfix_history_json_validator start_tag_not_found
        git checkout master
        {cmd}
        _out:× start-hotfix-1.0.X-my-repair from hotfix-history.json is not found in git tag
        _fail:
        {reset_master}

        {step} hotfix_history_json_validator end_tag_not_found
        git checkout master
        git tag start-hotfix-1.0.X-my-repair
        {cmd}
        _out:× v1.0.2 from hotfix-history.json is not found in git tag
        _fail:
        {clean_tags}
        {reset_master}

        {step} hotfix_history_json_validator closed_hotfix_with_branch
        git checkout master
        git tag start-hotfix-1.0.X-my-repair
        git tag v1.0.2
        git checkout -b hotfix-1.0.X-my-repair
        {cmd}
        _out:× hotfix-1.0.X-my-repair branch is present whereas it is closed in hotfix-history.json
        _fail:
        {clean_tags}
        git checkout master
        {reset_master}
        git branch -D hotfix-1.0.X-my-repair

        {step} hotfix_history_json_validator open_hotfix_without_branch
        git checkout master
        git tag start-hotfix-1.0.X-my-repair
        {cmd}
        _out:× hotfix-1.0.X-my-repair branch is not present whereas it is open in hotfix-history.json
        _fail:
        {clean_tags}
        {reset_master}

        {step} hotfix_history_json_validator hotfix_without_tag_in_json
        git checkout master
        git tag start-hotfix-1.0.X-my-repair
        git tag v1.0.2
        git checkout -b hotfix-2.0.X-repair-function2
        {cmd}
        _out:× hotfix-2.0.X-repair-function2 branch is present whereas it is not found in one start_tag of its hotfix-history.json
        _fail:
        git checkout master
        git branch -D hotfix-2.0.X-repair-function2
        {clean_tags}
        {reset_master}

        {step} hotfix_history_json_validator success
        git checkout master
        git tag start-hotfix-1.0.X-my-repair
        git tag v1.0.2
        {cmd}
        _out:√ hotfix_history_json_validator
        {clean_tags}
        {reset_master}

        #####################################################
        {step} get_hotfix_tags_from_tags no_tags
        {cmd}
        _out:[]
        {reset_master}

        {step} get_hotfix_tags_from_tags with_tags
        {cmd}
        _out:['v1.1.1', 'start-hotfix-1.0.X-version']
        {reset_master}
      
        ######################################################
        {step} compare_git_tags_to_hotfix_json_tags no_tags
        {cmd}
        _out:∆ no hotfix_tags
        {reset_master}

        {step} compare_git_tags_to_hotfix_json_tags tag_json_empty
        git checkout master
        git checkout -b support-1.0.X
        {cmd}
        _out:× hotfix tags exist [v1.1.1, start-hotfix-1.0.X-version] but no hotfix-history.json has objects in at least one of these branches [master, support-1.0.X]
        _fail:
        {reset_master}
        git branch -D support-1.0.X

        {step} compare_git_tags_to_hotfix_json_tags tag_not_found_in_obj
        git checkout master
        git checkout -b support-1.0.X
        {cmd}
        _out:× [v1.1.1, start-hotfix-1.0.X-version] found in 'git tag' but not in hotfix-history.json in at least one of these branches [master, support-1.0.X]
        _fail:
        {reset_master}
        git branch -D support-1.0.X

        {step} compare_git_tags_to_hotfix_json_tags tags_found_in_json
        git checkout master
        git checkout -b support-1.0.X
        {cmd}
        _out:# master
        _out:# Found >> start-hotfix-1.0.X-version
        _out:# support-1.0.X
        _out:# Found >> v1.1.1
        _out:√ compare_git_tags_to_hotfix_json_tags
        {reset_master}
        git branch -D support-1.0.X

    """)

    start_processor(conf)

if __name__ == "__main__":
    direpa_script=os.path.realpath(__file__)
    while os.path.basename(direpa_script) != "processor":
        direpa_script=os.path.dirname(direpa_script)
    sys.path.insert(0,os.path.dirname(direpa_script))

    import git_helpers.git_utils as git
    from utils.json_config import Json_config
    hotfix_json=Json_config().get_value("filen_hotfix_history")

    data={
        "hotfix-1.0.X-my-repair": {
            "description": "Solving problem 1",
            "end_tag": "v1.0.2",
            "start_tag": "start-hotfix-1.0.X-my-repair",
            "end_commit": "1a609bd4e4ba5091b5977fbaaeacb1a15c253d07",
            "start_commit": "31cef1b34ceb58d4441d360baa4b9d4a352a0c94"
        }
    }

    if sys.argv[1] == "hotfix_history_json_validator":
        from git_helpers.validator.hotfix_history_json import hotfix_history_json_validator 
        from git_helpers.get_all_branch_regexes import get_all_branch_regexes
        from git_helpers.remote_repository import Remote_repository
        repo=Remote_repository()
        regex_branches=get_all_branch_regexes(repo)
                
        if sys.argv[2] == "no_json_file":
            hotfix_history_json_validator(regex_branches)
        elif sys.argv[2] == "start_tag_not_found":
            Json_config(hotfix_json).set_file_with_data(data)
            git.commit("commit")
            hotfix_history_json_validator(regex_branches)
        elif sys.argv[2] == "end_tag_not_found":
            Json_config(hotfix_json).set_file_with_data(data)
            git.commit("commit")
            hotfix_history_json_validator(regex_branches)
        elif sys.argv[2] == "closed_hotfix_with_branch":
            Json_config(hotfix_json).set_file_with_data(data)
            git.commit("commit")
            hotfix_history_json_validator(regex_branches)
        elif sys.argv[2] == "open_hotfix_without_branch":
            data["hotfix-1.0.X-my-repair"]["end_tag"]=""            
            data["hotfix-1.0.X-my-repair"]["end_commit"]=""            
            Json_config(hotfix_json).set_file_with_data(data)
            git.commit("commit")
            hotfix_history_json_validator(regex_branches)
        elif sys.argv[2] == "hotfix_without_tag_in_json":
            Json_config(hotfix_json).set_file_with_data(data)
            git.commit("commit")
            hotfix_history_json_validator(regex_branches)
        elif sys.argv[2] == "success":
            Json_config(hotfix_json).set_file_with_data(data)
            git.commit("commit")
            hotfix_history_json_validator(regex_branches)

    elif sys.argv[1] == "get_hotfix_tags_from_tags":
        from git_helpers.validator.hotfix_history_json import get_hotfix_tags_from_tags
        if sys.argv[2] == "no_tags":
            print(get_hotfix_tags_from_tags([]))
        elif sys.argv[2] == "with_tags":
            print(get_hotfix_tags_from_tags(["v2.1.0","v1.1.1","start-hotfix-1.0.X-version"]))

    elif sys.argv[1] == "compare_git_tags_to_hotfix_json_tags":
        from git_helpers.validator.hotfix_history_json import compare_git_tags_to_hotfix_json_tags 
        import git_helpers.regex_obj as ro
        if sys.argv[2] == "no_tags":
            compare_git_tags_to_hotfix_json_tags(
                [
                    ro.Master_regex("master"),
                ], 
                [], 
                hotfix_json
            )

        elif sys.argv[2] == "tag_json_empty":
            compare_git_tags_to_hotfix_json_tags(
                [
                    ro.Master_regex("master"),
                    ro.Support_regex("support-1.0.X")
                ], 
                ['v1.1.1', 'start-hotfix-1.0.X-version'], 
                hotfix_json
            )

        elif sys.argv[2] == "tag_not_found_in_obj":
            Json_config(hotfix_json).set_file_with_data(data)
            git.commit("commit")
            compare_git_tags_to_hotfix_json_tags(
                [
                    ro.Master_regex("master"),
                    ro.Support_regex("support-1.0.X")
                ], 
                ['v1.1.1', 'start-hotfix-1.0.X-version'], 
                hotfix_json
            )
        elif sys.argv[2] == "tags_found_in_json":
            data["hotfix-1.0.X-my-repair"]["end_tag"]="v1.1.1"
            Json_config(hotfix_json).set_file_with_data(data)
            git.commit("commit")

            git.checkout("master")
            data["hotfix-1.0.X-my-repair"]["end_tag"]="v1.0.2"
            data["hotfix-1.0.X-my-repair"]["start_tag"]="start-hotfix-1.0.X-version"
            Json_config(hotfix_json).set_file_with_data(data)
            git.commit("commit")

            compare_git_tags_to_hotfix_json_tags(
                [
                    ro.Master_regex("master"),
                    ro.Support_regex("support-1.0.X")
                ], 
                ['v1.1.1', 'start-hotfix-1.0.X-version'], 
                hotfix_json
            )