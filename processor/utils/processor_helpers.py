#!/usr/bin/env python3
import subprocess
import shlex
import sys
from shutil import copyfile
from datetime import datetime
import utils.message as msg
import os
import getpass
import utils.shell_helpers as shell
from utils.json_config import Json_config
from pprint import pprint
import shutil
from processor.utils.read_logs import read_logs
import uuid
import time
import stat
import git_helpers.git_utils as git
from processor.utils.task_clean import delete_test_and_repo

def get_active_window_dec_id():
    dec_id=shell.cmd_get_value("xdotool getactivewindow")
    if not dec_id:
        msg.app_error("Can't get window_id")
        sys.exit(1)
    else:
        return dec_id

def get_active_window_hex_id():
    return hex(int(get_active_window_dec_id()))

def get_win_dec_id_by_name(name):
    out=subprocess.check_output(shlex.split('wmctrl -l'))
    for line in out.decode("utf-8").strip().splitlines():
        print(name)
        print(line)
        if name in line:
            hex_id=line.split(" ")[0]
            dec_id=int(hex_id, 16)
            
            return dec_id

def window_set_above(window_hex_id):
    shell.cmd("wmctrl -i -r "+window_hex_id+" -b add,above")

def window_focus(window_hex_id):
    shell.cmd("wmctrl -i -a "+window_hex_id)

def window_unset_above(window_id):
    shell.cmd("wmctrl -i -r "+window_id+" -b remove,above")

def send_cmd_to_screen(session_name, cmd):
    shell.cmd("screen -S '"+session_name+"' -X stuff '"+cmd+"^M'")

def kill_screen_session(session_name):
    timer=Time_out(3)
    for session_item in shell.cmd_get_value("screen -ls").splitlines():
        if session_name in session_item:
            # session_pid=session_item.strip().split(".")[0]
            full_session_name=session_item.strip().split()[0]
            shell.cmd("screen -X -S '{}' quit".format(full_session_name))
            # screen -X -S [session # you want to kill] quit
        #     # try to correct bug hard to reproduce with dead screen
        #     while session_item in shell.cmd_get_value("screen -ls"):
        #         shell.cmd("kill "+session_pid)
        #         if timer.has_ended():
        #             msg.app_error("Can't kill '"+session_item+"'")
        #             sys.exit(1)
    # sys.exit(1)

def open_logs(conf):
    log_files=os.listdir(conf["direpa_logs"])
    if log_files:
        read_logs(conf, log_files)

def clean_logs(conf):
    directory = conf["direpa_logs"]
    files=os.listdir(directory)
    if files:
        msg.info("Clean Log Files")
        for this_file in files:
            file_path = os.path.join(directory, this_file)
            if os.path.isfile(file_path):
                os.unlink(file_path)

    # kill any log window already open
    os.system('wmctrl -c \"'+conf["read_log_window_title"]+'\"')

def log(conf):
    src_file=conf["filenpa_screen_log"]
    dst_path=conf["direpa_logs"]
    test_name=conf['tmp']['test_name']
    
    prefix="{:%Y%m%d-%H%M%S%f}".format(datetime.now())[:-4]
    dst_file=os.path.join(dst_path,prefix+"-"+test_name+".txt")
    copyfile(src_file, dst_file)

# def ssh_cmd(conf, sudo_pass, cmd):
#     ssh_user=conf["remote"]["ssh_user"]
#     domain=conf["remote"]["domain"]
#     ssh_url=ssh_user+"@"+domain

def get_file_user_obj(passwd_file):
    file_user_obj={}
    with open(passwd_file) as file:
        for line in file:
            file_user_obj.update({
                line.split(":")[0]:{
                    "name":line.split(":")[0],
                    "uid":line.split(":")[2],
                    "gid":line.split(":")[3],
                    "home_path":line.split(":")[5],
                    "shell":line.split(":")[6].rstrip()
                }
            })

    return file_user_obj

def enable_sudo(sudo_pass_obj):
    p = subprocess.Popen(shlex.split('sudo -p "" ls'))
    try:
        p.wait(.1)
    except:
        p.kill()
        os.system("stty sane")

        sudo_pass=sudo_pass_obj.get_sudo_pass()

        cmd="""pass=$(cat<<'EOF'
            {}
            EOF
            )
        """.format(sudo_pass).replace(" ","")

        if os.system(cmd+' echo $pass | sudo -S -p "" echo -n') != 0:
            msg.user_error("Wrong pass")
            sys.exit(1)

