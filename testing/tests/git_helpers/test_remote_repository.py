#!/usr/bin/env python3
import os, sys
if __name__ != "__main__":
    from testing.utils.test_processor import test_processor, set_test_steps, set_test_vars
    from utils.json_config import Json_config
    import utils.shell_helpers as shell
    import re
    from pprint import pprint

def test_remote_repository(conf):
    set_test_vars(conf, {
        "direpa_par_remote_src": conf["remote"]["direpa_par_src"],
        "direpa_remote_src": conf["remote"]["direpa_src"],
        "direpa_test": conf["direpa_test"],
        "direpa_repository": conf["direpa_repository"],
        "direpa_test_src": conf["direpa_test_src"],
        'direpa_testgf': conf["direpa_testgf"],        
        "diren_src": conf["diren_src"],
        "block_user_input": """
            _out:Enter user name [q to quit]:
            _type:user_name
            _out:Enter user email [q to quit]:
            _type:test@test.com
            _out:Enter origin repository [q to quit]:
        """,
        "ssh_url_domain_direpa_src": conf["remote"]["ssh_url_domain_direpa_src"],
        "ssh_url_domain_direpa_par_src": conf["remote"]["ssh_url_domain_direpa_par_src"],
        "domain": conf["remote"]["domain"],
        "user_git": conf["remote"]["user_git"],
        "sudo_pass": conf.get("sudo_pass"),
        "user_current": conf["user_current"],
        "ssh_url_ip_direpa_src": conf["remote"]["ssh_url_ip_direpa_src"],
        "ssh_url_ip_direpa_par_src": conf["remote"]["ssh_url_ip_direpa_par_src"],
        "ip": conf["remote"]["ip"],
    })

    if conf["mode"] == "local_path":
        set_test_steps(conf, """
            {step} local
            mkdir -p {direpa_test}
            cd {direpa_test}
            git init .
            {cmd}
            {block_user_input}
            _type:{direpa_remote_src}
            _out:path: {direpa_remote_src}
            _out:direpa_src: {direpa_remote_src}
            _out:path_type: directory
            _out:direpa_par_src: {direpa_par_remote_src}
            cd {direpa_testgf}
            rm -rf {direpa_test}
        """)
    elif conf["mode"] == "ssh_url":
        set_test_steps(conf, """
            {step} remote url_with_name
            mkdir -p {direpa_test_src}
            cd {direpa_test_src}
            git init .
            touch myfile.txt
            git add .
            # git commit -am "myfile"
            git -c user.name='user_name' -c user.email='test@test.com' commit -am "myfile"
            mkdir -p {direpa_remote_src}
            cd {direpa_test}
            git clone --bare {diren_src} {direpa_remote_src}
            sudo -k
            sudo chown -R {user_git}:{user_git} {direpa_remote_src}
            _out:[sudo] password for {user_current}: 
            _type:{sudo_pass}
            cd {diren_src}
            {cmd}
            {block_user_input}
            _type:{ssh_url_domain_direpa_src}
            _out:√ Remote Path '{domain}' is reachable.
            _out:√ Remote Repository '{ssh_url_domain_direpa_src}' exists.
            _out:path: {ssh_url_domain_direpa_src}
            _out:domain: {domain}
            _out:direpa_src: {direpa_remote_src}
            _out:user_git: {user_git}
            _out:path_type: url
            _out:direpa_par_src: {direpa_par_remote_src}
            cd {direpa_testgf}
            rm -rf {direpa_test}
            sudo rm -rf {direpa_repository}

            {step} remote url_with_ip
            mkdir -p {direpa_test_src}
            cd {direpa_test_src}
            git init .
            touch myfile.txt
            git add .
            # git commit -am "myfile"
            git -c user.name='user_name' -c user.email='test@test.com' commit -am "myfile"
            mkdir -p {direpa_remote_src}
            cd {direpa_test}
            git clone --bare {diren_src} {direpa_remote_src}
            sudo -k
            sudo chown -R {user_git}:{user_git} {direpa_remote_src}
            _out:[sudo] password for {user_current}: 
            _type:{sudo_pass}
            cd {diren_src}
            {cmd}
            {block_user_input}
            _type:{ssh_url_ip_direpa_src}
            _out:√ Remote Path '{ip}' is reachable.
            _out:√ Remote Repository '{ssh_url_ip_direpa_src}' exists.
            _out:path: {ssh_url_ip_direpa_src}
            _out:domain: {ip}
            _out:direpa_src: {direpa_remote_src}
            _out:user_git: {user_git}
            _out:path_type: url
            _out:direpa_par_src: {direpa_par_remote_src}
            cd {direpa_testgf}
            rm -rf {direpa_test}
            sudo rm -rf {direpa_repository}
        """)

    test_processor(conf)

if __name__ == "__main__":
    direpa_script=os.path.realpath(__file__)
    while os.path.basename(direpa_script) != "src":
        direpa_script=os.path.dirname(direpa_script)
    sys.path.insert(0,direpa_script)

    from git_helpers.remote_repository import Remote_repository

    repo=Remote_repository()

    if sys.argv[1] == "local":
        print()
        print("path: "+repo.path)
        print("direpa_src: "+repo.direpa_src)
        print("path_type: "+repo.path_type)
        print("direpa_par_src: "+repo.direpa_par_src)
    elif sys.argv[1] == "remote":
        print()
        print("path: "+repo.path)
        print("domain: "+repo.domain)
        print("direpa_src: "+repo.direpa_src)
        print("user_git: "+repo.user_git)
        print("path_type: "+repo.path_type)
        print("direpa_par_src: "+repo.direpa_par_src)
