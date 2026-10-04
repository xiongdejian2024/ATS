#!/usr/bin/expect -f
# work dir: sat/
set password "public_soa_bgm_tcam\r"
set user "public_soa_bgm_tcam\r"
set JIDLCompiler [lindex $argv 0]
set X86 [lindex $argv 1]
set idl [lindex $argv 2]
set timeout 600


cd ./ecu_simulator/soa_partner

cd ./BootesRelease

cd ./Tools
spawn git pull
expect {
        "Username" {send $user; exp_continue}
        "Password" {send $password; exp_continue}
        eof {send_user "eof"}
        }
spawn git checkout $JIDLCompiler
expect {eof {send_user "eof"}}

cd ../X86
spawn git pull
expect {
        "Username" {send $user; exp_continue}
        "Password" {send $password; exp_continue}
        eof {send_user "eof"}
        }
spawn git checkout $X86
expect {eof {send_user "eof"}}

cd ../idl
spawn git pull
expect {
        "Username" {send $user; exp_continue}
        "Password" {send $password; exp_continue}
        eof {send_user "eof"}
        }
spawn git checkout $idl
expect {eof {send_user "eof"}}
cd ./inter_idl
spawn git pull
expect {
        "Username" {send $user; exp_continue}
        "Password" {send $password; exp_continue}
        eof {send_user "eof"}
        }
