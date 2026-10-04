#!/usr/bin/expect -f
set password "oelinux123\r"
set device "c5169e42"
set eth0 "ethtool eth0\r"
set timeout 100
set tar_tcam_log "tar -zcvf /mnt/sdcard/log/tcam_log.tar.gz /mnt/sdcard/log/soa /mnt/sdcard/log/jidu /mnt/sdcard/log/diagd_iautosar/usrdata /umdp  /mnt/sdcard/log/mcu_log.txt /mnt/sdcard/log/backup/*  /mnt/sdcard/log/diagd_iautosar /mnt/sdcard/log/UDS*.dlt /mnt/sdcard/log/SUVS*.dlt"
spawn adb -s $device shell root

expect {
    "running as root" {exp_continue}
    "Passwd:" {send $password;exp_continue}
	"adb root success" {puts "eof, sleep 12s"; sleep 12}
	eof {send_user "eof"}
}

spawn adb -s $device shell $tar_tcam_log
expect {
        "Passwd:" {send $password;exp_continue}
        eof {send_user "eof"}
}
spawn adb -s $device pull /mnt/sdcard/log/tcam_log.tar.gz .
expect eof

