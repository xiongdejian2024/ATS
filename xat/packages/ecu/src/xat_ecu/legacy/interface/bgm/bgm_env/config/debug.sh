#!/bin/sh


  source /data/app/etc/bgm_app_env.sh
  /app/etc/change_own.sh
  echo 1 > /proc/sys/net/ipv4/ip_forward

  echo "===>>start from runenv <<===" >/dev/kmsg

  chmod 755 /data
  chmod 775 /log /update /dev/kmsg
  chmod 664 /sys/class/gpio/export /sys/class/gpio/unexport /dev/mmcblk0* /dev/spidev*

  umask 0007

  file_path="/app/etc/build.prop"
  version_result=""
  if [ -f "$file_path" ]; then
    version_num_result=$(grep "sys.build.version.swpn=" "$file_path" | sed 's/.*=//; s/.*\(.\{3\}\)/\1/')
    version_alp_result=$(grep "sys.build.version.ver=" "$file_path" | awk -F "=" '{print $2}')
    version_result="_$version_num_result$version_alp_result"
  fi
  ulimit -c unlimited
  sysctl -w kernel.core_pattern=/log/coredump/core$version_result.%e.%p
  sysctl -w fs.suid_dumpable=2
  ip route add 239.255.0.1 dev lo
  ifconfig eth0.10 169.254.19.1 netmask 255.255.0.0 up
  resumed_path="/sys/power/sys_resumed"
  snapshotfile_path="/data/snapshot"
  mcubootmode_flag=$(LD_LIBRARY_PATH=/app/lib /app/bin/eoltest gpio 52|cut -d ' ' -f 4)
  if [[ $(cat "$resumed_path") == "0" && ! -e "$snapshotfile_path" ]]; then
    touch /tmp/startupflag /tmp/allappready /tmp/seco_startup_finish /tmp/s2s_startup_flag
    su - jetlogd -c "source /app/etc/bgm_app_env.sh load_env;umask 0007;/app/bin/jetlogd &"
    /app/bin/seco_daemon &
    /app/bin/vehInfoServer &

    if [[ "1" -eq "$mcubootmode_flag" ]]; then
      echo "==>>is in boot mode,skip start s2s<<==" >/dev/kmsg
    else
      echo "==>>startup s2s from runenv <<==" >/dev/kmsg
      #su - s2s_service -c "source /app/etc/bgm_app_env.sh load_env;umask 0007;/app/bin/s2s_service &"
      #sleep 1
    fi
  else
    systemctl start dropbear.socket
    /app/etc/s2d_mem_swap.sh &
  fi

  # start service_monitor for bootes service discovery
  su - service_monitor -c "source /app/etc/bgm_app_env.sh load_env;umask 0007;/app/bin/service_monitor  -c /data/app/etc/service_monitor.json &"
  if [[ $(cat "$resumed_path") == "0"  &&  ! -e "$snapshotfile_path" ]]; then
    sleep 1
    if [[ "1" -eq "$mcubootmode_flag" ]]; then
      echo "==>>is in boot mode,skip start SOAapp<<==" >/dev/kmsg
    else
      su - SOAApp -c "source /app/etc/bgm_app_env.sh load_env;umask 0007;/app/bin/SOAApp &"
      sleep 1
    fi
    su - jetcrashd -c "source /app/etc/bgm_app_env.sh load_env;umask 0007;/app/bin/jetcrashd &"
    su - diagd_iautosar -c "source /app/etc/bgm_app_env.sh load_env;umask 0007;/app/bin/diagd_iautosar &"
  else
    systemctl start dropbear.socket
  fi

  echo "==>>startup em2 from runenv <<==" >/dev/kmsg
  /app/bin/em2 &
  sleep 1
  /app/etc/monitor_em2.sh &

  while [ $(cat "$resumed_path") == "0" ]
  do
    usleep 500000
  done
  if [ -e /data/debug_s2d.sh ]; then
    source /data/debug_s2d.sh
  fi
  while true
  do
    usleep 5000000
  done
