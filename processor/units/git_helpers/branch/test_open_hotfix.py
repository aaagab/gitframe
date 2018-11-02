#!/usr/bin/env python3
import os, sys
if __name__ != "__main__":
    from processor.utils.processor_engine import start_processor, set_task_steps, set_task_vars

def test_open_hotfix(conf):
    set_task_vars(conf, {
        "direpa_test_src": conf["direpa_test_src"],
        "clean_tag": 'git tag | grep -Ev "start_develop|start_master" | xargs git tag -d',
        "commit": "git commit --allow-empty -m 'empty_commit'",
        "hotfix_branch": "hotfix-1.0.X-my_repair"
    })

    set_task_steps(conf,"""
        cd {direpa_test_src}
        
        {step} get_tag_for_hotfix
        {cmd}
        _out:Choose a release From Where To branch The Hotfix.
        _out:choice or 'q' to quit:
        _type:2
        _out:2.1.0

        {step} get_hotfix_obj closed_hotfix
        {cmd}
        _out:Do you want to Duplicate a previous Hotfix? [y/N/q]: 
        _type:y
        _out:choice or 'q' to quit: 
        _type:1
        _out:{hotfix_branch}

        {step} get_hotfix_obj no_closed_hotfix
        {cmd}
        _out:No hotfixes closed

        {step} get_diff_between_commits no_start_commit
        {cmd}
        _out:× Start commit: 5d5fd7df8cb675791b0e581b8526b2ea86134ad5 does not exist. Can't get diff between two commits.
        _fail:

        {step} get_diff_between_commits no_end_commit
        {cmd}
        # _out:× End commit: 5d5fd7df8cb675791b0e581b8526b2ea86134ad5 does not exist. Can't get diff between two commits.
        _fail:

        {step} get_diff_between_commits diff_file_content
        git checkout master
        echo "content" > file.txt
        git add .; git commit -a -m "added file.txt"
        git tag added_file
        {cmd}
        _out:√ diff_file has content
        git reset --hard start_master

        {step} get_diff_between_commits diff_file_no_content
        {cmd}
        _fail:

        {step} open_hotfix no_tags
        {cmd} 
        _out:× There are no tags in this project. You can't open a Hotfix Branch
        _fail:

        {step} open_hotfix no_hotfix_obj_no_tag_support_has_latest_release_tag
        git checkout master
        git tag v1.0.0
        {cmd} 
        _out:choice or 'q' to quit: 
        _type: 1
        _out:Type Few Keywords For new hotfix branch name [q to quit]:
        _type: my repair
        _out:Add Description For {hotfix_branch} [q to quit]:
        _type: this is the repair for 1.0.0 release
        _out:# hotfix from latest release

        {step} open_hotfix has_hotfix_obj_has_related_support
        {dep} open_hotfix no_hotfix_obj_no_tag_support_has_latest_release_tag
        {commit}
        git tag -a "v1.0.1" -m "hotfix"
        git checkout master
        git checkout -b support-1.0.X
        # Normally you can't have a support branch on latest release but for the test out of context of the validator it works
        git checkout {hotfix_branch}
        {cmd}
        _out:choice or 'q' to quit:
        _type:1
        _out:Do you want to Duplicate a previous Hotfix? [y/N/q]:
        _type:y
        _out:choice or 'q' to quit:
        _type:1
        _out:Type Few Keywords For new hotfix branch name [q to quit]:
        _type: my repair another branch
        _out:# hotfix from existing support branch
        git checkout master
        git reset --hard start_master
        {clean_tag}
        git branch -D support-1.0.X

        {step} open_hotfix no_hotfix_obj_no_tag_support_not_latest_release_tag
        git checkout master
        {commit}
        git tag v1.1.0
        {commit}
        git tag v2.1.0
        {cmd}
        _out:choice or 'q' to quit:
        _type:1
        _out:Type Few Keywords For new hotfix branch name [q to quit]:
        _type:again a repair
        _out:Add Description For hotfix-1.1.X-again_a_repair [q to quit]:
        _type: this is a repair that is done on previous release, so a support branch is also created
        _out:# hotfix from new support branch
        _out:√ git checkout -b support-1.1.X v1.1.0
        _out:√ git checkout -b hotfix-1.1.X-again_a_repair support-1.1.X

        {step} create_json_data_hotfix json_empty
        git checkout master
        git tag start-{hotfix_branch}
        {cmd}
        {clean_tag}

        {step} create_json_data_hotfix json_with_different_entry
        git checkout master
        git tag start-{hotfix_branch}
        {cmd}
        {clean_tag}

      
    """)

    start_processor(conf)

