#!/bin/bash
echo "Received arguments: $@"
check_and_install_package() {
  local package_name=$1
  if dpkg-query -W -f='${Status}' "$package_name" 2>/dev/null | grep -qE '^install ok installed$'; then
      echo "$package_name is already installed."
  else
      # 假设使用apt-get作为包管理器
      echo "Installing $package_name..."
      sudo apt-get update
      sudo apt-get install -y "$package_name"
      if [ $? -eq 0 ]; then
          echo "$package_name installed successfully."
      else
          echo "Failed to install $package_name."
      fi
  fi
}

setup_linux_env() {
  check_and_install_package net-tools
  check_and_install_package unzip
  check_and_install_package curl
  check_and_install_package usbrelay
  check_and_install_package expect
  check_and_install_package can-utils
  check_and_install_package cmake
  check_and_install_package minicom
  check_and_install_package adb
  check_and_install_package sshpass
  check_and_install_package docker.io

  # install java
  check_and_install_package openjdk-17-jre-headless

  pip config --global set global.index-url https://repo.jidudev.com/artifactory/api/pypi/pypi/simple
  pip config --global set install.trusted-host repo.jidudev.com
  pip config --global set global.cache-dir ~/.cache/pip/
  check_and_install_package nginx
}

change_and_start_nginx() {
  cp -rf nginx.conf /etc/nginx/nginx.conf
  sync
}

install_allure_and_configure_allure_env() {
  /opt/allure-2.19.0/bin/allure --version
  if [ $? != 0 ]; then
    ./allure_install.sh
    echo "export PATH=/opt/allure-2.19.0/bin:\$PATH" >>/etc/profile
    source /etc/profile
  fi
}

setup_python_venv() {
  check_and_install_package python3-pip
  check_and_install_package python3-virtualenv
  virtualenv ../../venv -p python3
  source ../../venv/bin/activate
  pip install --upgrade pip -i https://repo.jidudev.com/artifactory/api/pypi/pypi/simple
  deactivate
}

deploy_ecu_simulator() {
  cd ../../ && ./update_lib.sh $@
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

check_command_status setup_linux_env
check_command_status change_and_start_nginx
check_command_status install_allure_and_configure_allure_env
check_command_status setup_python_venv
check_command_status deploy_ecu_simulator $@
