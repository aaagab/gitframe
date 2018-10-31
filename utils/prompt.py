#!/usr/bin/env python3
import sys
import utils.message as msg

def prompt(txt):
    tmp_var=""
    while not tmp_var:
        tmp_var = input("  "+txt +" [q to quit]: ")
        if tmp_var.lower() == "q":
            sys.exit(1)
    return tmp_var.strip()

def prompt_boolean(txt, Y_N="y"):
    tmp_var=""
    while not tmp_var:
        if Y_N.lower() == "y":
            tmp_var = input(txt +" [Y/n/q]: ")
            if tmp_var.lower() == "":
                return True
        elif Y_N.lower() == "n":
            tmp_var = input(txt +" [y/N/q]: ")
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
    