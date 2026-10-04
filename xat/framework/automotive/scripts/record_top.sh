#!/bin/bash
top_file="/data/top_files"
mkdir -p $top_file
cd $top_file
ls -t ${top_file}| tail -n +6 | xargs rm
current_date=$(date +%Y-%m-%d-%H_%M_%S)
while [ true ]; do
    top -b | head -n 30 >> $top_file/TOP$current_date.txt
    echo "-------------------------------------------------------------------------------" >> $top_file/TOP$current_date.txt
    sleep 1
done
