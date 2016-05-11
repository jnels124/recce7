#!/bin/sh

if which authbind > /dev/null; then
    touch recce7.log
    chmod 777 recce7.log
    mkdir -p ./honeyDB
    chmod 777 ./honeyDB
    sudo authbind ./recce7.sh
else
    echo "You don't seem to have authbind installed. Authbind is only available"
    echo "for Linux, and must be compiled from scratch in Cent OS. In Debian, you"
    echo "may install authbind by running"
    echo
    echo "    sudo apt-get install authbind"
    echo
fi

