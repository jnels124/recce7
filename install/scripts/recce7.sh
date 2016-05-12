#!/bin/bash
RECCE7_DB=/usr/lib/recce7/honeyDB/
RECCE7_LOG=/usr/sbin/recce7/recce7.log

if [ ! -d "$RECCE7_DB" ]; then
    mkdir -p $RECCE7_DB
    chmod 777 $RECCE7_DB
fi

if [ ! -a "$RECCE7_LOG" ]; then
    touch $RECCE7_LOG
    chmod 666 $RECCE7_LOG
fi

export RECCE7_OS_DIST=debian
export RECCE7_PLUGIN_CONFIG=/etc/recce7/configs/plugins.cfg
export RECCE7_GLOBAL_CONFIG=/etc/recce7/configs/global.cfg
export RECCE7_PATH=/usr/sbin/recce7/
cd $RECCE7_PATH
python3 -m framework.frmwork