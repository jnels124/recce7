#!/bin/bash
export RECCE7_OS_DIST=debian
export RECCE7_PLUGIN_CONFIG=/etc/recce7/configs/plugins.cfg
export RECCE7_GLOBAL_CONFIG=/etc/recce7/configs/global.cfg
export RECCE7_PATH=/usr/sbin/recce7/
cd $RECCE7_PATH
python3 -m framework.frmwork
