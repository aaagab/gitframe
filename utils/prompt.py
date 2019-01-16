#!/usr/bin/env python3
import sys
import utils.message as msg
import readline
# readline allows to use arrow keys and backspace when input text however there is a bug with tmux
# when text is wrapped some characters are eaten so I have to display first the text with print

def prompt(txt):
    tmp_var=""
    while not tmp_var:
        print("  "+txt +" [q to quit]: ", end="")
        tmp_var = input()
        if tmp_var.lower() == "q":
            sys.exit(1)
    return tmp_var.strip()

def prompt_boolean(txt, Y_N="y"):
    tmp_var=""
    while not tmp_var:
        if Y_N.lower() == "y":
            print(txt +" [Y/n/q]: ", end="")
            tmp_var = input()
            if tmp_var.lower() == "":
                return True
        elif Y_N.lower() == "n":
            print(txt +" [y/N/q]: ", end="")
            tmp_var = input()
            if tmp_var.lower() == "":
                return False
        else:
            msg.app_error("Wrong Value for prompt_boolean: "+Y_N )
            sys.exit(1)

        if tmp_var.lower() == "q":
            sys.exit(1)
        elif tmp_var.lower() == "y":
            return True
        elif tmp_var.lower() == "n":
            return False
    