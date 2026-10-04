#!/bin/bash
vmstat_file="/data/vmstat_files"
mkdir -p $vmstat_file
cd $vmstat_file
ls -t ${vmstat_file}| tail -n +6 | xargs rm
current_date=$(date +%Y-%m-%d-%H_%M_%S)
while [ true ]; do
    vmstat 2 10 -t >> $vmstat_file/VM$current_date.txt
    echo "-------------------------------------------------------------------------------" >> $vmstat_file/TOP$current_date.txt
    sleep 1
done
