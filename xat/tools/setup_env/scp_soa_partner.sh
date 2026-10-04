#!/usr/bin/bash
# work dir: sat/
soa_name=$1
# Artifactory相关信息
ARTIFACTORY_URL="https://repo.jidudev.com/artifactory/SOASDK/SoaAutoTestPackages"
ARTIFACTORY_USERNAME="public_soa_bgm_tcam"
ARTIFACTORY_PASSWORD="${XAT_CREDENTIAL_SCAN_5E8C8975CA0E618E76D4}"
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
        expect tools/setup_env/scp_soa_partner.exp $soa_name
    fi
}

# 调用重试函数进行下载
retry_download_from_artifactory
