#!/usr/bin/expect
set ipaddress "169.254.1.1"
set passwd "mars1bgm"
set timeout 30

spawn ssh root@$ipaddress 
expect {
	"yes/no" { send "yes\r";exp_continue}
        "password:" { send "$passwd\r";exp_continue};
	"imx8" { send "cd /log;tar -zcvf bgm_log.tar.gz ./*\r"}
}
expect eof

spawn scp -r root@169.254.1.1:/log/bgm_log.tar.gz .;

expect {
	"yes/no" { send "yes\r";exp_continue}
	"password:" { send "$passwd\r"};
}
expect eof
