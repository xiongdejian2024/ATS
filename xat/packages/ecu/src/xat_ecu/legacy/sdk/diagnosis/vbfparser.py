# -*- coding: utf-8 -*-
"""
@File        : vbfparser.py
@Author      : quan.sun@jiduatuo.com
@Time        : 2022-06-01 18:57
@Description : 
"""

import sys
import os
from vbf_parser import *
import re
import io
from typing import BinaryIO, Pattern, Union
from xat_ecu.legacy.common.logger import *

VBF_ENCODING = "ascii"


class VbfParser:
    def __init__(self, filepath):
        self.filepath = filepath

    def _read_until(self, fp: BinaryIO, pattern: Union[Pattern, str]) -> bool:
        """
        >>> file = io.BytesIO("abc; header {spanish inquisition".encode(VBF_ENCODING))
        >>> _read_until(file, r'header\\s*{')
        True
        >>> file.read().decode(VBF_ENCODING)
        'spanish inquisition'
        >>> file = io.BytesIO("no pattern".encode(VBF_ENCODING))
        >>> _read_until(file,r"\\{")
        False
        """
        text = ""
        while not re.search(pattern, text):
            c = fp.read(1).decode(VBF_ENCODING)
            if not c:
                return False
            text += c
        return True

    def header_bodycan_and_asciisize(self, fp: BinaryIO) -> str:
        if self._read_until(fp, r"header\s*{"):
            nested_level = 1
            header = []
            is_in_quotes = False
            while nested_level != 0:
                char = fp.read(1).decode(VBF_ENCODING)
                if char == "":
                    raise ValueError("Reached file end before header was closed")
                header.append(char)
                # if char == '"':
                #     is_in_quotes = not is_in_quotes
                if not is_in_quotes:
                    if char == "{":
                        nested_level += 1
                    elif char == "}":
                        nested_level -= 1
            return "".join(header[:-1]), fp.tell()
        else:
            logger.error("header is not found ")

    def get_vbf_header_and_asciisize(self):
        with open(self.filepath, "rb") as f:
            vbf_header, asciisize = self.header_bodycan_and_asciisize(f)
            print(vbf_header)
            print(len(vbf_header))
            print(asciisize)
        return vbf_header, asciisize

    def get_start_end_signature(self, vbf_header):
        vbf_header_list = vbf_parser.lex_vbf_header(vbf_header)
        print(vbf_header_list)
        i = 0
        for data in vbf_header_list:
            if data == "erase":
                start = vbf_header_list[i + 4]
                end = vbf_header_list[i + 6]
            elif data == "sw_signature_dev":
                signature = vbf_header_list[i + 2]
            i += 1
        start_len = (len(start) - 2) // 2
        start = bytes.fromhex(start.strip("0x"))
        start = list(start)
        if start == []:
            start = [0]*start_len
        end = bytes.fromhex(end.strip("0x"))
        end = list(end)
        signature = bytes.fromhex(signature.strip("0x"))
        signature = list(signature)
        return start, end, signature

if __name__ == '__main__':
    vbf = VbfParser('/home/sun/6160110050AH.vbf')
    vbf_header, asciisize = vbf.get_vbf_header_and_asciisize()
    start, end, signature = vbf.get_start_end_signature(vbf_header)
    print(start)
    print(end)
    print(signature)



