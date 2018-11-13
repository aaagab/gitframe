#!/usr/bin/env python3
import os, sys
if __name__ != "__main__":
    from processor.utils.processor_engine import start_processor, set_task_steps, set_task_vars
    from utils.json_config import Json_config
    
def test_clone_project(conf):
    # from pprint import pprint
    # pprint(conf)

    set_task_vars(conf, {
        "direpa_remote_src": conf["remote"]["direpa_src"],
        "direpa_par_remote_src": conf["remote"]["direpa_par_src"],
        "direpa_task_src": conf["direpa_task_src"],
        "direpa_task": conf["direpa_task"],
        "direpa_repository": conf["direpa_repository"],
        "diren_task": conf["diren_task"],
        "diren_src": conf["diren_src"],
        "ssh_url_domain_direpa_src": conf["remote"]["ssh_url_domain_direpa_src"],
        "scp_url_domain_direpa_par_src": conf["remote"]["scp_url_domain_direpa_par_src"],
        "direpa_task_conf": conf["direpa_task_conf"],
        "user_ssh": conf["user_current"],
        "user_git": conf["remote"]["user_git"],
        "domain": conf["remote"]['domain'],
        "sudo_pass": conf.get("sudo_pass"),
        "block_init_repo":"""
            mkdir -p {direpa_task_src}
            cd {direpa_task_src}
            git init .
            touch myfile.txt
            git add .
            git -c user.name='user_name' -c user.email='test@test.com' commit -am "myfile"
            mkdir -p {direpa_par_remote_src}
        """,
        "block_user_input": """
            _out:Enter user name [q to quit]:
            _type:user_name
            _out:Enter user email [q to quit]:
            _type:test@test.com
            _out:Enter origin repository [q to quit]:
        """    
    })

    if conf["task_mode"] == "local_path":
        set_task_steps(conf,"""
            {step} clone_project_to_remote directory existing
            {block_init_repo}
            {cmd}
            {block_user_input}
            _type:{direpa_remote_src}
            _out:√ Remote Path '{direpa_par_remote_src}' is reachable.
            _out:∆ Remote Repository '{direpa_remote_src}' does not exist.
            _out:# repo is a directory
            # # _out:√ git clone --bare src {direpa_remote_src}
            rm -rf {direpa_task}
            rm -rf {direpa_repository}

        """)
    elif conf["task_mode"] == "ssh_url":
        set_task_steps(conf,"""
            {step} clone_project_to_remote url
            {block_init_repo}
            {cmd}
            {block_user_input}
            _type:{ssh_url_domain_direpa_src}
            _out:Type ssh username [q to quit]:
            _type:{user_ssh}
            _out:√ git clone --bare {direpa_task_src} {direpa_task_src}.git
            _out:{user_ssh}@{domain}'s password:
            _type:{sudo_pass}
            _out:√ scp -r {direpa_task_src}.git {scp_url_domain_direpa_par_src}
            _out:{user_ssh}@{domain}'s password:
            _type:{sudo_pass}
            _out:[sudo] password for {user_ssh}:
            _type:{sudo_pass}
            _out:√ ssh -t {user_ssh}@{domain} "sudo chown -R {user_git}:{user_git} {direpa_remote_src}"
            _out:√ {direpa_task_src}.git deleted on local.
            rm -rf {direpa_task_conf}/{diren_task}
            sudo rm -rf {direpa_repository}
            _out:[sudo] password for {user_ssh}:
            _type:{sudo_pass}
        """)
    

    start_processor(conf)

if __name__ == "__main__":
    direpa_script=os.path.realpath(__file__)
    while os.path.basename(direpa_script) != "processor":
        direpa_script=os.path.dirname(direpa_script)
    sys.path.insert(0,os.path.dirname(direpa_script))

    from git_helpers.clone_project_to_remote import clone_project_to_remote
    from git_helpers.remote_repository import Remote_repository

    if sys.argv[1] == "clone_project_to_remote":
        clone_project_to_remote(Remote_repository())
      