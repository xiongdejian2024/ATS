#!/usr/bin/expect -f
# work dir: sat/test_case/xxx/
set password "public_soa_bgm_tcam\r"
set user "public_soa_bgm_tcam\r"
set soazippath [lindex $argv 0]
set timeout 600


cd ../../ecu_simulator/soa_partner

spawn scp root@172.18.128.5:/root/soazip/$soazippath/soa.zip ./
expect {
    "password:" {send "jidu123\r"; exp_continue}
    "yes/no" {send "yes\r"; exp_continue}
    eof {send_user "eof"}
    }

spawn unzip -o soa.zip
expect {eof {send_user "eof"}}

spawn rm soa.zip
expect {eof {send_user "eof"}}
