#!/bin/bash
PWD=`pwd`
echo $PWD
activate () {
    . $PWD/.venv/bin/activate
}

activate
uwsgi --ini uwsgi.ini