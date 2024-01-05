#!/bin/bash
PWD=`pwd`
echo $PWD
activate () {
    . $PWD/.venv/bin/activate
}

activate
python3 stopRecording.py
deactivate