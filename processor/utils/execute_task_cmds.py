#!/usr/bin/env python3
import os
import subprocess
import shlex
import sys
import utils.message as msg
import processor.utils.processor_helpers as ph
import re
import tempfile
from utils.format_text import Format_text as ft
from pprint import pprint
from utils.json_config import Json_config
import time
import utils.shell_helpers as shell
    

def execute_task_cmds(conf, test_name):

    # print a blank page kirk for visual rendering on terminal
    ph.send_cmd_to_screen(conf["main_session_name"], conf["filenpa_blank_page"])

    # create a new session
    command="screen -c '{}' -S '{}' -d -m -L".format(conf["filenpa_screenrc"], conf[test_name]["session_name"])
    if subprocess.call(shlex.split(command)) != 0:
        msg.user_error(command)
        sys.exit(1)

    # attach it
    open(conf["filenpa_screen_log"], 'w').close()
    ph.send_cmd_to_screen(conf["main_session_name"], "screen -r -d \""+conf[test_name]["session_name"]+"\"")
    # clear scrolling
    ph.send_cmd_to_screen(conf["main_session_name"], "echo -en \"\ec\e[3J\"")

    cmds=[]
    
    cmds.append(r"#!/bin/bash")
    cmds.append(r'echo -ne "\e]0;'+conf[test_name]["session_name"]+r'\007"')
    cmds.append(r'echo -e "\t\e[1;33mTEST: '+conf["filen_app"]+' '+test_name+'\e[0m\n"')
    cmd_num=0
    step_num=0
    for i, cmd in enumerate(conf[test_name]["cmds"]):
        step=re.match(r"{step}(.*)",cmd)
        info=re.match(r"{info}(.*)",cmd)
        if step:
            step_value=step.group(1).strip()
            if not step_value:
                step_value=""

            step_num+=1
            cmds.append(r'echo -e "\n\t\e[1;35m### Step '+str(step_num)+':\e[0m '+step_value+'"')
            cmd_num=0
        elif info:
            info_value=info.group(1).strip()
            if not info_value:
                info_value=""
            else:
                info_value=info_value.replace("\"","'")

            cmds.append(r'echo -e " \e[4;2mINFO\e[0m: '+info_value+'"')
        else:
            cmd_num+=1
            cmd_display=cmd.replace(conf["direpa_app"], ".../"+os.path.basename(os.path.normpath(conf["direpa_app"])))
            cmd_display=cmd_display.replace('"','\'')
            cmds.append('echo;')
            cmds.append('echo -e "\e[1;33m==\e[0m" '+str(cmd_num)+' "\e[1;33m==\e[0m" :'+str(conf["tmp"]["cmds_line_num"][i])+': "'+cmd_display+'"')
            cmds.append(cmd+' || ( echo -e "\e[1;31m'+conf["txt_screen_cmd_error"]+'\e[0m" && sleep .4 )')

    cmds.append(r'echo -e "\n'+conf["txt_screen_log_eof"]+'"')
    cmds.append(r'rm '+conf["direpa_cmds"])

    # copy cmds to file
    with open(conf["direpa_cmds"], 'w') as f:
        for cmd in cmds:
            f.write(cmd)
            f.write("\n")

    # make file executable
    os.chmod(conf["direpa_cmds"], 0o755)    
    
    # for cmd in cmds:
    #     print(cmd)
    
    # launch script with screen session
    ph.send_cmd_to_screen(conf[test_name]["session_name"], conf["direpa_cmds"])
    