if __name__ == "__main__":
    direpa_script=os.path.realpath(__file__)
    while os.path.basename(direpa_script) != "processor":
        direpa_script=os.path.dirname(direpa_script)
    sys.path.insert(0,os.path.dirname(direpa_script))

    from pprint import pprint

    data={
        "hotfix-2.0.X-my_repair": {
            "description": "This is my new great hotfix",
            "end_commit": "5d5fd7df8cb675791b0e581b8526b2ea86134ad5",
            "end_tag": "v2.0.3",
            "start_commit": "5d5fd7df8cb675791b0e581b8526b2ea86134ad5",
            "start_tag": "start-hotfix-2.0.X-my_repair"
        },
        "hotfix-1.0.X-my_repair": {
            "description": "This is my new great hotfix",
            "end_commit": "5d5fd7df8cb675791b0e581b8526b2ea86134ad5",
            "end_tag": "v1.0.2",
            "start_commit": "5d5fd7df8cb675791b0e581b8526b2ea86134ad5",
            "start_tag": "start-hotfix-1.0.X-my_repair"
        }
    }

    if sys.argv[1] == "get_tag_for_hotfix":
        from git_helpers.branch.hotfix import get_tag_for_hotfix
        print(get_tag_for_hotfix(['1.0.0', '1.1.0', '1.2.0', '2.0.0', '2.1.0', '3.0.0', '3.1.0']))

    elif sys.argv[1] == "get_hotfix_obj":
        from git_helpers.branch.hotfix import get_hotfix_obj
        if sys.argv[2] == "closed_hotfix":
            get_hotfix_obj(data)
        elif sys.argv[2] == "no_closed_hotfix":
            data["hotfix-1.0.X-my_repair"]["end_commit"]=""
            data["hotfix-1.0.X-my_repair"]["end_tag"]=""
            data["hotfix-2.0.X-my_repair"]["end_commit"]=""
            data["hotfix-2.0.X-my_repair"]["end_tag"]=""
            get_hotfix_obj(data)

    elif sys.argv[1] == "get_diff_between_commits":
        from git_helpers.branch.hotfix import get_diff_between_commits
        import utils.shell_helpers as shell
        if sys.argv[2] == "no_start_commit":
            fake_commit="5d5fd7df8cb675791b0e581b8526b2ea86134ad5"
            get_diff_between_commits(
                fake_commit,
                shell.cmd_get_value("git rev-list -n1 start_develop")
            )
        elif sys.argv[2] == "no_end_commit":
            fake_commit="5d5fd7df8cb675791b0e581b8526b2ea86134ad5"
            get_diff_between_commits(
                shell.cmd_get_value("git rev-list -n1 start_master"),
                fake_commit
            )
        elif sys.argv[2] == "diff_file_content":
            print(get_diff_between_commits(
                shell.cmd_get_value("git rev-list -n1 start_master"),
                shell.cmd_get_value("git rev-list -n1 added_file")
            ))

        elif sys.argv[2] == "diff_file_no_content":
            print(get_diff_between_commits(
                shell.cmd_get_value("git rev-list -n1 start_master"),
                shell.cmd_get_value("git rev-list -n1 start_develop")
            ))
        


    elif sys.argv[1] == "open_hotfix":
        from git_helpers.remote_repository import Remote_repository
        from git_helpers.branch.hotfix import open_hotfix
        import git_helpers.git_utils as git

        from git_helpers.get_all_branch_regexes import get_all_branch_regexes
        from git_helpers.remote_repository import Remote_repository
        from git_helpers.get_all_version_tags import get_all_version_tags
        repo=Remote_repository()


        if sys.argv[2] == "no_tags":
            open_hotfix(repo, get_all_version_tags())
        
        elif sys.argv[2] == "no_hotfix_obj_no_tag_support_has_latest_release_tag":
            from utils.json_config import Json_config
            fname=Json_config().get_value("filen_hotfix_history")
            open_hotfix(repo, get_all_version_tags())
            os.system("cat "+fname)
            
        elif sys.argv[2] == "has_hotfix_obj_has_related_support":
            from utils.json_config import Json_config
            fname=Json_config().get_value("filen_hotfix_history")
            data=Json_config(fname).data
            data["hotfix-1.0.X-my_repair"]["end_commit"]=git.get_commit_from_tag("v1.0.1")
            data["hotfix-1.0.X-my_repair"]["end_tag"]="v1.0.1"
            Json_config(fname).set_file_with_data(data)
            os.system("git add .")
            os.system("git commit -a -m 'history.json modified'")
            os.system("git checkout master")
            os.system("git  master")
            git.merge_noff("hotfix-1.0.X-my_repair")
            open_hotfix(repo, get_all_version_tags())
        
        elif sys.argv[2] == "no_hotfix_obj_no_tag_support_not_latest_release_tag":
            open_hotfix(repo, get_all_version_tags())

    elif sys.argv[1] == "create_json_data_hotfix":
        from git_helpers.branch.hotfix import create_json_data_hotfix
        from utils.json_config import Json_config
        fname=Json_config().get_value("filen_hotfix_history")
        description="This is my great hotfix"

        os.system("cat "+fname)
        
        if sys.argv[2] == "json_empty":
            create_json_data_hotfix("hotfix-1.0.X-my_repair", description, fname)
            os.system("cat "+fname)
            os.system("echo {} > "+fname)
        elif sys.argv[2] == "json_with_different_entry":
            data={
                "hotfix-2.0.X-my-new-repair": {
                    "description": "This is another great hotfix",
                    "end_commit": "",
                    "end_tag": "",
                    "start_commit": "5d5fd7df8cb675791b0e581b8526b2ea86134ad5",
                    "start_tag": "start-hotfix-1.0.X-my_repair"
                }
            }
            Json_config(fname).set_file_with_data(data)
            create_json_data_hotfix("hotfix-1.0.X-my_repair", description, fname)
            os.system("cat "+fname)
            os.system("echo {} > "+fname)
	