

def reverse_bits8(input_data):
    """
    按比特位翻转数据
    :param input_data: 输入数据
    :return: 翻转数据结果
    """
    if input_data == 0 or input_data == 255:
        return input_data

    result = 0
    for i in range(8):
        if (input_data & 0x01) == 1:
            result |= (1 << (8-i-1))
        input_data = input_data >> 1

    return result


def calc_crc(data_crc, poly, start_value, xor_value, input_ref=False, output_ref=False):
    """
    Calculate CRC data using mod 2 algorithm
    :param data_crc: 需要检验的数据
    :param poly: 多项式
    :param start_value: 初始值
    :param xor_value: 结果异或值
    :param input_ref: Input data reflection flag
    :param output_ref: Output data reflection flag
    :return: CRC result
    """
    crc_result = start_value

    for elem in data_crc:
        data_byte = reverse_bits8(elem) if input_ref else elem
        crc_result = (crc_result ^ data_byte) & 0xFF
        for idx in range(8):
            if crc_result & 0x80 != 0:
                crc_result = (crc_result << 1) ^ poly & 0xFF
            else:
                crc_result = (crc_result << 1) & 0xFF

    crc_result = reverse_bits8(crc_result) if output_ref else crc_result

    return (crc_result ^ xor_value) & 0xFF


if __name__ == '__main__':
    data = [0x98, 0x1F, 0x00, 0x01]
    print(calc_crc(data, 0x1D, 0x00, 0x00))
