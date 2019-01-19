#!/usr/bin/env python3
import os
import subprocess
import shlex
import sys
import utils.message as msg
import processor.utils.processor_helpers as ph
import time
import re

import inspect
from utils.install_dependencies import install_dependencies
from copy import deepcopy
from utils.format_text import Format_text as ft

import utils.shell_helpers as shell
from processor.utils.task_clean import clean_after_cmd
from processor.utils.execute_task_cmds import execute_task_cmds
from utils.prompt import prompt

from utils.json_config import Json_config
conf_param = Json_config()
from pprint import pprint

import tempfile
import getpass

def get_screen_session_conf(conf):
    return dict(
        direpa_task=os.path.join(conf["processor"]["task"]["direpa"], conf["processor"]["task"]["diren"]),
        filenpa_conf=os.path.join( conf["processor"]["task"]["direpa"],conf["processor"]["filen_conf"] ),
        filenpa_screen_log=os.path.join(conf["processor"]["task"]["direpa"], conf["processor"]["filen_screen_log"]),
        filenpa_screenrc=os.path.join(conf["processor"]["task"]["direpa"], conf["processor"]["filen_screenrc"]),
        task_name=conf["processor"]["task"]["name"],
    )

def terminal_setup(launcher_conf, args):
    direpa_script=os.path.dirname(os.path.realpath(__file__))
    filepa_processor=os.path.join(
        os.path.dirname(direpa_script),
        "processor.py"
    )
    task_name=launcher_conf["processor"]["task"]["name"]

    screen_conf=get_screen_session_conf(launcher_conf)
    os.makedirs(screen_conf["direpa_task"], exist_ok=True)

    open(screen_conf["filenpa_conf"], 'w').close()

    text=re.sub(r'\n\s*','\n',"""
        # get output in logfile in realtime
        logfile flush 0
        # use custom logfile
        logfile {filenpa_screen_log}
        # enable scrolling mode in screen session
        termcapinfo xterm* ti@:te@
    """.format(filenpa_screen_log=screen_conf["filenpa_screen_log"]))[1:-1]

    with open(screen_conf["filenpa_screenrc"], "w") as f:
        f.write(text)

    if shell.cmd_devnull("tmux info") == 0:
        tmux_sessions=shell.cmd_get_value("tmux ls")
        for tmux_session in tmux_sessions.splitlines():
            if task_name in tmux_session:
                shell.cmd_prompt("tmux kill-session -t '"+task_name+"'")
                
    cmd=re.sub(r"\n\s*", "\n","""
        tmux new-session -s '{task_name}' -d \\; \\
        set -g mouse on \\; \\
        send-keys "echo -en '\e]2;{task_name}\e[0m'" \\; \\
        send-keys KPEnter \\; \\
        send-keys 'echo -en "\ec\e[3J"' \\; \\
        send-keys KPEnter \\; \\
        split-window -h \\; \\
        send-keys "echo -en '\e]2;processor\e[0m'" \\; \\
        send-keys KPEnter \\; \\
        send-keys 'echo -en "\ec\e[3J"' \\; \\
        send-keys KPEnter \\; \\
        split-window -h \\; \\
        send-keys "echo -en '\e]2;logs\e[0m'" \\; \\
        send-keys KPEnter \\; \\
        send-keys 'echo -en "\ec\e[3J"' \\; \\
        send-keys KPEnter \\; \\
        select-layout even-horizontal \\; \\
        select-pane -t 0 \\; \\
        send-keys "{cmd_processor}" \\; \\
        send-keys KPEnter \\; \\
        attach-session -d
        """.format(
        task_name=task_name,
        cmd_processor=filepa_processor+" '"+"' '".join(args)+"'",
        )
    )[1:-1]

    os.system(cmd)

