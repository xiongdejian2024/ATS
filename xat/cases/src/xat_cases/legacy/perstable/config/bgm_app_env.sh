#!/bin/sh

export JIDU_APP_LOG_PATH=/log/
export JETCRASH_DMP_DIR=/log/jetcrash/
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/app/lib

export ENV_APP_PATH=/app/
export ENV_SOA_CONFIG_PATH=/app/etc/soaconfig/
export ENV_CONFIG_PATH=/data/app/etc/

# uds stack
export UDSDOIP_CONFIG_PATH=/app/bin/udsconfig/
export UDSDOIP_DATA_PATH=/tmp/uds/
export UDSDOIP_LOG_PATH=/tmp/uds/

# bootes etc path
export BOOTES_HOME_DIR=/app/etc