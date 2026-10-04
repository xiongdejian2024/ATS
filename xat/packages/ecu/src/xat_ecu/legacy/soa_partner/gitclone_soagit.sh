#!/usr/bin/expect -f
# work dir: sat/ ecu_simulator/soa_partner  部署环境，只用一次
set password "public_soa_bgm_tcam\r"
set user "public_soa_bgm_tcam\r"
set timeout 600


spawn git clone http://gerrit.jiduauto.com/SOA/ApusRelease/JIDLCompiler
expect {
        "Username" {send $user; exp_continue}
        "Password" {send $password; exp_continue}
        eof {send_user "eof"}
        }

spawn git clone http://gerrit.jiduauto.com/SOA/ApusRelease/X86
expect {
        "Username" {send $user; exp_continue}
        "Password" {send $password; exp_continue}
        eof {send_user "eof"}
        }

spawn git clone http://gerrit.jiduauto.com/SOA/idl
expect {
        "Username" {send $user; exp_continue}
        "Password" {send $password; exp_continue}
        eof {send_user "eof"}
        }
cd ./idl
spawn git clone http://gerrit.jiduauto.com/SOA/jet/inter_idl
expect {
        "Username" {send $user; exp_continue}
        "Password" {send $password; exp_continue}
        eof {send_user "eof"}
        }

cd ..
mkdir BootesRelease
cd ./BootesRelease

spawn git clone "http://gerrit.jiduauto.com/a/SOA/BootesRelease/X86"
expect {
        "Username" {send $user; exp_continue}
        "Password" {send $password; exp_continue}
        eof {send_user "eof"}
        }

# spawn git clone "http://gerrit.jiduauto.com/a/SOA/BootesRelease/Tools"
spawn git clone "https://gerrit.jiduauto.com/plugins/gitiles/SOA/BootesRelease/Tools_Utils"
expect {
        "Username" {send $user; exp_continue}
        "Password" {send $password; exp_continue}
        eof {send_user "eof"}
        }
mv ./Tools_Utils/ ./Tools/

spawn git clone http://gerrit.jiduauto.com/SOA/idl
expect {
        "Username" {send $user; exp_continue}
        "Password" {send $password; exp_continue}
        eof {send_user "eof"}
        }
cd ./idl
spawn git clone http://gerrit.jiduauto.com/SOA/jet/inter_idl
expect {
        "Username" {send $user; exp_continue}
        "Password" {send $password; exp_continue}
        eof {send_user "eof"}
        }