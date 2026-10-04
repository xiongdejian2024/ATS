#!/bin/bash

SWITCH_BASE_PATH=$(cd "$(dirname "${BASH_SOURCE[0]}")"; pwd)

TOOL=$SWITCH_BASE_PATH/DownloadImage

INTERFACE=$1

$TOOL -ii$INTERFACE -gc
