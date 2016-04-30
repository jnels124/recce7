#!/bin/bash
ports_path="/etc/authbind/byport/"
ports=( "$@" )
config_file_ports=( )
run=true

if [ -z ${ports} ]; then
    ports="NULL"
    flag="NULL"
else
    honey_pot_pid=$(ps aux | grep '[p]ython3 -m framework.frmwork' | awk '{print $2}')
    if [ -n ${honey_pot_pid} ]; then
        echo "Shutting down the honeypot."
        kill $honey_pot_pid
    fi

    report_server_pid=$(ps aux | grep '[p]ython3 /home/mmcgui/recce7/reportserver/server/main.py' | awk '{print $2}')
    if [ -n ${report_server_pid} ]; then
        echo "Shutting down the report server."
        kill $report_server_pid
    fi

    flag=${ports[0]}

    for line in $(cat ./config/plugins.cfg)
    do
        regex="port = ([0-9]+)"
        if [[ $line =~ $regex ]]; then
            port="${BASH_REMATCH[1]}"
            config_file_ports+=($port)
        fi
    done
fi

if [ "$flag" == "--disable" -o "$flag" == "-d" ]; then

    if [ "${ports[1]}" == "ALL" ]; then
        echo "Removing ALL ports from: " $ports_path
        run=false
        ports=$config_file_ports
    fi
    
    for (( i=1; i<${#ports[@]}; i++ ))
    do
        echo "Removing: $ports_path${ports[$i]}"
        rm "$ports_path${ports[$i]}" 
    done

elif [ "$flag" == "--enable" -o "$flag" == "-e" ]; then
    if ["${ports[1]}" == "ALL"]; then
        echo "Enabling all ports found in plugins.cfg"
        ports=$config_file_ports
    else
        for (( i=1; i<${#ports[@]}; i++))
        do
            #TODO add ability to check if ports passed in exists in config, not critical
            echo "Setting up port: $ports_path${ports[$i]}"
            touch "$ports_path${ports[$i]}"
            chmod 755 "$ports_path${ports[$i]}"
            chown nobody "$ports_path${ports[$i]}"
            chgrp nogroup "$ports_path${ports[$i]}"
        done
    fi

    if ["$ports" == "NULL"]; then
        echo "You have passed in a flag to enable ports but have not passed in any ports as parameters."
        echo "If ports were previously opened the application will begin with those."
        echo "To setup ports for authbind please see the documentation located at http://recce7.github.io"
    fi
fi

if [ $run ]; then
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
else
    echo "All ports disabled, will not start honey pot."
fi
