#!/usr/bin/expect -f
set password "oelinux123\r"
set device "c5169e42"
set eth0 "ethtool eth0\r"
set timeout 100
set clear_tcam_log "rm -rf /mnt/sdcard/log/*"
spawn adb -s $device shell root

expect {
    "running as root" {exp_continue}
    "Passwd:" {send $password;exp_continue}
	"adb root success" {puts "eof, sleep 12s"; sleep 12}
	eof {send_user "eof"}
}

spawn adb -s $device shell $clear_tcam_log
expect {
        "Passwd:" {send $password;exp_continue}
        eof {send_user "eof"}
}


