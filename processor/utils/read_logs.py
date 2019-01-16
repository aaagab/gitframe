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

def read_logs(conf, log_files):
    file_full_path=[]
    for log_file in log_files:
        file_full_path.append(os.path.join(conf["direpa_logs"],log_file))
        logs=""
        with open(file_full_path[-1]) as file:
            for line in file:

                # remove any scroll delete
                if "\ec\e[3J" in line:
                    continue

                # change absolute ansii escape position to relative
                line=re.sub(r"\x1b\[\d+;(\d+)H","\x1b["+r"\1C",line)
                # remove hidden scroll delete
                line=re.sub(r"\x1bc\x1b\[3J","",line)
                logs+=line

        with open(file_full_path[-1], "w") as f:
            f.write(logs)

    with open(conf["filenpa_read_log_bashrc"], "w") as f:
        f.write("source ~/.bashrc\n")
        for file in sorted(file_full_path):
            f.write("echo\n")
            f.write("echo \"===============================================================\"\n")
            f.write("echo \"   "+os.path.basename(file)+"\"\n")
            f.write("echo \"===============================================================\"\n")
            f.write("cat \""+file+"\"\n")
        f.write("echo\n")

    os.chmod(conf["filenpa_read_log_bashrc"], 0o755)

    cmd=re.sub(r"\n\s*", "\n","""
        tmux select-pane -t 1
        tmux swap-pane -s gitframe:1.0
        tmux send-keys -t 1 'echo -en "\ec\e[3J"'
        tmux send-keys -t 1 KPEnter
        tmux send-keys -t 1 "{cmd}"
        tmux send-keys -t 1 KPEnter
        tmux select-pane -t 0
        tmux set -g status-bg red
    """.format(
        task_name=conf["task_name"],
        cmd=conf["filenpa_read_log_bashrc"]
    )
    )[1:-1]
    os.system(cmd)
    