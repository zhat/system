#!/bin/sh
source /home/lepython/work/venv_py3/bin/activate
uwsgi --ini `pwd`/runapp.ini