def init_config(direpa_processor_script):
    launcher_conf=Json_config().data
    ft.clear_screen()

    install_dependencies(launcher_conf["processor"]["deps"])

    conf=dict(

        clean_after=launcher_conf["processor"]["clean_after"],

        direpa_logs=os.path.join(direpa_processor_script, launcher_conf["processor"]["diren_logs"]),
        direpa_launcher=os.path.dirname(direpa_processor_script),

        filen_launcher=launcher_conf["processor"]["filen_launcher"],
        
        filenpa_launcher=os.path.join(os.path.dirname(direpa_processor_script), launcher_conf["processor"]["filen_launcher"]),
        
        num_unit_failures=0,

        read_log_window_title=launcher_conf["processor"]["read_log_window_title"],

        txt_screen_cmd_error=launcher_conf["processor"]["txt_screen_cmd_error"],
        txt_screen_log_eof=launcher_conf["processor"]["txt_screen_log_eof"],

        user_current=getpass.getuser(),

        waiting_time_between_cmds=launcher_conf["processor"]["waiting_time_between_cmds"],
    )

    set_task_conf(launcher_conf, conf)
    open(conf["filenpa_task_status"], 'w').close()

    cmd=re.sub(r"\n\s*", "\n","""
        tmux send-keys -t 1 'echo -en "\ec\e[3J"'
        tmux send-keys -t 1 KPEnter
        tmux send-keys -t 1 ^c
    """)[1:-1]
    os.system(cmd)

    return conf

def set_task_conf(launcher_conf, conf):
    conf.update(
        diren_src=launcher_conf["processor"]["task"]["diren_src"],
        diren_task=launcher_conf["processor"]["task"]["diren"],

        direpa_task_conf=launcher_conf["processor"]["task"]["direpa"],
        direpa_task_src=os.path.join(launcher_conf["processor"]["task"]["direpa"], launcher_conf["processor"]["task"]["diren"],launcher_conf["processor"]["task"]["diren_src"]),
        direpa_repository=os.path.join(launcher_conf["processor"]["task"]["direpa"], launcher_conf["processor"]["task"]["remote"]["diren_root"]),
        direpa_remote_src=os.path.join(launcher_conf["processor"]["task"]["direpa"], launcher_conf["processor"]["task"]["remote"]["diren_root"], launcher_conf["processor"]["task"]["diren"], launcher_conf["processor"]["task"]["diren_src"]+".git"),
        filenpa_deploy=os.path.join(launcher_conf["processor"]["task"]["direpa"], launcher_conf["processor"]["task"]["diren"], launcher_conf["filer_deploy"]+".py"),
        filenpa_bump_version=os.path.join(launcher_conf["processor"]["task"]["direpa"],launcher_conf["processor"]["task"]["diren"], launcher_conf["filer_bump_version"]+".py"),
        filenpa_cmds=os.path.join(launcher_conf["processor"]["task"]["direpa"], launcher_conf["processor"]["filen_cmds"]),
        filenpa_read_log_bashrc=os.path.join(launcher_conf["processor"]["task"]["direpa"], launcher_conf["processor"]["filen_read_log_bashrc"]),

        filenpa_task_status=os.path.join(launcher_conf["processor"]["task"]["direpa"], launcher_conf["processor"]["filen_task_status"]),

        remote=launcher_conf["processor"]["task"]["remote"],
    )

    conf.update(
        get_screen_session_conf(launcher_conf)
    )

    ip=conf["remote"]["ip"]
    domain=conf["remote"]["domain"]
    user_domain=conf["remote"]["user_git"]+"@"+domain
    user_ip=conf["remote"]["user_git"]+"@"+ip
    direpa_src=conf["direpa_remote_src"]
    direpa_par_src=os.path.dirname(conf["direpa_remote_src"])

    conf["remote"].update(
        user_domain=user_domain,
        user_ip=user_ip,
        ssh_url_domain_direpa_par_src=user_domain+":"+os.path.join(direpa_par_src),
        ssh_url_ip_direpa_par_src=user_ip+":"+os.path.join(direpa_par_src),
        ssh_url_domain_direpa_src=user_domain+":"+direpa_src,
        ssh_url_ip_direpa_src=user_ip+":"+direpa_src,
        scp_url_domain_direpa_src=conf["user_current"]+"@"+domain+":"+direpa_src,
        scp_url_domain_direpa_par_src=conf["user_current"]+"@"+domain+":"+direpa_par_src,
        scp_url_ip_direpa_src=conf["user_current"]+"@"+ip+":"+direpa_src,
        scp_url_ip_direpa_par_src=conf["user_current"]+"@"+ip+":"+direpa_par_src,
        direpa_src=direpa_src,
        direpa_par_src=direpa_par_src
    )

