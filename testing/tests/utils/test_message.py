#!/usr/bin/env python3
import os, sys
if __name__ != "__main__":
    from testing.utils.test_processor import test_processor, set_test_steps, set_test_vars

def test_message(conf):
    set_test_steps(conf, """
        {cmd}
        _fail:user_error
    """)

    test_processor(conf)

if __name__ == "__main__":
    direpa_script=os.path.realpath(__file__)
    while os.path.basename(direpa_script) != "testing":
        direpa_script=os.path.dirname(direpa_script)
    sys.path.insert(0,os.path.dirname(direpa_script))

    import utils.message as msg

    msg.title("This is a title")
    msg.subtitle("This is a subtitle")

    txt="info"
    msg.info("This is a single-line "+txt+"\n")
    msg.info(
        "This is a multi-line "+txt,
        "This is a multi-line "+txt,
        "This is a multi-line "+txt,
        "This is a multi-line "+txt+"\n",
    )

    txt="warning"
    msg.warning("This is a single-line "+txt+"\n")
    msg.warning(
        "This is a multi-line "+txt,
        "This is a multi-line "+txt,
        "This is a multi-line "+txt,
        "This is a multi-line "+txt+"\n",
    )

    txt="success"
    msg.success("This is a single-line "+txt+"\n")
    msg.success(
        "This is a multi-line "+txt,
        "This is a multi-line "+txt,
        "This is a multi-line "+txt,
        "This is a multi-line "+txt+"\n",
    )

    txt="user_error"
    msg.user_error("This is a single-line "+txt+"\n")
    msg.user_error(
        "This is a multi-line "+txt,
        "This is a multi-line "+txt,
        "This is a multi-line "+txt,
        "This is a multi-line "+txt+"\n",
    )

    txt="app_error"
    # msg.app_error("This is a single-line "+txt+"\n")
    msg.app_error(
        "This is a multi-line "+txt,
        "This is a multi-line "+txt,
        "This is a multi-line "+txt,
        "This is a multi-line "+txt+"\n",
    )
