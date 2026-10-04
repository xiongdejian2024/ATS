#!/usr/bin/expect -f
# work dir: sat/
set password "public_soa_bgm_tcam\r"
set user "public_soa_bgm_tcam\r"
set JIDLCompiler [lindex $argv 0]
set X86 [lindex $argv 1]
set idl [lindex $argv 2]
set timeout 600


cd soa_partner

spawn mkdir -p BootesRelease/out/x86/bin BootesRelease/out/x86/conf BootesRelease/out/x86/log BootesRelease/X86 BootesRelease/Tools BootesRelease/idl
expect eof

cd BootesRelease

spawn git clone --depth 1 --single-branch -b $JIDLCompiler http://gerrit.jiduauto.com/SOA/BootesRelease/Tools_Utils Tools

expect {
        "Username" {send $user; exp_continue}
        "Password" {send $password; exp_continue}
        eof {send_user "eof"}
        }

spawn git clone --depth 1 --single-branch -b $X86 http://gerrit.jiduauto.com/a/SOA/BootesRelease/X86 X86
expect {
        "Username" {send $user; exp_continue}
        "Password" {send $password; exp_continue}
        eof {send_user "eof"}
        }

spawn git clone --depth 1 --single-branch -b $idl http://gerrit.jiduauto.com/SOA/idl idl
expect {
        "Username" {send $user; exp_continue}
        "Password" {send $password; exp_continue}
        eof {send_user "eof"}
        }

cd idl

spawn git clone -b bgm_master http://gerrit.jiduauto.com/SOA/jet/inter_idl
expect {
        "Username" {send $user; exp_continue}
        "Password" {send $password; exp_continue}
        eof {send_user "eof"}
        }
