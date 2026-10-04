#!/bin/bash
ethn=$1
time=$(date -d +8hour +%k:%M:%S)
MemTotal=$(printf "%.1f" `cat /proc/meminfo | grep 'MemTotal' | awk '{print $2/1024}'`)
MemFree=$(printf "%.1f" `cat /proc/meminfo | grep 'MemFree' | awk '{print $2/1024}'`)
Active=$(printf "%.1f" `cat /proc/meminfo | grep 'Active:' | awk '{print $2/1024}'`)
eval $(vmstat | grep -v memory | grep -v free | awk 'END{printf("b_in=%s\nb_out=%s\nuser=%s\nsys=%s\nidle=%s",$9,$10,$13,$14,$15)}')
RX_pre=$(cat /proc/net/dev | grep $ethn | sed 's/:/ /g' | awk '{print $2}')
TX_pre=$(cat /proc/net/dev | grep $ethn | sed 's/:/ /g' | awk '{print $10}')
sleep 1
RX_next=$(cat /proc/net/dev | grep $ethn | sed 's/:/ /g' | awk '{print $2}')
TX_next=$(cat /proc/net/dev | grep $ethn | sed 's/:/ /g' | awk '{print $10}')
RX=$((${RX_next}-${RX_pre}))
TX=$((${TX_next}-${TX_pre}))
if [[ $RX -lt 1024 ]];then
  RX="${RX}"
  RX_unit="B/s"
elif [[ $RX -gt 1048576 ]];then
  RX=$(echo $RX | awk '{print $1/1048576}')
  RX_unit="MB/s"
else
  RX=$(echo $RX | awk '{print $1/1024}')
  RX_unit="KB/s"
fi
RX=$(printf "%.2f" `echo $RX`)
if [[ $TX -lt 1024 ]];then
  TX="${TX}"
  TX_unit="B/s"
elif [[ $TX -gt 1048576 ]];then
  TX=$(echo $TX | awk '{print $1/1048576}')
  TX_unit="MB/s"
else
  TX=$(echo $TX | awk '{print $1/1024}')
  TX_unit="KB/s"
fi
TX=$(printf "%.2f" $TX)
echo -e "$time" "$ethn" "$RX" "$TX" "$MemTotal" "$MemFree" "$Active" "$user" "$sys" "$idle" "$b_in" "$b_out"
df -h | grep -v Filesystem | grep mmcblk0p|sort -rn -k +5|head -3
