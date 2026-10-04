#!/bin/sh
apt-get install -y net-tools
apt-get install -y curl
apt-get install -y usbrelay
apt-get install -y expect
apt-get install -y can-utils
apt-get install -y cmake
apt-get install -y minicom
apt-get install -y adb
apt-get install -y sshpass

# install java
apt-get install -y openjdk-17-jre-headless

pip config --global set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
pip config --global set install.trusted-host pypi.tuna.tsinghua.edu.cn
apt-get install -y nginx