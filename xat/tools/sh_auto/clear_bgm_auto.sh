#!/usr/bin/expect
set ipaddress "169.254.1.1"
set passwd "mars1bgm"
set timeout 30

spawn ssh root@$ipaddress 
expect {
	"yes/no" { send "yes\r";exp_continue}
        "password:" { send "$passwd\r";exp_continue};
	"imx8" { send "rm -rf /log/*;sync;exit\r"}
}
expect eof

