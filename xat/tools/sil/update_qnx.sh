#!/usr/bin/bash
current_dir=$(pwd)
package_url=$1
if [ -z "$package_url" ]; then
  echo "Error: The first argument (package_url) is missing."
  exit 1  # 退出脚本并返回非零状态码，表示错误
fi
# package_name为$1用/做分割，取最后一个字段
package_name=$(echo $package_url | awk -F '/' '{print $(NF)}')
# 镜像名称
image_name=$(echo $package_name | awk -F '.gz' '{print $1}')
# 最大重试次数
MAX_RETRIES=3

echo "当前工作路径: $current_dir"
echo "包链接: $package_url"
echo "包名: $package_name"
echo "镜像名称: $image_name"

function check_command_status() {
  $@
  exit_status=$?

  if [ $exit_status -eq 0 ]; then
    echo "$@执行成功"
  else
    echo "$@执行失败，脚本退出"
    exit 1
  fi
}

function start_ccu_cd() {
    cd /root/vjet && ./vjet.sh stop_qemu ccu_cd
    sleep 5
    cd /root/vjet && ./vjet.sh start_qemu ccu_cd
    sleep 10
    HOST="172.20.5.11"
    COUNT=60
    qemu_process=$(ps -ef | grep -v grep | grep qemu-system-aarch64 | wc -l)
    if [ "$qemu_process" -eq "0" ]; then
      echo "ccu_cd未成功启动"
      exit 1
    else
      ping_host "$HOST" "$COUNT"
      # 检查函数的返回值
      if [ $? -eq 0 ]; then
        echo "ccu_cd已成功启动"
      else
        echo "ccu_cd启动失败，$HOST ping不通"
        exit 1
      fi
    fi

}

function retry_start_qemu {
    local retries=0
    local status=1
    while [[ $retries -lt $MAX_RETRIES && $status -ne 0 ]]; do
        ((retries++))

        start_ccu_cd
        status=$?

        if [[ $status -ne 0 ]]; then
            echo "Download attempt $retries failed."
        fi
    done

    if [[ $status -eq 0 ]]; then
        echo "Download successful!"
    else
        echo "Download failed after $MAX_RETRIES attempts. Trying scp..."
        expect tools/setup_env/scp_soa_partner.exp $soa_name
    fi
}

function ping_host() {
  local HOST=$1
  local COUNT=$2
  local SUCCESS=false
  echo "开始 ping $HOST"
  for ((i = 0; i < $COUNT; i++)); do
    # 使用ping命令，每次只发送一个ICMP包，-W 1设置超时时间为1秒
    if ping -c 1 -W 1 $HOST >/dev/null 2>&1; then
      echo "$HOST is reachable."
      SUCCESS=true
      break # 成功ping通后退出循环
    else
      echo "$HOST is not reachable, trying again ($((i + 1))/$COUNT)..."
      sleep 1
    fi
  done

  if $SUCCESS; then
    return 0 # 成功返回0
  else
    echo "$HOST is not reachable after $COUNT attempts."
    return 1 # 失败返回1
  fi
}

mkdir -p update
cd update
# 获取md5
rm -f md5.txt
curl -u ${XAT_CREDENTIAL_SCAN_EE2AAE2A369A258F440F} -H "X-Checksum-MD5: 1" -o md5.txt -I $package_url
target_md5=$(cat md5.txt | grep 'x-checksum-md5: '|awk '{print $2}')
echo "target md5: $target_md5"
# 如果不存在61SDU241107.0111.02E_system_la.img.gz
if [ ! -e $image_name ]; then
  # 重试3次
  while [ $MAX_RETRIES -gt 0 ]; do
    check_command_status curl --retry $MAX_RETRIES -u ${XAT_CREDENTIAL_SCAN_EE2AAE2A369A258F440F} -o $package_name $package_url
    current_md5=$(md5sum $package_name | awk '{print $1}')
    echo "当前md5: $current_md5"
    # 校验md5是否一致
    if echo "$target_md5" | grep -q "$current_md5"; then
      echo "开始解压$package_name"
      check_command_status gunzip -f $package_name
      break
    else
      rm -f $package_name
      MAX_RETRIES=$((MAX_RETRIES-1))
      echo "$package_name md5校验失败，重新下载, 剩余下载次数$MAX_RETRIES"
    fi
  done
  if [ $MAX_RETRIES -eq 0 ]; then
    echo "下载$package_name失败"
    exit 1
  fi
else
  echo "$image_name已存在，跳过下载"
fi

echo "开始将$image_name复制到/root/vjet/images/ccu_cd/目录下"
check_command_status cp -f $image_name /root/vjet/images/ccu_cd/system_la.img


echo "开始启动ccu_cd"
retry_start_qemu

ssh-keygen -f "/root/.ssh/known_hosts" -R "172.20.5.11"

echo "开始拷贝ifs文件到QEMU虚拟机"
check_command_status expect ${current_dir}/tools/sil/scp_ifs.exp
