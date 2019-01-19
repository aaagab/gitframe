#!/usr/bin/env python3
import os, sys
if __name__ != "__main__":
    from processor.utils.processor_engine import start_processor, set_task_steps, set_task_vars
    
def init_readline_screen(conf):

    set_task_steps(conf,"""
      {cmd}
      _out:init readline
      _out:\033[K
    """)

    start_processor(conf)

if __name__ == "__main__":
    direpa_script=os.path.realpath(__file__)
    while os.path.basename(direpa_script) != "processor":
        direpa_script=os.path.dirname(direpa_script)
    sys.path.insert(0,os.path.dirname(direpa_script))

    import readline
    import sys, select

    print("init readline",end="")
    i, o, e = select.select( [sys.stdin], [], [], .3 )
    print()
    print("\033[K")
    del readline
