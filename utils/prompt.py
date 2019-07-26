#!/usr/bin/env python3
import os
import sys

from ..gpkgs import message as msg

# import utils.shell_helpers as shell
# readline allows to use arrow keys and backspace when input text however there is a bug with tmux
# when text is wrapped some characters are eaten so I have to display first the text with print,
# I abandonned this alternative I just try to prompt shorter sentence.
# then there is also another bug that eat the print text if no newline when readline is init for the first time in a screen session inside a tmux session.


def prompt(txt):
    tmp_var=""
    while not tmp_var:
        tmp_var=get_input("  "+txt +" [q to quit]: ")
        if tmp_var.lower() == "q":
            sys.exit(1)
    return tmp_var.strip()

def get_input(text):
    # import readline # removed because not installed on windows and I am not sure about linux anymore.
    tmp_var=input(text)
    # del readline
    return tmp_var

def prompt_boolean(txt, Y_N="y"):
    tmp_var=""
    while not tmp_var:
        if Y_N.lower() == "y":
            tmp_var=get_input(txt +" [Y/n/q]: ")
            if tmp_var.lower() == "":
                return True
        elif Y_N.lower() == "n":
            tmp_var=get_input(txt +" [y/N/q]: ")
            if tmp_var.lower() == "":
                return False
        else:
            msg.error("Wrong Value for prompt_boolean: "+Y_N )
            sys.exit(1)

        if tmp_var.lower() == "q":
            sys.exit(1)
        elif tmp_var.lower() == "y":
            return True
        elif tmp_var.lower() == "n":
            return False
        else:
            tmp_var=""
    