#!/bin/bash

SWITCH_BASE_PATH=$(cd "$(dirname "${BASH_SOURCE[0]}")"; pwd)

TOOL=$SWITCH_BASE_PATH/DownloadImage

INTERFACE=$1
FW=$2
SWITCH_ADDR=$3
DN=$4

$TOOL -ii$INTERFACE -gc




$TOOL -ii$INTERFACE -if$FW -dt2 -io0x0B0000 -is0x50000 -da02-00-00-00-00-$SWITCH_ADDR -dn$DN 
if [ "$?" != 0 ]; then
    sleep 1
    $TOOL -ii$INTERFACE -if$FW -dt2 -io0x0B0000 -is0x50000 -da02-00-00-00-00-$SWITCH_ADDR -dn$DN 
    if [ "$?" != 0 ]; then
        exit 1
    fi
fi


$TOOL -ii$INTERFACE -if$FW -dt1 -io0x030000 -is0x7d000 -da02-00-00-00-00-$SWITCH_ADDR -dn$DN 
if [ "$?" != 0 ]; then
    sleep 1
    $TOOL -ii$INTERFACE -if$FW -dt1 -io0x030000 -is0x7d000 -da02-00-00-00-00-$SWITCH_ADDR -dn$DN 
    if [ "$?" != 0 ]; then
        exit 1
    fi
fi
$TOOL -ii$INTERFACE -if$FW -dt5 -io0x12000 -is0x1E000 -da02-00-00-00-00-$SWITCH_ADDR -dn$DN 
if [ "$?" != 0 ]; then
    sleep 1
    $TOOL -ii$INTERFACE -if$FW -dt5 -io0x12000 -is0x1E000 -da02-00-00-00-00-$SWITCH_ADDR -dn$DN 
    if [ "$?" != 0 ]; then
        exit 1
    fi
fi
$TOOL -ii$INTERFACE -if$FW -dt3 -io0x10000 -is0x2000 -da02-00-00-00-00-$SWITCH_ADDR -dn$DN 
if [ "$?" != 0 ]; then
    sleep 1
    $TOOL -ii$INTERFACE -if$FW -dt3 -io0x10000 -is0x2000 -da02-00-00-00-00-$SWITCH_ADDR -dn$DN 
    if [ "$?" != 0 ]; then
        exit 1
    fi
fi

$TOOL -ii$INTERFACE -if$FW -dt2 -io0x1A0000 -is0x50000 -da02-00-00-00-00-$SWITCH_ADDR -dn$DN 
if [ "$?" != 0 ]; then
    sleep 1
    $TOOL -ii$INTERFACE -if$FW -dt2 -io0x1A0000 -is0x50000 -da02-00-00-00-00-$SWITCH_ADDR -dn$DN 
    if [ "$?" != 0 ]; then
        exit 1
    fi
fi
$TOOL -ii$INTERFACE -if$FW -dt1 -io0x120000 -is0x7d000 -da02-00-00-00-00-$SWITCH_ADDR -dn$DN 
if [ "$?" != 0 ]; then
    sleep 1
    $TOOL -ii$INTERFACE -if$FW -dt1 -io0x120000 -is0x7d000 -da02-00-00-00-00-$SWITCH_ADDR -dn$DN 
    if [ "$?" != 0 ]; then
        exit 1
    fi
fi
$TOOL -ii$INTERFACE -if$FW -dt5 -io0x102000 -is0x1E000 -da02-00-00-00-00-$SWITCH_ADDR -dn$DN 
if [ "$?" != 0 ]; then
    sleep 1
    $TOOL -ii$INTERFACE -if$FW -dt5 -io0x102000 -is0x1E000 -da02-00-00-00-00-$SWITCH_ADDR -dn$DN 
    if [ "$?" != 0 ]; then
        exit 1
    fi
fi
$TOOL -ii$INTERFACE -if$FW -dt4 -io0x100000 -is0x2000 -da02-00-00-00-00-$SWITCH_ADDR -dn$DN 
if [ "$?" != 0 ]; then
    sleep 1
    $TOOL -ii$INTERFACE -if$FW -dt4 -io0x100000 -is0x2000 -da02-00-00-00-00-$SWITCH_ADDR -dn$DN 
    if [ "$?" != 0 ]; then
        exit 1
    fi
fi

