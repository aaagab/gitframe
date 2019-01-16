#!/usr/bin/env python3
import os
if __name__ != "__main__":
    from processor.utils.processor_engine import start_processor, set_task_steps, set_task_vars
    from utils.json_config import Json_config
    
    import sys

def new_project(conf):
    from pprint import pprint
    # pprint(conf)

    set_task_vars(conf, {
        # "direpa_remote_src": conf["remote"]["direpa_src"],
        # "direpa_par_remote_src": conf["remote"]["direpa_par_src"],
        # "direpa_task": conf["direpa_task"],
        # "direpa_task_src": conf["direpa_task_src"],
        # "filenpa_deploy": conf["filenpa_deploy"],
        # "filenpa_bump_version": conf["filenpa_bump_version"],
        # 'this_cmd':conf["filenpa_launcher"]+" "+conf["tmp"]["opt"]+" "+conf["diren_task"],
        # "ssh_url_domain_direpa_src": conf["remote"]["ssh_url_domain_direpa_src"],
        # "ssh_url_domain_direpa_par_src": conf["remote"]["ssh_url_domain_direpa_par_src"],
        # "scp_url_domain_direpa_src": conf["remote"]["scp_url_domain_direpa_src"],
        # "scp_url_domain_direpa_par_src": conf["remote"]["scp_url_domain_direpa_par_src"],
        # "user_git": conf["remote"]["user_git"],
        # "user_current": conf["user_current"],
        # "domain": conf["remote"]["domain"],
        # "diren_src": conf["diren_src"],
        # "sudo_pass": conf.get("sudo_pass"),
        # "block_input_create_directory": """
        #     _out:Enter git user name [q to quit]:
        #     _type:{user_git}
        #     _out:Enter git user email [q to quit]:
        #     _type:test@test.com
        #     _out:Enter origin parent repository [q to quit]:
        # """,
        # "block_input_license": """
        #     _out:Do you Want To Add a License [Y/n/q]:
        #     _type:Y
        #     _out:choice or 'q' to quit:
        #     _type:1
        #     _out:Copyright Holders:  [q to quit]:
        #     _type:Thomas Edison
        # """,
        # "block_create_scripts_deploy_and_bump": """
        #     {step} bump_release_version_script
        #     echo '#!/usr/bin/env python3' > {filenpa_deploy}
        #     echo 'import sys' >> {filenpa_deploy}
        #     echo 'print(sys.argv[1])' >> {filenpa_deploy}
        #     chmod +x {filenpa_deploy}
        #     echo '#!/usr/bin/env python3' > {filenpa_bump_version}
        #     echo 'import sys' >> {filenpa_bump_version}
        #     echo 'print(sys.argv[1])' >> {filenpa_bump_version}
        #     chmod +x {filenpa_bump_version}
        # """   
    })

    set_task_steps(conf,"""
        {step} automated new_project
        echo "I am here"
        
        # {step} new_project local
        # mkdir -p {direpa_par_remote_src}
        # {this_cmd}
        #     _out:Do you want to create directory? [Y/n/q]:
        # _type:y 
        # _out:√ Path '{direpa_task}' created.
        # {block_input_create_directory}
        # _type:{direpa_par_remote_src}
        # {block_input_license}
        # _out:√ Remote Path '{direpa_par_remote_src}' is reachable.
        # _out:∆ Remote Repository '{direpa_remote_src}' does not exist.
        # _out:√ git clone --bare {direpa_task_src} {direpa_remote_src}
        # _out:√ New Project test initialized.
        # pwd
        # cd {direpa_task_src}
        # git checkout master
        # git tag start_master
        # git checkout develop
        # git tag start_develop
        # git push origin master
        # git push origin develop
        # {block_create_scripts_deploy_and_bump}
        # {filenpa_deploy} 1.0.2
        # _out:1.0.2
        # {filenpa_bump_version} 1.0.2
        # _out:1.0.2
    """)

    # set_task_steps(conf,"""
    #     {step} new_project
    #     mkdir -p {direpa_par_remote_src}
    #     {this_cmd}
        
    #     _out:Do you want to create directory? [Y/n/q]:
    #     _type:y 
    #     _out:√ Path '{direpa_task}' created.

    #     {block_input_create_directory}
    #     _type:{ssh_url_domain_direpa_par_src}
    #     _out:Do you Want To Add a License [Y/n/q]:
    #     _type:n
    #     _out:Type ssh username [q to quit]:
    #     _type:{user_current}
    #     _out:√ git clone --bare {direpa_task}/doc {direpa_task}/doc.git
    #     _out:{user_current}@{domain}'s password:
    #     _type:{sudo_pass}
    #     _out:√ ssh {user_current}@{domain} "mkdir -p {direpa_par_remote_src}"
    #     _out:{user_current}@{domain}'s password:
    #     _type:{sudo_pass}
    #     _out:√ scp -r {direpa_task}/doc.git {scp_url_domain_direpa_par_src}/doc.git
    #     _out:{user_current}@{domain}'s password:
    #     _type:{sudo_pass}
    #     _out:[sudo] password for {user_current}:
    #     _type:{sudo_pass}
    #     _out:√ ssh -t {user_current}@{domain} "sudo chown -R {user_git}:{user_git} {direpa_par_remote_src}/doc.git"
    #     _out:√ '{direpa_task}/doc.git' deleted on local.

    #     _out:Type ssh username [q to quit]:
    #     _type:{user_current}
    #     _out:√ git clone --bare {direpa_task}/mgt {direpa_task}/mgt.git
    #     _out:{user_current}@{domain}'s password:
    #     _type:{sudo_pass}
    #     _out:√ ssh {user_current}@{domain} "mkdir -p {direpa_par_remote_src}"
    #     _out:{user_current}@{domain}'s password:
    #     _type:{sudo_pass}
    #     _out:√ scp -r {direpa_task}/mgt.git {scp_url_domain_direpa_par_src}/mgt.git
    #     _out:{user_current}@{domain}'s password:
    #     _type:{sudo_pass}
    #     _out:[sudo] password for {user_current}:
    #     _type:{sudo_pass}
    #     _out:√ ssh -t {user_current}@{domain} "sudo chown -R {user_git}:{user_git} {direpa_par_remote_src}/mgt.git"
    #     _out:√ '{direpa_task}/mgt.git' deleted on local.
        
    #     _out:Type ssh username [q to quit]:
    #     _type:{user_current}
    #     _out:√ git clone --bare {direpa_task}/src {direpa_task}/src.git
    #     _out:{user_current}@{domain}'s password:
    #     _type:{sudo_pass}
    #     _out:√ ssh {user_current}@{domain} "mkdir -p {direpa_par_remote_src}"
    #     _out:{user_current}@{domain}'s password:
    #     _type:{sudo_pass}
    #     _out:√ scp -r {direpa_task}/src.git {scp_url_domain_direpa_par_src}/src.git
    #     _out:{user_current}@{domain}'s password:
    #     _type:{sudo_pass}
    #     _out:[sudo] password for {user_current}:
    #     _type:{sudo_pass}
    #     _out:√ ssh -t {user_current}@{domain} "sudo chown -R {user_git}:{user_git} {direpa_par_remote_src}/src.git"
    #     _out:√ '{direpa_task}/src.git' deleted on local.
        
    #     cd {direpa_task_src}
    #     git checkout master
    #     git tag start_master
    #     git checkout develop
    #     git tag start_develop
    #     git push origin master
    #     git push origin develop
    #     {block_create_scripts_deploy_and_bump}
    #     ssh {user_current}@{domain} "{filenpa_deploy} 1.0.2"
    #     _out:{user_current}@{domain}'s password:
    #     _type:{sudo_pass}
    #     _out:1.0.2
    #     ssh {user_current}@{domain} "{filenpa_bump_version} 1.0.2"
    #     _out:{user_current}@{domain}'s password:
    #     _type:{sudo_pass}
    #     _out:1.0.2
        # """)

    start_processor(conf)
