#!/bin/bash

nmap -sP --host-timeout 1000 --max-retries 100 --dns-servers 192.168.2.3 192.168.2.* -oG n.tmp
echo "_______________________________"
while read line; do
    if [[ $line != "#"* ]]; then
        ip=$(echo $line | cut -f2 -d":" | cut -f2 -d" ")
        hostname=$(echo $line | cut -f2 -d"(" | cut -f1 -d")" )

        echo "nmap_scan{ip="$ip",hostname="$hostname"} 1"
    fi
done <n.tmp

# nmap_scan{ip="192.168.1.5",name="phone"} 1