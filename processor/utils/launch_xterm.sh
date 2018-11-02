#!/bin/bash

function error()
{
    local msg=$1
    local path="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"
    echo "Error $msg"
    echo "At: $(caller)"
    echo "Path: $path"
    kill $$
}

test_window_name="$1"
TMPFILE="$2"
lock_title="$3"

if [ -z "$test_window_name" ]; then
    error "test_window_name is empty"
fi

if [ -z "$TMPFILE" ]; then
    error "TMPFILE is empty"
fi

cols=$(tput cols)
lines=$(tput lines)

if [ ! -z "$lock_title" ] && [ "$lock_title" == "lock_title" ]; then
    lock_title_str="-xrm xterm*allowTitleOps:false"
else
    lock_title_str=""
fi

{ xterm -title "$test_window_name" -sl 100000000 -ls -fa "DejaVu Sans Mono" -fs 10 \
$lock_title_str \
-xrm xterm*foreground:white \
-xrm xterm*background:black \
-xrm xterm*faceName:VeraMono \
-xrm xterm*faceSize:10 \
-xrm xterm*geometry:${cols}x$((lines+1)) \
-xrm XTerm*selectToClipboard:true \
-xrm xterm*ScrollBar:on \
-xrm xterm*ScrollBar:on \
-xrm *XTerm*scrollBar:true \
-xrm xterm*rightScrollBar:true \
-xrm xterm*multiScroll:on \
-xrm xterm*jumpScroll:on \
-e bash --rcfile "$TMPFILE" & \
} &> /dev/null
