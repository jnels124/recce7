#!/bin/bash
export PYTHONPATH=${PYTHONPATH}:$PWD/reportserver/
echo $PYTHONPATH
python3 $PWD/reportserver/server/main.py
