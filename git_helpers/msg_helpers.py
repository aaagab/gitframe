#!/usr/bin/env python3
import os
import re
import sys

from ..gpkgs.message import ft

def title(msg):
    print()
    print(ft.lGreen("  @@@@ ")+ft.bold(msg)+ft.lGreen(" @@@@"))
    print()

def subtitle(msg):
    print()
    ldeco="### "
    rdeco=""
    tmp_str=ldeco+msg+rdeco;
    print("  "+ft.lBlue(ldeco)+ft.bold(msg)+ft.lCyan(rdeco))
