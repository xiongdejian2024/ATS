#!/usr/bin/bash
# work dir: sat/
soa_name=$1
# Artifactory相关信息
ARTIFACTORY_URL="https://repo.jidudev.com/artifactory/SOASDK/SoaAutoTestPackages"
ARTIFACTORY_USERNAME="public_soa_bgm_tcam"
ARTIFACTORY_PASSWORD="${XAT_CREDENTIAL_SCAN_98EBA5D218FCACADF29E}"
SOA_FILE='soa.zip'
OUTPUT_FILE="/root/soa.zip"
DOWNLOAD_PATH="$ARTIFACTORY_URL/$soa_name/$SOA_FILE"
MAX_RETRIES=3

# 从Artifactory下载文件
function download_file {
    echo "Downloading file from Artifactory..."
    echo "curl -u xxx:xxxx -o $OUTPUT_FILE $DOWNLOAD_PATH"
    curl -u "$ARTIFACTORY_USERNAME:$ARTIFACTORY_PASSWORD" \
         -o "$OUTPUT_FILE" \
         "$DOWNLOAD_PATH"
    cp -f $OUTPUT_FILE ./
}

# 下载文件并进行重试
function retry_download_from_artifactory {
    local retries=0
    local status=1
    while [[ $retries -lt $MAX_RETRIES && $status -ne 0 ]]; do
        ((retries++))

        download_file
        status=$?

        if [[ $status -ne 0 ]]; then
            echo "Download attempt $retries failed."
        fi
    done

    if [[ $status -eq 0 ]]; then
        echo "Download successful!"
    else
        echo "Download failed after $MAX_RETRIES attempts. Trying scp..."
        return 1
    fi
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

# 调用重试函数进行下载
check_command_status retry_download_from_artifactory
