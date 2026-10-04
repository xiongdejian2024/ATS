# -*- coding: utf-8 -*-
"""
@File        : codecs.py
@Author      : yu.zhang0101 & jiankai.zhang
@Time        : 2022/04/13 4:01 PM
@Description : DidCodec

"""




class F190Codec(udsoncan.DidCodec):
    def encode(self, data):  # 17 bytes
        byteslist = data.to_bytes(17, 'big')
        return byteslist

    def decode(self, payload):
        _value = payload.hex()
        print("Payload: %s" % _value)

    def __len__(self):
        return 17


class F186Codec(udsoncan.DidCodec):
    def encode(self, data):
        # return super().encode(*did_value)
        if data == 'Default session':
            return 0x01
        elif data == 'Programming session':
            return 0x02
        elif data == 'Extended session':
            return 0x03
        elif data == 'Safety system diagnostic session':
            return 0x04
        else:
            return 0xFF

    def decode(self, payload):
        # return super().decode(did_payload)
        if payload == 0x01:
            return 'Default session'
        elif payload == 0x02:
            return 'Programming session'
        elif payload == 0x03:
            return 'Extended session'
        elif payload == 0x04:
            return 'Safety system diagnostic session'
        else:
            return 'Unknown session'

    def __len__(self):
        return 1


