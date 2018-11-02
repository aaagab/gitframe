#!/usr/bin/env python3
import os
if __name__ != "__main__":
    from testing.utils.test_processor import test_processor, set_test_steps, set_test_vars
    from utils.json_config import Json_config
    
    import sys

def test_set_new_project(conf):
    # from pprint import pprint
    # pprint(conf)

    set_test_vars(conf, {
        "direpa_remote_src": conf["remote"]["direpa_src"],
        "direpa_par_remote_src": conf["remote"]["direpa_par_src"],
        "direpa_test": conf["direpa_test"],
        "direpa_scripts": conf["direpa_scripts"],
        "filenpa_bump_release_version": conf["filenpa_bump_release_version"],
        "direpa_test_src": conf["direpa_test_src"],
        'this_cmd':conf["direpa_app"]+"/"+conf["filen_app"]+" "+conf["tmp"]["opt"]+" "+conf["diren_test"],
        "ssh_url_domain_direpa_src": conf["remote"]["ssh_url_domain_direpa_src"],
        "scp_url_domain_direpa_par_src": conf["remote"]["scp_url_domain_direpa_par_src"],
        "user_git": conf["remote"]["user_git"],
        "user_current": conf["user_current"],
        "domain": conf["remote"]["domain"],
        "diren_src": conf["diren_src"],
        "sudo_pass": conf.get("sudo_pass"),
        "block_input_create_directory": """
            _out:Do you want to create directory? [Y/n/q]:
            _type:y 
            _out:√ Path '{direpa_test}' created.
            _out:Enter user name [q to quit]:
            _type:user_name
            _out:Enter user email [q to quit]:
            _type:test@test.com
            _out:Enter origin repository [q to quit]:
        """,
        "block_input_license": """
            _out:Do you Want To Add a License [Y/n/q]:
            _type:Y
            _out:choice or 'q' to quit:
            _type:1
            _out:Copyright Holders:  [q to quit]:
            _type:Thomas Edison
        """,
        "block_create_bump_release_version_script": """
            {step} bump_release_version_script
            mkdir -p {direpa_scripts}
            echo '#!/bin/bash' > {filenpa_bump_release_version}
            echo 'echo $1' >> {filenpa_bump_release_version}
            chmod +x {filenpa_bump_release_version}
        """   
    })

    if conf["mode"] == "local_path":
        set_test_steps(conf,"""
            {step} new_project local
            mkdir -p {direpa_par_remote_src}
            {this_cmd}
            {block_input_create_directory}
            _type:{direpa_remote_src}
            {block_input_license}
            _out:√ Remote Path '{direpa_par_remote_src}' is reachable.
            _out:∆ Remote Repository '{direpa_remote_src}' does not exist.
            _out:√ git clone --bare {direpa_test_src} {direpa_remote_src}
            _out:√ New Project test initialized.
            pwd
            cd {direpa_test_src}
            git checkout master
            git tag start_master
            git checkout develop
            git tag start_develop
            git push origin master
            git push origin develop
            {block_create_bump_release_version_script}
            {filenpa_bump_release_version} 1.0.2
            _out:1.0.2
        """)
    elif conf['mode'] == 'ssh_url':
        set_test_steps(conf,"""
            {step} new_project
            mkdir -p {direpa_par_remote_src}
            {this_cmd}
            {block_input_create_directory}
            _type:{ssh_url_domain_direpa_src}
            {block_input_license}
            _out:Type ssh username [q to quit]:
            _type:{user_current}
            _out:√ git clone --bare {direpa_test_src} {direpa_test_src}.git
            _out:{user_current}@{domain}'s password:
            _type:{sudo_pass}
            _out:√ scp -r {direpa_test_src}.git {scp_url_domain_direpa_par_src}
            _out:{user_current}@{domain}'s password:
            _type:{sudo_pass}
            _out:[sudo] password for {user_current}:
            _type:{sudo_pass}
            _out:√ ssh -t {user_current}@{domain} "sudo chown -R {user_git}:{user_git} {direpa_remote_src}"
            _out:√ {direpa_test_src}.git deleted on local.
            cd {direpa_test_src}
            git checkout master
            git tag start_master
            git checkout develop
            git tag start_develop
            git push origin master
            git push origin develop
            {block_create_bump_release_version_script}
            ssh {user_current}@{domain} "{filenpa_bump_release_version} 1.0.2"
            _out:{user_current}@{domain}'s password:
            _type:{sudo_pass}
            _out:1.0.2
        """)

    test_processor(conf)
