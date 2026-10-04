#!/bin/bash
echo $PWD
SystemType=`uname -m`
echo $SystemType
if [[ "$SystemType" == "x86_64" ]];then
export LD_LIBRARY_PATH="$PWD/libs/linux/x86_64:$LD_LIBRARY_PATH"
elif [[ "$SystemType" == "x86_32" ]];then
export LD_LIBRARY_PATH="$PWD/libs/linux/x86:$LD_LIBRARY_PATH"
elif [[ "$SystemType" =~ "armv6" ]];then
export LD_LIBRARY_PATH="$PWD/libs/linux/armv7:$LD_LIBRARY_PATH"
elif [[ "$SystemType" =~ "armv7" ]];then
export LD_LIBRARY_PATH="$PWD/libs/linux/armv7:$LD_LIBRARY_PATH"
elif [[ "$SystemType" =~ "armv8" ]];then
export LD_LIBRARY_PATH="$PWD/libs/linux/arm64:$LD_LIBRARY_PATH"
elif [[ "$SystemType" =~ "aarch64" ]];then
export LD_LIBRARY_PATH="$PWD/libs/linux/aarch64:$LD_LIBRARY_PATH"
elif [[ "$SystemType" =~ "mips64" ]];then
export LD_LIBRARY_PATH="$PWD/libs/linux/mips64:$LD_LIBRARY_PATH"
fi
echo $LD_LIBRARY_PATH
./${PWD##*/}