def set_unit_conf(conf):
    frame,filename,line_number,function_name,lines,index=inspect.stack()[2]

    unit_name=conf["tmp"]["unit_name"]

    conf.update({
        unit_name:{
            'filenpa_screen_log': conf["filenpa_screen_log"],
            'cmds': conf["tmp"]["exec_cmds"],
        }
    })

    conf_for_json=deepcopy(conf)
    conf_for_json.pop('tmp', None)
    conf_for_json.pop('sudo_pass', None)

    Json_config(conf["filenpa_conf"]).set_file_with_data(conf_for_json)
    
def start_processor(conf):

    unit_name=conf["tmp"]["unit_name"].strip().replace(" ","_")
    conf['tmp']['unit_name']=unit_name
    if not conf.get('unit_num'):
        conf['unit_num']=1
    else:
        conf['unit_num']+=1

    ph.log_to_task_status_file(conf["filenpa_task_status"],"unit", conf['unit_num'], unit_name)

    try:
        caller_filename=inspect.stack()[1][1]

        set_unit_conf(conf)
        execute_task_cmds(conf, unit_name)

        if not os.path.exists(conf["filenpa_screen_log"]):
            msg.app_error(conf["filenpa_screen_log"]+" not found.")
            sys.exit(1)

        msg.title("UNIT: "+conf["filen_launcher"]+" "+unit_name)
        
        msg.subtitle("Starting Unit")
        tail_obj=dict(
            interrupted=False,
            file_start_position=0,
            waiting_time="",
            searched_value=""
        )
        
        step_num=0

        for line_obj in conf["tmp"]["cmds_to_monitor"]:
            key=next(iter(line_obj))
            obj_value=line_obj[key]

            if key == "fail":
                # this part is for failing command
                tail_obj["searched_value"]=conf["txt_screen_cmd_error"]
                tail_obj["failing_cmd_name"]=obj_value
                tmp_tail_obj=tail_screen_file(conf, tail_obj)
                tail_obj["file_start_position"]=tmp_tail_obj["file_start_position"]
                tail_obj["interrupted"]=tmp_tail_obj["interrupted"]

            elif key == "time":
                if re.match(r"\d{2}:\d{2}:\d{2}", obj_value):
                    tail_obj["waiting_time"]=obj_value
                elif re.match(r"\d.*",obj_value):
                    if (int(obj_value)):
                        tail_obj["waiting_time"]=seconds_to_hhmmss(int(obj_value))
                else:
                    msg.user_error(
                        "Format unknown time: "+obj_value+" for object: ",
                        str(line_obj),
                        "from file: "+caller_filename
                    )
                    sys.exit(1)
                continue
            elif key == "type":
                cmd=re.sub(r"\n\s*", "\n","""
                    tmux send-keys -t 1 '{user_input}'
                    tmux send-keys -t 1 KPEnter
                """.format(
                    user_input=obj_value.replace("type:", "").strip()
                ))[1:-1]
                os.system(cmd)
                continue
            elif key == "step":
                if not obj_value:
                   obj_value="" 

                step_num+=1
                print("\n  "+ft.lMagenta("### Step "+str(step_num)+": ")+obj_value)
                ph.log_to_task_status_file(conf["filenpa_task_status"],"step", step_num, obj_value)
                continue
            elif key == "out":
                tail_obj["searched_value"]=obj_value
                # print(obj_value)
                # if obj_value == '\x1b[K':
                    # print("here unicode")
                tmp_tail_obj=tail_screen_file(conf, tail_obj)
                tail_obj["file_start_position"]=tmp_tail_obj["file_start_position"]
                tail_obj["interrupted"]=tmp_tail_obj["interrupted"]
                tail_obj["waiting_time"]="" # reset waiting time
                
            else:
                msg.user_error(
                    "key unknown: "+key+" for object: ",
                    str(line_obj),
                    "from file: "+caller_filename
                )
                sys.exit(1)

            if tail_obj["interrupted"] == True:
                break

        if tail_obj["interrupted"]:
            ph.log(conf)
            ph.kill_screen_session(unit_name)
            sys.exit(1)
        else:
            # continue processing the script until the end
            tail_obj["searched_value"]=conf["txt_screen_log_eof"]
            tmp_tail_obj=tail_screen_file(conf, tail_obj)
            # if error
            if tmp_tail_obj["interrupted"]:
                ph.log(conf)
                ph.kill_screen_session(unit_name)
                sys.exit(1)
            else:
                print()
                msg.success("All steps succeeded for unit: "+ unit_name)

    except KeyboardInterrupt:
        conf["num_unit_failures"]+=1
        # when a unit is stopped by ctrl+c on the unit windows
        msg.user_error("Unit "+unit_name+" canceled.")
        sys.exit(1)
    except SystemExit as e:
        if int(str(e)) != 3:
            conf["num_unit_failures"]+=1
            msg.user_error("Predictable Error for Unit "+unit_name)

        time.sleep(1)
        ph.kill_screen_session(unit_name)

    except Exception as e:
        conf["num_unit_failures"]+=1
        msg.app_error("Not Predictable Error for Unit "+unit_name)
        time.sleep(1)
        ph.kill_screen_session(unit_name)
        
        sys.exit(1)
    finally:
        ph.kill_screen_session(unit_name)
        
        if conf["clean_after"]:
            clean_after_cmd(conf)
            conf["clean_after"]=False

        # delete individual unit data in conf
        del conf[unit_name]
        del conf["tmp"]
        conf_for_json=deepcopy(conf)
        conf_for_json.pop('sudo_pass', None)

        Json_config(conf["filenpa_conf"]).set_file_with_data(conf_for_json)
        # ph.send_cmd_to_screen(
        #     conf["task_name"], 
        #     r'echo -ne "\e]2;'+conf["task_name"]+r'\e[0m"'
        # )

