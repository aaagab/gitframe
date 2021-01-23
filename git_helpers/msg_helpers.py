#!/usr/bin/env python3
import os
import re
import sys

try:
    from ..gpkgs.message import ft
except:
    direpa_script=os.path.realpath(__file__)
    direpa_launcher=os.path.dirname(direpa_script)
    sys.path.insert(0,direpa_launcher)
    from gpkgs.message import ft

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
