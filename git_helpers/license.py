#!/usr/bin/env python3
import datetime
import os
import sys

from ..gpkgs import message as msg

from ..utils.prompt import prompt
from ..utils.format_text import Format_text as ft

def remove_tabs_heredoc(text):
    new_text=""
    for line in text.splitlines()[1:-1]:
        new_text+=line.lstrip()+"\n"
    
    return new_text

def mit():
    msg.info("Preparing License MIT")
    
    now = datetime.datetime.now()
    copyright_holders=prompt("Copyright Holders: ")

    text="""
        Copyright (c) {year} {copyright_holders}

        Permission is hereby granted, free of charge, to any person obtaining a copy
        of this software and associated documentation files (the "Software"), to deal
        in the Software without restriction, including without limitation the rights
        to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
        copies of the Software, and to permit persons to whom the Software is
        furnished to do so, subject to the following conditions:

        The above copyright notice and this permission notice shall be included in all
        copies or substantial portions of the Software.

        THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
        IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
        FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
        AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
        LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
        OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
        SOFTWARE.
    """.format(year=now.year, copyright_holders=copyright_holders)

    return remove_tabs_heredoc(text)


def get_license_content():
    licenses=[
        "MIT"
    ]

    menu="\n"

    for i, lic in enumerate(licenses):
        menu+="    "+str(i+1)+" => "+lic+"\n"

    menu+="\n"
    menu+="    Choose a License.\n"
    menu+="    choice or 'q' to quit: "

    user_choice=""
    while not user_choice:
        isValid=True
        user_choice = input(menu)
        if user_choice.isdigit():
            if int(user_choice) >= 1 and int(user_choice) <= len(licenses):
                selected_license=licenses[int(user_choice)-1]
                if  selected_license == "MIT":
                    print()
                    return mit()

                    break
            else:
                isValid=False
        elif user_choice.lower() == "q":
            sys.exit(1)
        else:
            isValid=False

        if not isValid:
            msg.warning("Wrong input")
            input("  Press Enter To Continue...")
            user_choice=""