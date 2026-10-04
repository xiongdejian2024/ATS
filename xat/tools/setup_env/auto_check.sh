#!/bin/bash

deploy_sat_autorun() {
    cd /root/autorun
    git clone https://jidudev.com/soa/soa_test/sat.git
    cd sat
    python3 tools/setup_env/setupenv.py
}

check_command_status() {
  $@
  exit_status=$?

  if [ $exit_status -eq 0 ]; then
    echo "$@执行成功"
  else
    echo "$@执行失败，脚本退出"
    exit 1
  fi
}

check_command_status deploy_sat_autorun
