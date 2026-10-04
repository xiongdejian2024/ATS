import os, sys

current_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_path)
sys.path.append(os.path.join(current_path, ".."))

import json
from vbf_parser.vbf_jsonifier import *
import re

VBF_HEADER_END = "\n}"
max_number_of_block_length = 511998  # 51200-2 bytes


class VBFParser:

    def __init__(self, file):
        self.file = file

    def read_header(self):

        if not os.path.isfile(self.file):
            print("Error File")
            return False
        header = ""
        before = ""
        with open(self.file, 'r', encoding="ascii", errors="ignore") as f:
            while f.readable():
                s = f.read(1)
                if s == VBF_HEADER_END[1] and before == VBF_HEADER_END[0]:
                    header += s
                    break
                header += s
                before = s
        comments = re.search("//.*\n", header).group()
        ddd = jsonify_vbf_header(header.replace(comments, ''))
        json_header = json.loads(ddd)
        return json_header

    async def read_block(self):
        header = ""
        before = ""
        with open(self.file, "rb") as f:
            while f.readable():
                s = f.read(1).decode(errors="ignore", encoding="utf-8")
                if s == VBF_HEADER_END[1] and before == VBF_HEADER_END[0]:
                    header += s
                    break
                header += s
                before = s
            while True:
                block = f.read(max_number_of_block_length)  # 每次读取固定长度到内存缓冲区
                if block:
                    yield block
                else:
                    return  # 如果读取到文件末尾，则退出

    async def read_all_block(self):
        with open(self.file, "rb") as f:
            while True:
                block = f.read(max_number_of_block_length)  # 每次读取固定长度到内存缓冲区
                if block:
                    yield block
                else:
                    return  # 如果读取到文件末尾，则退出


if __name__ == '__main__':
    v = VBFParser(r'../../VBF_signed/6160110050ZAF.vbf')
    head = v.read_header()
    print(head)
