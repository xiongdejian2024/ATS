#!/bin/bash
check_command_status() {
  $@
  exit_status=$?

  if [ $exit_status -eq 0 ]; then
    echo "命令返回值为$exit_status"
    echo "$@执行成功"
  else
    echo "$@执行失败，脚本退出"
    exit 1
  fi
}
#cd soa_partner
#check_command_status "./BootesRelease/Tools/bin/soa_partner -r ./BootesRelease/idl/inter_idl -s ./BootesRelease/X86 build"
#cd -

function unzip_recursively() {
    unzip -o soa.zip -d soa
    cd soa/*
    for file in *.zip; do
      # 解压文件
      unzip -o "$file"
      # 删除原始zip文件
      rm "$file"
    done
    cp -rf * ../../x86/bin/
    rm -rf ../../soa*
}
check_command_status "cp -rf soa_partner/conf soa_partner/BootesRelease/out/x86/"
#check_command_status "cp -rf soa_partner/BootesRelease/idl/inter_idl/out/x86/bin/* soa_partner/BootesRelease/out/x86/bin/"
cd soa_partner/BootesRelease/out
# 解压和打包soa partner服务
unzip_recursively
cd ../../../../
pwd
check_command_status "zip -r soa.zip BootesRelease/X86/include BootesRelease/X86/lib BootesRelease/X86/bin BootesRelease/Tools/bin BootesRelease/idl/ BootesRelease/out/x86/conf BootesRelease/out/x86/bin"
if [ ! -d "$1" ]; then
    mkdir -p "$1"
fi
mv soa.zip $1
