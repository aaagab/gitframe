#!/usr/bin/env python3
import os
import subprocess
import shlex
import sys
import utils.message as msg
from utils.format_text import Format_text as ft
import utils.shell_helpers as shell
import re
import tempfile
import time

def read_log(conf, log_files):
    file_full_path=[]
    for log_file in log_files:
        file_full_path.append(os.path.join(conf["direpa_logs"],log_file))
        logs=""
        with open(file_full_path[-1]) as file:
            for line in file:

                # remove any scroll delete
                if "\ec\e[3J" in line:
                    continue

                # remove line when launching cmds script 
                # if conf["direpa_cmds"] in line:
                #     continue
                
                # change absolute ansii escape position to relative
                line=re.sub(r"\x1b\[\d+;(\d+)H","\x1b["+r"\1C",line)
                # remove hidden scroll delete
                line=re.sub(r"\x1bc\x1b\[3J\x1b","",line)
                logs+=line

        with open(file_full_path[-1], "w") as f:
            f.write(logs)

    with open(conf["filenpa_read_log_bashrc"], "w") as f:
        f.write("source ~/.bashrc\n")
        f.write("stty -echo\n")
        for file in sorted(file_full_path):
            f.write("echo\n")
            f.write("echo \"===============================================================\"\n")
            f.write("echo \"   "+os.path.basename(file)+"\"\n")
            f.write("echo \"===============================================================\"\n")
            f.write("cat \""+file+"\"\n")
        f.write("echo\n")
        f.write("read -p \"Press Enter to Exit\"\n")
        f.write("stty echo\n")
        f.write("exit\n")

    command=conf["filenpa_xterm"]+" \""+conf["read_log_window_title"]+"\" \""+conf["filenpa_read_log_bashrc"]+"\" lock_title &"

    import testing.utils.test_helpers as th

    th.window_set_above(conf["launching_window_hex_id"])

    if subprocess.call(shlex.split(command)) != 0:
        msg.user_error(command)
        sys.exit(1)

    timer=th.Time_out(3)
    while True:
        if conf["read_log_window_title"] in shell.cmd_get_value("wmctrl -l"):
            time.sleep(.5)
            break
        
        if timer.has_ended():
            print("exit")
            break
    
        th.window_focus(conf["launching_window_hex_id"])

    th.window_unset_above(conf["launching_window_hex_id"])
    th.window_focus(conf["current_window_hex_id"])

