# pip install vbf-parser
# 读取vbf后，可以得到vbf中的header信息，并得到一个字典类型的变量。

from vbf_parser import extract_header_body, lex_vbf_header, parse_vbf_tokens


def get_block_info(byte_data):
    block_infos = []
    remaining_data = byte_data
    while remaining_data:
        block_info = {}
        start_addr = remaining_data[:4]
        length_raw = remaining_data[4:8]
        length = int.from_bytes(length_raw, 'big')
        data = remaining_data[8:length + 8]
        checksum = remaining_data[length + 8:length + 10]
        block_info = {
            'start_addr': start_addr,
            'length': length_raw,
            'data': data,
            'checksum': checksum
        }
        remaining_data = remaining_data[length + 10:]
        block_infos.append(block_info)
    return block_infos

def get_vbf_payload(filepath):
    with open(filepath, "rb") as f:
        # hearder_body 
        header_body = extract_header_body(f)
        vbf = parse_vbf_tokens(lex_vbf_header(header_body))

        # payload
        remaining_data = f.read()  # 获取剩余的数据
        return remaining_data

def get_vbf_hearder_body(filepath):
    with open(filepath, "rb") as f:
        # hearder_body 
        header_body = extract_header_body(f)
        vbf = parse_vbf_tokens(lex_vbf_header(header_body))   # 变成字典
    return vbf

def get_vbf_sw_signature(filepath):
    vbf = get_vbf_hearder_body(filepath)
    sw_signature = vbf.get("sw_signature") or vbf.get("sw_signature_dev")
    # int 转 十六进制
    sw_signature = hex(sw_signature)
    # 十六进制转bytes
    sw_signature = sw_signature[2:]
    # 目前看sw_signature是512个字符，不足512，是之前转成数字时省略了前面的0，所以需要最前面补齐0，需要补齐到512个字符
    sw_signature = sw_signature.zfill(512)
    sw_signature = bytes.fromhex(sw_signature)
    # bytes 转 list
    sw_signature = list(sw_signature)
    return sw_signature

def get_vbf_erase_info(filepath):
    vbf = get_vbf_hearder_body(filepath)
    erase_info = vbf.get("erase")
    if erase_info:
        erase_info = erase_info[0]
        memory_address = erase_info[0]
        memory_size = erase_info[1]
        # 十六进制转bytes
        memory_address = bytes.fromhex(memory_address[2:])
        memory_size = bytes.fromhex(memory_size[2:])
        # bytes 转 list
        memory_address = list(memory_address)
        memory_size = list(memory_size)
        return [memory_address, memory_size]
    else:
        raise ValueError("No erase information found in the VBF file.")
    
def get_vbf_call(filepath):
    # 用于sbl 激活
    vbf = get_vbf_hearder_body(filepath)
    vbf_call = vbf.get("call")
    if vbf_call:
        vbf_call = hex(vbf_call)
        # 十六进制转bytes
        vbf_call = vbf_call[2:]
        vbf_call = vbf_call.zfill(8)
        vbf_call = bytes.fromhex(vbf_call)
        # bytes 转 list
        vbf_call = list(vbf_call)
        return vbf_call
    else:
        raise ValueError("No call information found in the VBF file.")

if __name__ == '__main__':
    # remaining_data = get_vbf_payload("/root/quansun_new3/aicomate/PTZ_sbl.VBF")
    # block_infos = get_block_info(remaining_data)
    # for i in range(len(block_infos)):
    #     print('第{}块数据'.format(i+1))
    #     print(block_infos[i])

    # remaining_data = get_vbf_payload("/root/quansun_new3/aicomate/PTZ_Upd.VBF")
    # block_infos = get_block_info(remaining_data)
    # for i in range(len(block_infos)):
    #     print('第{}块数据'.format(i+1))
    #     print(block_infos[i])

    # sw_signature = get_vbf_sw_signature("/root/quansun_new3/aicomate/PTZ_sbl.VBF")
    # print(sw_signature)

    # vbf_erase_info = get_vbf_erase_info("/root/quansun_new3/aicomate/PTZ_Upd.VBF")
    # print(vbf_erase_info)

    vbf_call = get_vbf_call("/root/quansun_new3/aicomate/PTZ_sbl.VBF")
    print(vbf_call)