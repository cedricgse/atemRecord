#!/bin/bash
PWD=`pwd`
echo $PWD
activate () {
    . $PWD/.venv/bin/activate
}

activate
python3 startRecording.py $1 "$2"
deactivate