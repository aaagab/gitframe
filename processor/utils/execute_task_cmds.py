#!/usr/bin/env python3
from pprint import pprint
import os
import subprocess
import shlex
import sys
import re
import tempfile
import time

try:
    from ...gpkgs import message as msg
    from ...gpkgs import shell_helpers as shell
    from ...gpkgs.format_text import Format_text as ft
except:
    direpa_script=os.path.realpath(__file__)
    direpa_launcher=os.path.dirname(os.path.dirname(os.path.dirname(direpa_script)))
    sys.path.insert(0,direpa_launcher)
    from gpkgs import message as msg
    from gpkgs import shell_helpers as shell
    from gpkgs.format_text import Format_text as ft

def execute_task_cmds(conf, unit_name):
    
    # tmux list-panes
    # 
    # tmux swap-pane -s gitframe:1.0


    num_panes=len(shell.cmd_get_value("tmux list-panes").splitlines())
    if num_panes == 3:
        cmd=re.sub(r"\n\s*", "\n","""
            tmux break-pane -d -s 2
            tmux select-layout even-horizontal
            tmux select-pane -t 0
        """)[1:-1]
        os.system(cmd)

    elif num_panes == 2:
        tmux_panes=shell.cmd_get_value("tmux list-panes -s -F '#{window_id}|#{pane_title}'")
        window_id, pane_name = tmux_panes.splitlines()[1].split("|")
        window_id=window_id.replace("@", "")
        
        if pane_name == "logs":
            cmd=re.sub(r"\n\s*", "\n","""
                tmux select-pane -t 1
                tmux swap-pane -s gitframe:1.0
                tmux select-pane -t 0
                tmux set -g status-bg green
            """.format(
                task_name=conf["task_name"]
            ))[1:-1]
            os.system(cmd)

    command="screen -c '{}' -S '{}' -d -m -L".format(conf["filenpa_screenrc"], unit_name)
    if subprocess.call(shlex.split(command)) != 0:
        msg.user_error(command)
        sys.exit(1)

    cmd=re.sub(r"\n\s*", "\n","""
        tmux send-keys -t 1 "screen -r -d '{unit_name}'"
        tmux send-keys -t 1 KPEnter
        tmux send-keys -t 1 KPEnter
    """.format( unit_name=unit_name)
    )[1:-1]
    os.system(cmd)

    cmds=[]
    
    cmds.append(r"#!/bin/bash")
    cmds.append(r'echo -ne "\ec\e[3J"')
    cmds.append(r'echo -e "\t\e[1;33mUNIT: '+conf["filen_launcher"]+' '+unit_name+'\e[0m"')
    cmds.append('echo')

    cmd_num=0
    step_num=0
    for i, cmd in enumerate(conf[unit_name]["cmds"]):
        step=re.match(r"{step}(.*)",cmd)
        info=re.match(r"{info}(.*)",cmd)
        if step:
            step_value=step.group(1).strip()
            if not step_value:
                step_value=""

            step_num+=1
            cmds.append(r'echo -e "\n\t\e[1;35m___ Step '+str(step_num)+':\e[0m '+step_value+'"')
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
            cmd_display=cmd.replace(conf["direpa_launcher"], ".../"+os.path.basename(os.path.normpath(conf["direpa_launcher"])))
            cmd_display=cmd_display.replace('"','\'')
            cmds.append('echo;')
            cmds.append('echo -e "\e[1;33m==\e[0m" '+str(cmd_num)+' "\e[1;33m==\e[0m" :'+str(conf["tmp"]["cmds_line_num"][i])+': "'+cmd_display+'"')
            cmds.append(cmd+' || ( echo -e "\e[1;31m'+conf["txt_screen_cmd_error"]+'\e[0m" && sleep .4 )')

    cmds.append(r'echo -e "\n'+conf["txt_screen_log_eof"]+'"')
    cmds.append(r'rm '+conf["filenpa_cmds"])

    # copy cmds to file
    with open(conf["filenpa_cmds"], 'w') as f:
        for cmd in cmds:
            f.write(cmd)
            f.write("\n")

    # make file executable
    os.chmod(conf["filenpa_cmds"], 0o755)    
    
    # for cmd in cmds:
    #     print(cmd)
    open(conf["filenpa_screen_log"], 'w').close()
    
    # launch script with screen session
    cmd=re.sub(r"\n\s*", "\n","""
        tmux send-keys -t 1 {cmd}
        tmux send-keys -t 1 KPEnter
    """.format(cmd=conf["filenpa_cmds"]))[1:-1]
    os.system(cmd)

    