def tail_screen_file(conf, tail_obj):
    try:
        time_max_wait=0
        if not tail_obj["waiting_time"]:
            time_max_wait=conf["waiting_time_between_cmds"]
        else:
            time_max_wait=time_to_seconds(tail_obj["waiting_time"])

        f = open(conf["filenpa_screen_log"])
        p = tail_obj["file_start_position"]
        tail_return_obj=dict(
            file_start_position=tail_obj["file_start_position"],
            interrupted=False
        )

        start_time = time.time()
        end_time=0
        elapsed_time=0
        while True:
            previous_p=p            
            f.seek(p)
            latest_data = f.readline().strip()
            p = f.tell()
            if latest_data:
                line=clean_ansii_code(latest_data)
                if line == tail_obj["searched_value"]:
                    if line == conf["txt_screen_cmd_error"]:
                        tail_return_obj["file_start_position"]=p
                        msg.success("Normal Failure: '"+str(tail_obj["failing_cmd_name"])+"'")
                        return tail_return_obj
                    elif line == conf["txt_screen_log_eof"]:
                        tail_return_obj["file_start_position"]=p
                        return tail_return_obj
                    elif line == "\033[K":
                        # this is for init_readline_screen in utils
                        msg.success("done")
                        sys.exit(3)
                    else:
                        msg.success("Found >> "+tail_obj["searched_value"])
                        tail_return_obj["file_start_position"]=p
                        return tail_return_obj
                else:
                    if line == conf["txt_screen_cmd_error"]:
                        check_for_KeyboardInterrupt_in_screen_file(f, previous_p)
                        msg.user_error("cmd_error Unit "+conf['tmp']['unit_name']+" failed on '"+tail_obj["searched_value"]+"'")
                        tail_return_obj["interrupted"]=True
                        return tail_return_obj
                    elif line == conf["txt_screen_log_eof"]:
                        msg.user_error("EOF Unit "+conf['tmp']['unit_name']+" failed on '"+tail_obj["searched_value"]+"'")
                        tail_return_obj["interrupted"]=True
                        return tail_return_obj

            time.sleep(.01)
            
            end_time = time.time()
            elapsed_time = end_time - start_time
            if elapsed_time >= time_max_wait:
                message="time_max_wait "+str(time_max_wait)+" has been reached for value: \""+tail_obj["searched_value"]+"\""
                with open(conf["filenpa_screen_log"], "a") as f:                               
                    f.write("\n# Error: "+message+"\n")
                tail_return_obj["interrupted"]=True
                msg.info(message)
                
                return tail_return_obj

    except KeyboardInterrupt:
        conf["num_unit_failures"]+=1
        print()
        msg.user_error("Program Exited Ctrl+C")
        sys.exit(1)

