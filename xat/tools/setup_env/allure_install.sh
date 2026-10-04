#!/usr/bin/expect -f
# work dir: sat/

set timeout 60

spawn scp root@172.18.128.5:/root/linuxzip/allure-2.19.0.zip /opt
expect {
    "password:" {send "jidu123\r"; exp_continue}
    "yes/no" {send "yes\r"; exp_continue}
    eof {send_user "eof"}
    }

cd /opt
spawn unzip -o allure-2.19.0.zip
expect {eof {send_user "eof"}}

