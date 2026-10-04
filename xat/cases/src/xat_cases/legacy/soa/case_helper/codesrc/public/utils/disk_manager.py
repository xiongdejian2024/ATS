#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@IDE     ：PyCharm
@Author  ：'wxa'
@Date    ：2023/7/25 10:46
@Description  : 磁盘空间清理
"""

import os
import time
from datetime import datetime, timedelta

from .report import WechatTools
from .log import logger
from .utils import clear_dir


class DiskCleaner:
    def __init__(self, target_path, threshold_gb):
        self.target_path = target_path
        self.threshold_gb = threshold_gb

    def get_free_space_gb(self):
        """获取目标路径所在磁盘的剩余容量（以GB为单位）"""
        stat = os.statvfs(self.target_path)
        free_space_bytes = stat.f_frsize * stat.f_bavail
        free_space_gb = free_space_bytes / (1024 ** 3)
        return free_space_gb

    @staticmethod
    def delete_old_files_and_folders(folder_path, days_to_keep=3):
        """删除指定路径下，指定天数之前的文件和文件夹"""
        if not os.path.exists(folder_path) or not os.path.isdir(folder_path):
            return

        current_time = datetime.now()
        for root, dirs, files in os.walk(folder_path):
            for folder in dirs:
                folder_path = os.path.join(root, folder)
                folder_creation_time = datetime.fromtimestamp(os.path.getctime(folder_path))
                if current_time - folder_creation_time > timedelta(days=days_to_keep):
                    clear_dir(folder_path, keep=False)

    def clean_if_needed(self):
        """检查磁盘容量，如果小于指定值，则清理文件和文件夹"""
        days_to_keep = 3
        while days_to_keep > 0:
            free_space_gb = self.get_free_space_gb()
            if free_space_gb < self.threshold_gb:
                json_msg = {
                    "msgtype": "text",
                    "text": {
                        "content": f"Disk space is low: {free_space_gb:.2f} GB (Threshold: {self.threshold_gb} GB)",
                    }
                }
                WechatTools.log(json=json_msg)
                logger.info(f"Disk space is {free_space_gb:.2f} GB, Delete files from {days_to_keep} days ago")
                self.delete_old_files_and_folders(self.target_path, days_to_keep)
                days_to_keep -= 1
                time.sleep(10)
            else:
                logger.info(f"Disk space is sufficient: {free_space_gb:.2f} GB (Threshold: {self.threshold_gb} GB)")
                break
        else:
            logger.info("Need to delete other folder files")


# 使用示例：
if __name__ == "__main__":
    target_path = "/root/ltg03/pressure_log"  # 要清理的目标文件夹路径
    threshold_gb = 30  # 磁盘容量阈值（以GB为单位）

    disk_cleaner = DiskCleaner(target_path, threshold_gb)
    disk_cleaner.clean_if_needed()
