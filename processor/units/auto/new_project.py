#!/usr/bin/env python3
import os
if __name__ != "__main__":
    from processor.utils.processor_engine import start_processor, set_task_steps, set_task_vars
    # from utils.json_config import Json_config
    
    import sys

def new_project(conf):
    from pprint import pprint

    set_task_vars(conf, {
        'block_ssh_credentials': """
            _out:Type ssh username [q to quit]:
            _type:{ssh_user}
            _out:[sudo] password for {ssh_user}:
            _type:{server_pass}
        """,
        'current_path': os.getcwd(),
        'domain':conf["tmp"]["domain"],
        'direpa_ssh':conf["tmp"]["direpa_ssh"],
        'git_user_name': conf["tmp"]["git_user_name"],
        'git_user_email': conf["tmp"]["git_user_email"],
        'ssh_user': conf["tmp"]["ssh_user"],
        'repository': conf["tmp"]["repository"],
        'server_pass':conf["tmp"]["server_pass"],
        'this_cmd':"gitframe --np"
    })

    set_task_steps(conf,"""
        {step} automated new_project
        {this_cmd}
        _out:Do you want to add git to directory anyway [Ynq]?
        _type:Y
        _out:Enter git user name [q to quit]:
        _type:{git_user_name}
        _out:Enter git user email [q to quit]:
        _type:{git_user_email},
        _out:Enter origin parent repository [q to quit]:
        _type:{repository}
        {block_ssh_credentials}
        {block_ssh_credentials}
        {block_ssh_credentials}
    """)

    start_processor(conf)
