#!/bin/sh
# work dir: ecu_simulator/
# cmd: ./tools/setup_env/set_gitconfig.sh "QuanSun" "quan.sun@jiduauto.com"

if [ ! $1 ]
then
    set username "QuanSun"
else
    username=$1
fi

if [ ! $2 ]
then
    set useremail "quan.sun@jiduauto.com"
else
    useremail=$2
fi

# set
git config --local user.name $username
git config --local user.email $useremail

# check
git config --local user.name
git config --local user.email

