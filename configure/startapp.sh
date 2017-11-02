#!/bin/sh
export PATH=$PATH:/home/lepython/work/venv_py3/bin
source /home/lepython/work/venv_py3/bin/activate
/home/lepython/work/venv_py3/bin/uwsgi --ini `pwd`/runapp.ini