class F1AACodec(udsoncan.DidCodec):
    def encode(self, data):  # BCD + ASC
        # return super().encode(*did_value)
        byteslist = []
        for i in range(0, 10):
            data1 = data[2 * i]
            data2 = data[2 * i + 1]
            hex1 = str.upper(data1) - 0x30
            hex1 = hex1 - 7 if hex1 > 9 else None
            hex2 = str.upper(data2) - 0x30
            hex2 = hex2 - 7 if hex2 > 9 else None
            hexvalue = hex1 * 16 + hex2
            bcdvalue = (hexvalue // 10) * 16 + (hexvalue % 10)
            byteslist.append(bcdvalue)
        for asc in data[10:]:
            byteslist.append(ord(asc))
        return byteslist

    def decode(self, payload):
        # return super().decode(did_payload)
        datalist = ''
        bcdlist = payload[0:5]
        asclist = payload[5:]
        for byte in bcdlist:
            hexvalue = (byte // 16) * 10 + (byte & 0x0F)
            hexstr = hex(hexvalue)[2:]  # 0xAB -> 'AB'
            print(hexstr)
            datalist = datalist + hexstr
        for asc in asclist:
            datalist = datalist + chr(asc)
        return datalist

    def __len__(self):
        return 8


class F1ABCodec(udsoncan.DidCodec):
    def encode(self, data):  # BCD + ASC
        # return super().encode(*did_value)
        byteslist = []
        for i in range(0, 10):
            data1 = data[2 * i]
            data2 = data[2 * i + 1]
            hex1 = str.upper(data1) - 0x30
            hex1 = hex1 - 7 if hex1 > 9 else None
            hex2 = str.upper(data2) - 0x30
            hex2 = hex2 - 7 if hex2 > 9 else None
            hexvalue = hex1 * 16 + hex2
            bcdvalue = (hexvalue // 10) * 16 + (hexvalue % 10)
            byteslist.append(bcdvalue)
        for asc in data[10:]:
            byteslist.append(ord(asc))
        return byteslist

    def decode(self, payload):
        # return super().decode(did_payload)
        datalist = ''
        bcdlist = payload[0:5]
        asclist = payload[5:]
        for byte in bcdlist:
            hexvalue = (byte // 16) * 10 + (byte & 0x0F)
            hexstr = hex(hexvalue)[2:]  # 0xAB -> 'AB'
            datalist = datalist + hexstr
        for asc in asclist:
            datalist = datalist + chr(asc)
        return datalist

    def __len__(self):
        return 8


class F1AECodec(udsoncan.DidCodec):
    def encode(self, data):  # 8 bytes
        byteslist = bytes.fromhex(data)
        return byteslist

    def decode(self, payload):
        _value = payload.hex()
        print("Payload: %s" % _value)

    def __len__(self):
        return 9


class F1A5Codec(udsoncan.DidCodec):  # need to be verified
    def encode(self, data):  # BCD + ASC
        # return super().encode(*did_value)
        byteslist = []
        for i in range(0, 10):
            data1 = data[2 * i]
            data2 = data[2 * i + 1]
            hex1 = str.upper(data1) - 0x30
            hex1 = hex1 - 7 if hex1 > 9 else None
            hex2 = str.upper(data2) - 0x30
            hex2 = hex2 - 7 if hex2 > 9 else None
            hexvalue = hex1 * 16 + hex2
            bcdvalue = (hexvalue // 10) * 16 + (hexvalue % 10)
            byteslist.append(bcdvalue)
        for asc in data[10:]:
            byteslist.append(ord(asc))
        return byteslist

    def decode(self, payload):
        # return super().decode(did_payload)
        datalist = ''
        bcdlist = payload[0:5]
        asclist = payload[5:]
        for byte in bcdlist:
            hexvalue = (byte // 16) * 10 + (byte & 0x0F)
            hexstr = hex(hexvalue)[2:]  # 0xAB -> 'AB'
            datalist = datalist + hexstr
        for asc in asclist:
            datalist = datalist + chr(asc)
        return datalist

    def __len__(self):
        return 8


class ECMCodec(udsoncan.DidCodec):
    """
    Did: 0x40DE
    """

    def encode(self, data):  # 32 bytes
        byteslist = data.to_bytes(32, 'big')
        return byteslist

    def decode(self, payload):
        _value = payload.hex()
        print("Payload: %s" % _value)

    def __len__(self):
        return 32


class IEMCodec(udsoncan.DidCodec):
    """
    Did: 0x40DF
    """

    def encode(self, data):  # 32 bytes
        byteslist = data.to_bytes(32, 'big')
        return byteslist

    def decode(self, payload):
        _value = payload.hex()
        print("Payload: %s" % _value)

    def __len__(self):
        return 32


class MGMCodec(udsoncan.DidCodec):
    """
    Did: 0x40E0
    """

    def encode(self, data):  # 32 bytes
        byteslist = data.to_bytes(32, 'big')
        return byteslist

    def decode(self, payload):
        _value = payload.hex()
        print("Payload: %s" % _value)

    def __len__(self):
        return 32


class F106Codec(udsoncan.DidCodec):
    def encode(self, data):  # 1558 bytes
        byteslist = bytes.fromhex(data)
        return byteslist

    def decode(self, payload):
        _value = payload.hex()
        print("Payload: %s" % _value)

    def __len__(self):
        return 1558


class D902Codec(udsoncan.DidCodec):
    def encode(self, data):
        byteslist = data.to_bytes(2, 'big')
        return byteslist

    def decode(self, payload):
        _value = payload.hex()
        print("Payload: %s" % _value)

    def __len__(self):
        return 2


class D260Codec(udsoncan.DidCodec):
    def encode(self, data):
        byteslist = data.to_bytes(4, 'big')
        return byteslist

    def decode(self, payload):
        _value = payload.hex()
        print("Payload: %s" % _value)

    def __len__(self):
        return 4


class F18CCodec(udsoncan.DidCodec):
    def encode(self, data):  # 8 bytes
        byteslist = data.to_bytes(8, 'big')
        return byteslist

    def decode(self, payload):
        _value = payload.hex()
        print("Payload: %s" % _value)

    def __len__(self):
        return 8


class F1A0Codec(udsoncan.DidCodec):
    def encode(self, data):  # 64 bytes
        byteslist = data.to_bytes(64, 'big')
        return byteslist

    def decode(self, payload):
        _value = payload.hex()
        print("Payload: %s" % _value)

    def __len__(self):
        return 64


class F1F0Codec(udsoncan.DidCodec):
    def encode(self, data):  # 64 bytes
        byteslist = data.to_bytes(64, 'big')
        return byteslist

    def decode(self, payload):
        _value = payload.hex()
        print("Payload: %s" % _value)

    def __len__(self):
        return 64


class F124Codec(udsoncan.DidCodec):
    def encode(self, data):  # 7 bytes
        byteslist = data.to_bytes(7, 'big')
        return byteslist

    def decode(self, payload):
        _value = payload.hex()
        print("Payload: %s" % _value)

    def __len__(self):
        return 7


class D01CCodec(udsoncan.DidCodec):
    def encode(self, data):
        byteslist = data.to_bytes(292, 'big')
        return byteslist

    def decode(self, payload):
        _value = payload.hex()
        print("Payload: %s" % _value)

    def __len__(self):
        return 292


class F102Codec(udsoncan.DidCodec):
    def encode(self, data):
        byteslist = data.to_bytes(5, 'big')
        return byteslist

    def decode(self, payload):
        _value = payload.hex()
        print("Payload: %s" % _value)

    def __len__(self):
        return 5


class ED20Codec(udsoncan.DidCodec):
    def encode(self, data):
        byteslist = data.to_bytes(26, 'big')
        return byteslist

    def decode(self, payload):
        _value = payload.hex()
        print("Payload: %s" % _value)

    def __len__(self):
        return 26