def seconds_to_hhmmss(total_seconds):
    hours =  int(total_seconds / 3600)
    remainder= total_seconds - (hours * 3600)
    if hours < 10:
        hours="0"+str(hours)
    minutes =  int(remainder / 60)
    remainder= remainder - (minutes * 60)
    if minutes < 10:
        minutes="0"+str(minutes)
    seconds =  remainder
    if seconds < 10:
        seconds="0"+str(seconds)
    
    return "{}:{}:{}".format(hours, minutes, seconds)

def time_to_seconds(waiting_time):
    return sum(x * int(t) for x, t in zip([3600, 60, 1], waiting_time.split(":")))

def clean_ansii_code(line):
    return re.sub("\\x1b\[.*?[0-9][a-zA-Z]", "", line).strip()

def check_for_KeyboardInterrupt_in_screen_file(file, last_position):
    text="KeyboardInterrupt"
    p=last_position

    newline=0
    read_text=""
    grabbed_input=False
    while p > len(text):
        file.seek(p)
        try:
            if file.read(1) == '\n':
                newline+=1
        except UnicodeDecodeError:
            # ignore encoding issue like:
            # UnicodeDecodeError: 'utf-8' codec can't decode byte 0x9a in position 0: invalid start byte
            pass

        if newline == 3:
            read_text=file.readline()
            grabbed_input=True
            break

        p-=1

    if grabbed_input:
        if clean_ansii_code(read_text).strip() == text:
            msg.user_error("keyboard interrupt in unit window")
            sys.exit(1)

def set_task_steps(conf, cmds):
    frame,caller_filename,caller_line_number,function_name,lines,index=inspect.stack()[1]
    count_line=0
    with open(caller_filename) as f:
        for i, line in enumerate(f, 1):
            if "set_task_steps(conf" in line:
                count_line=i
            # manage multiple set_task_steps
            if i == caller_line_number:
                break

    if not "{step}" in cmds:
        cmds="\n{step} "+conf["tmp"]["unit_name"]+cmds
        count_line-=1

    # add cmds to json file
    if not "exec_cmds" in conf["tmp"]:
        conf["tmp"]["exec_cmds"]=[]
    if not "cmds_line_num" in conf["tmp"]:
        conf["tmp"]["cmds_line_num"]=[]
    if not "cmds_to_monitor" in conf["tmp"]:
        conf["tmp"]["cmds_to_monitor"]=[]
    
    cmds=cmds.splitlines()[1:]

    step_args=""
    for i, cmd in enumerate(cmds):
        count_line+=1
        cmd=cmd.strip()
        # ignore empty line
        if cmd:
            # ignore commented line
            if not re.match(r"^#.*", cmd):
                block=re.match(r"^{(block_.+)}$",cmd)
                # msg.title('ere')
                if block:
                    if "cmd_vars" in conf["tmp"]:
                        if block.group(1) in conf["tmp"]["cmd_vars"]:
                            block_cmds=cmd.replace("{"+block.group(1)+"}", conf["tmp"]["cmd_vars"][block.group(1)])
                            for j, block_cmd in enumerate(block_cmds.splitlines()):
                                block_cmd=block_cmd.strip()
                                if block_cmd:
                                    # ignore commented line
                                    if not re.match(r"^#.*", block_cmd):
                                        step_args=process_cmd(conf, block_cmd, count_line, caller_filename, block_cmds, j, step_args)
                        else:
                            msg.user_error("'"+block+"' has no related key from set_task_vars",
                                "Line:"+str(count_line)+" "+caller_filename)
                            sys.exit(1)
                    else:
                        msg.user_error("'"+block+"' because set_task_vars is not set",
                            "Line:"+str(count_line)+" "+caller_filename)
                        sys.exit(1)
                else:
                    step_args=process_cmd(conf, cmd, count_line, caller_filename, cmds, i, step_args)

def replace_cmd_heredoc(conf, cmd):
    here_doc_vars=re.findall(r".*?{(?!step}|info}|dep})(.+?)}", cmd)
    if here_doc_vars:
        if not "cmd_vars" in conf["tmp"]:
            conf["tmp"]["cmd_vars"]=[]
            
        for key_doc in here_doc_vars:
            for key_cmd in conf["tmp"]["cmd_vars"]:
                if key_doc == key_cmd:
                    # msg.title(key_doc)
                    cmd=cmd.replace("{"+key_doc+"}", conf["tmp"]["cmd_vars"][key_cmd])

    return cmd

