#!/usr/bin/bash
if [ $# -ne 2 ]; then
  echo "Usage: ./deploy.sh arg1 arg2;arg1 is bootes_version(eg:bootes1_4_1r306) arg2 is JIDL_version(eg:JIDL_RELEASE_1_4REL_8)"
  exit 1
fi
X86=$1
idl=$2
soa_name=SOA_$1$1$2
# Artifactory相关信息
ARTIFACTORY_URL="https://repo.jidudev.com/artifactory/SOASDK/SoaAutoTestPackages"
ARTIFACTORY_USERNAME="public_soa_bgm_tcam"
ARTIFACTORY_PASSWORD="${XAT_CREDENTIAL_SCAN_008A1941C785EBB7606F}"
SOA_FILE='soa.zip'
OUTPUT_FILE="/root/soa.zip"
soa_name_txt=`pwd`"/soa_name.txt"
DOWNLOAD_PATH="$ARTIFACTORY_URL/$soa_name/$SOA_FILE"
MAX_RETRIES=3


# 从Artifactory下载文件
function download_file {
    echo "Downloading file from Artifactory..."
    echo "curl -u xxx:xxxx -o $OUTPUT_FILE $DOWNLOAD_PATH"
    echo "文件下载中, 请勿Ctrl+C退出"
    curl -u "$ARTIFACTORY_USERNAME:$ARTIFACTORY_PASSWORD" \
         -o "$OUTPUT_FILE" \
         "$DOWNLOAD_PATH"
    cp -f $OUTPUT_FILE ./soa_partner/
    # 重写soa_name.txt里面的版本号
    echo $soa_name >> $soa_name_txt
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
        echo "Download failed after $MAX_RETRIES attempts"
    fi
}

function clear_old_soapartner {
    echo "清理旧版本"
    rm -rf ./soa_partner/BootesRelease
}

function check_soapartner_version {
    # 判断文件是否存在
    if [ ! -f "$soa_name_txt" ]; then
        echo "版本文件不存在，需要升级"
        return 0
    fi
    # 从文件中读取内容
    file_content=$(<"$soa_name_txt")

    # 比较文件内容与输入的字符串
    if [ "$file_content" = "$soa_name" ]; then
        echo "版本一致无需升级"
        return 1
    else
        echo "版本文件不一致，需要升级"
        return 0
    fi
}

function unzip_soapartner {
    echo "解压soa.zip"
    unzip -o ./soa_partner/${SOA_FILE} -d ./soa_partner/ >/root/unzip_soa.log
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

check_soapartner_version
result=$?
if [ $result -eq 0 ]; then
    # 调用重试函数进行下载
    check_command_status clear_old_soapartner
    check_command_status retry_download_from_artifactory
    check_command_status unzip_soapartner
fi
