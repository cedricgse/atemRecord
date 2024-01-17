#!/bin/bash
PWD=`pwd`
echo $PWD
activate () {
    . $PWD/.venv/bin/activate
}

sleep 5 # To make stopping recording A and starting recording B at same minute possible
activate
python3 startRecording.py $1 "$2"
deactivate