def process_cmd(conf, cmd, count_line, caller_filename, cmds, index, step_args):
    step=re.match(r"^{step}(.*)$",cmd)
    if step:
        step_value=step.group(1).strip()
        if step_value:
            # if step value is just for title and not for args
            step_value=step_value.replace("\"","'")
            step_title=re.match(r"^'(.+)'$", step_value)
            if step_title:
                step_args=""
                step_value=step_title.group(1)
                cmd="{step} "+step_value
            else:
                step_value=re.sub(r"\s", " ",step_value)

                regex_authorized="[A-Za-z0-9_-]"
                for parameter in step_value.split(" "):
                    if not re.match(r"^[A-Za-z0-9_-]+$", parameter):
                        msg.user_error(
                            "Wrong parameter syntax for >> "+parameter+" <<",
                            "Authorized symbols are "+regex_authorized,
                            "Rename your parameters or surround the text with quotes to transform it into a step title only",
                            "Line:"+str(count_line)+" "+caller_filename
                        )
                        sys.exit(1)

                step_args=step_value

        conf["tmp"]["cmds_to_monitor"].append({
            "step": step_value.strip()
        })

    dep=re.match(r"^{dep}(.*)$",cmd)
    if dep:
        dep_value=dep.group(1).strip()
        if dep_value:
            dep_value_found=False
            for exec_cmd in conf["tmp"]["exec_cmds"]:
                step=re.match(r"^{step}(.*)$",exec_cmd)
                if step:
                    step_value=step.group(1).strip()
                    if step_value:
                        if step_value == dep_value:
                            dep_value_found=True
                            break

            if dep_value_found:
                return step_args
            else:
                msg.user_error(
                    "cmd depends on step '"+dep_value+"'",
                    "However step is not found or disabled",
                    "Line:"+str(count_line)+" "+caller_filename
                )
                sys.exit(1)

    this_cmd=re.match(r"^{cmd}(.*)$",cmd)
    if this_cmd:
        if this_cmd.group(1):
            msg.user_error(
                "{cmd} does not accept parameters '"+this_cmd.group(1).strip()+"'",
                "Line:"+str(count_line)+" "+caller_filename
            )
            sys.exit(1)

        if step_args:
            cmd=caller_filename+" "+step_args
        else:
            cmd=caller_filename

    cmd=replace_cmd_heredoc(conf, cmd)
            
    raw_cmd_to_monitor=re.match(r"^(_.+?):(.*)$", cmd)
    if raw_cmd_to_monitor:
        if not raw_cmd_to_monitor.group(2):
            if raw_cmd_to_monitor.group(1) == "_fail":
                fail_msg="blank"
                if index>0:
                    output_msg=re.match(r"^_out:(.*)$", cmds[index-1].strip())
                    if output_msg:
                        if output_msg.group(1):
                            fail_msg="See Output Above"
                conf["tmp"]["cmds_to_monitor"].append({
                    raw_cmd_to_monitor.group(1)[1:]: fail_msg
                })
            else:
                msg.user_error(
                    "cmd to monitor '"+raw_cmd_to_monitor.group(0)+"' has no value." ,
                    "Line:"+str(count_line)+" "+caller_filename
                )
                sys.exit(1)
        else:
            conf["tmp"]["cmds_to_monitor"].append({
                raw_cmd_to_monitor.group(1)[1:]: raw_cmd_to_monitor.group(2).strip()
            })
    else:
        conf["tmp"]["exec_cmds"].append(cmd)
        conf["tmp"]["cmds_line_num"].append(count_line)
        

    return step_args

def set_task_vars(conf, var_obj):
    frame,caller_filename,caller_line_number,function_name,lines,index=inspect.stack()[1]
    if not "cmd_vars" in conf["tmp"]:
        conf["tmp"]["cmd_vars"]={}

    for key in var_obj:
        if key in  ["cmd","step", "info", "dep"]:
            msg.user_error(
                "In file: "+str(caller_line_number)+" "+caller_filename,
                "key: '"+key+"' is a reserved keyword for processor_engine.",
                "Choose another key name."
            )
            sys.exit(1)

        conf["tmp"]['cmd_vars'].update({
            key: var_obj[key]
        })
