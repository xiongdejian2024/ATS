#!/usr/bin/bash
# work dir: sat/
soa_name=$1
# Artifactory相关信息
ARTIFACTORY_URL="https://repo.jidudev.com/artifactory/SOASDK/SoaAutoTestPackages"
ARTIFACTORY_USERNAME="public_soa_bgm_tcam"
ARTIFACTORY_PASSWORD="${XAT_CREDENTIAL_SCAN_9E958E1968A3255D87CF}"
SOA_FILE='soazipconf.json'
OUTPUT_FILE="/root/soazipconf.json"
DOWNLOAD_PATH="$ARTIFACTORY_URL/$soa_name/$SOA_FILE"

# 从Artifactory下载文件
function download_file {
    echo "Downloading soazipconf.json from Artifactory..."
    echo "curl -u xxx:xxxx -o $OUTPUT_FILE $DOWNLOAD_PATH"
    curl -u "$ARTIFACTORY_USERNAME:$ARTIFACTORY_PASSWORD" \
         -o "$OUTPUT_FILE" \
         "$DOWNLOAD_PATH"
}

download_file
