from utils.format_text import Format_text as ft
import traceback
import inspect, sys

def app_error(*msgs):
    if len(msgs) == 1:
        print(ft.error("".join(msgs)))
    else:
        for msg in msgs:
            print(ft.error(""+msg))
    frame,filename,line_number,function_name,lines,index=inspect.stack()[1]
    print("\t"+str(line_number)+": "+filename)
    print(traceback.format_exc())
    sys.exit(1)

def user_error(*msgs):
    if len(msgs) == 1:
        print(ft.error("".join(msgs)))
    else:
        for msg in msgs:
            print(ft.error(""+msg))

def success(*msgs):
    if len(msgs) == 1:
        print(ft.success("".join(msgs)))
    else:
        for msg in msgs:
            print(ft.success(""+msg))

def warning(*msgs):
    if len(msgs) == 1:
        print(ft.warning("".join(msgs)))
    else:
        for msg in msgs:
            print(ft.warning(""+msg))

def info(*msgs):
    if len(msgs) == 1:
        print(ft.info("".join(msgs)))
    else:
        for msg in msgs:
            print(ft.info(""+msg))


def raw_print(msg):
    print(msg)

def draw_line(char, n):
    tmp_str=""
    for i in range(0, n):
        tmp_str+=char

    return tmp_str

def title(msg):
    char="="
    len_title=len(msg)
    margin_out_len=5
    border_len=1
    margin_in_len=1

    dmo=draw_line(" ", margin_out_len)
    db=draw_line("|", border_len)
    dmi=draw_line(" ", margin_in_len)

    frame_len= \
    border_len + \
    margin_in_len + \
    len_title + \
    margin_in_len + \
    border_len

    line=draw_line(char, frame_len)

    title=(
        line,
        db+dmi+msg+dmi+db,
        line
    )

    print()
    for i, s in enumerate(title):
        ft.center(s)
        if i == 1:
            print(ft.bold(s))
        else:
            print(s)

    # print()

def subtitle(msg):
    print()
    ldeco="-->> # "
    rdeco=" # <<--"
    tmp_str=ldeco+msg+rdeco;
    ft.center(tmp_str)
    print(ft.lCyan(ldeco)+ft.bold(msg)+ft.lCyan(rdeco))
    # print()

def dbg(funct, *msgs):
    from utils.json_config import Json_config
    conf = Json_config()
    if conf.get_value("debug"):
        globals()[funct](*msgs)