def setup_mock_repository(conf):  
    msg.subtitle("Setup remote repository for testing")

    user_git=conf["remote"]["user_git"]

    # create  test path
    try:
        os.makedirs(conf["direpa_testgf"], exist_ok=True)
        os.chdir(conf["direpa_testgf"])
    except:
        msg.app_error("Cannot create "+conf["direpa_testgf"])
        sys.exit(1)

    # create remote path
    try:
        os.makedirs(conf["remote"]["direpa_src"], exist_ok=True)
    except:
        msg.app_error("Cannot create "+conf["remote"]["direpa_src"])
        sys.exit(1)

    passwd_file="/etc/passwd"
    if not os.path.exists(passwd_file):
        msg.user_error("{} does not exist or is not accessible.".format(passwd_file))
        sys.exit(1)

    shells_file="/etc/shells"
    if not os.path.exists(shells_file):
        msg.user_error("{} does not exist or is not accessible.".format(shells_file))
        sys.exit(1)

    group_file="/etc/group"
    if not os.path.exists(shells_file):
        msg.user_error("{} does not exist or is not accessible.".format(shells_file))
        sys.exit(1)

    file_user_obj=get_file_user_obj(passwd_file)
    current_user_obj=file_user_obj[getpass.getuser()]
    current_user_and_group="{}:{}".format(current_user_obj["name"], current_user_obj["name"])
    
    with open(shells_file) as file:
        git_shell_path="/usr/bin/git-shell"
        if not git_shell_path in file.read():
            shell.cmd_prompt("sudo sh -c \"echo '{}' >> {}\"".format(git_shell_path, shells_file))

    if not user_git in file_user_obj:
        msg.warning("user_git {} does not exist".format(user_git))
        shell.cmd_prompt("sudo adduser {}".format(user_git))
        file_user_obj=get_file_user_obj(passwd_file)
        
    user_git_obj=file_user_obj[user_git]
    
    if user_git_obj["shell"] != git_shell_path:
        shell.cmd_prompt("sudo chsh -s {} {}".format(git_shell_path, user_git))

    user_git_ssh_path=os.path.join(user_git_obj["home_path"], ".ssh")

    current_user_ssh_file=os.path.join(current_user_obj["home_path"], ".ssh", "id_rsa.pub")

    current_user_ssh_str=""
    while not current_user_ssh_str:
        if not os.path.exists(current_user_ssh_file):
            shell.cmd_prompt("ssh-keygen -t rsa")
        else:
            with open(current_user_ssh_file) as file:
                current_user_ssh_str=file.read().strip()

            if not current_user_ssh_str:
                shell.cmd_prompt("ssh-keygen -t rsa")

    if not os.path.exists(user_git_ssh_path):
        shell.cmd_prompt("sudo mkdir "+user_git_ssh_path)

    git_ssh_directory_obj=os.stat(user_git_ssh_path)
    git_ssh_directory_chmod=oct(git_ssh_directory_obj.st_mode)[-3:]
    git_ssh_directory_uid=str(git_ssh_directory_obj.st_uid)
    git_ssh_directory_gid=str(git_ssh_directory_obj.st_gid)
    user_git_and_group="{}:{}".format(user_git_obj["name"], user_git_obj["name"])

    if git_ssh_directory_chmod != "700":
        shell.cmd_prompt("sudo chmod -R 700 '"+user_git_ssh_path+"'")

    if git_ssh_directory_uid != user_git_obj["uid"] or \
        git_ssh_directory_gid != user_git_obj["gid"]:
        shell.cmd_prompt("sudo chown -R {} '{}'".format(user_git_and_group, user_git_ssh_path))

    ssh_cmd_txt="ssh -o PasswordAuthentication=no {} test_ssh".format(conf["remote"]['user_ip'])
    ssh_cmds_path=os.path.join(user_git_obj['home_path'], "git-shell-commands")
    shell_cmd_script=os.path.join(ssh_cmds_path, 'test_ssh')

    if shell.cmd_devnull(ssh_cmd_txt) != 0:
        shell.cmd_prompt("sudo mkdir -p {}".format(ssh_cmds_path))
        shell.cmd_prompt("sudo sh -c \"echo '#!/bin/sh' > {}\"".format(shell_cmd_script))
        shell.cmd_prompt("sudo chown -R {} '{}'".format(user_git_and_group, ssh_cmds_path))
        shell.cmd_prompt("sudo chmod +x '{}'".format(shell_cmd_script))

    user_git_ssh_file=os.path.join(user_git_ssh_path, "authorized_keys")


    if shell.cmd_devnull(ssh_cmd_txt) != 0:
        if shell.cmd("sudo [ -f {} ]".format(user_git_ssh_file)) != 0 :
            shell.cmd_prompt("sudo sh -c \"echo '{}' > {}\"".format(current_user_ssh_str, user_git_ssh_file))

        git_authorized_keys_str=shell.cmd_get_value("sudo cat '{}'".format(user_git_ssh_file).strip())
        if not "current_user_ssh_str" in git_authorized_keys_str:
            shell.cmd_prompt("sudo sh -c \"echo '{}' > {}\"".format(current_user_ssh_str, user_git_ssh_file))

        if shell.cmd_get_value("sudo stat --format '%a' '{}'".format(user_git_ssh_file).strip()) != "644":
            shell.cmd_prompt("sudo chmod 644 '"+user_git_ssh_file+"'")

        stat_user_and_group=shell.cmd_get_value("sudo stat --format '%U:%G' '{}'".format(user_git_ssh_file).strip())
        if  stat_user_and_group != user_git_and_group:
            shell.cmd_prompt("sudo chown {} '{}'".format(user_git_and_group, ssh_cmds_path))

    print(ssh_cmd_txt)
    if shell.cmd_devnull(ssh_cmd_txt) != 0:
        msg.user_error("ssh not connecting: unknown error")
        sys.exit(1)

    if conf["mode"] == "local_path":
        user_and_group_root_dir=shell.cmd_get_value("sudo stat --format '%U:%G' '{}'".format(conf["remote"]["direpa_src"]).strip())
        if user_and_group_root_dir != current_user_and_group:
            shell.cmd_prompt("sudo chown -R {} '{}'".format(current_user_and_group, conf["remote"]["direpa_src"]))

class Sudo_pass():
    def __init__(self):
        self.sudo_pass=""
        self.count=0

    def get_sudo_pass(self):
        if self.count == 0:
            if not self.sudo_pass:
                self.sudo_pass=getpass.getpass("Sudo Password: ")
                self.count+=1

        return self.sudo_pass

class Time_out():
    import time
    def __init__(self, seconds, sleep_time=0.001):
        self.waiting_time=seconds
        self.start_time = time.time()
        self.sleep_time=sleep_time

    def has_ended(self):
        elapsed_time = time.time() - self.start_time
        if elapsed_time >= self.waiting_time:
            return True
        else:
            time.sleep(self.sleep_time)
            return False
