# -*- coding: utf-8 -*-
"""
@File        : signal_core_base.py.py
@Author      : quan.sun@jiduauto.com
@Time        : 2022/4/3 12:19
@Description : 
@Examples    :
"""


class SignalCoreBase:
    def __init__(self):
        # widths   ????  之前的
        pass

    def get_signal_dict_helper(
            self, sname, num_bits_in_signal, msb_bit_ndx_in_msg,
            signal_first_byte_lsb_bit_ndx_in_first_msg_byte=None):
        """
        :param sname:
        :type sname:
        :param num_bits_in_signal:
        :type num_bits_in_signal:
        :param msb_bit_ndx_in_msg:
        :type msb_bit_ndx_in_msg:
        :param signal_first_byte_lsb_bit_ndx_in_first_msg_byte:
        :type signal_first_byte_lsb_bit_ndx_in_first_msg_byte:
        :return:
        :rtype:
        """
        if signal_first_byte_lsb_bit_ndx_in_first_msg_byte == "Intel":
            signal_first_byte_lsb_bit_ndx_in_first_msg_byte = True
        elif signal_first_byte_lsb_bit_ndx_in_first_msg_byte == "Motorola":
            signal_first_byte_lsb_bit_ndx_in_first_msg_byte = False
        else:
            print("sig_byteorder is error")

        s_dict = {'length': num_bits_in_signal}

        byte_ndxs_in_msg, signal_msb_bit_ndx_in_msg, masks, unmasks, widths, shifts = \
            self.get_byte_ndxs_in_msg_and_msb_ndx_in_msg_and_masks_and_unmasks_and_widths_and_shifts(
                sname, num_bits_in_signal, msb_bit_ndx_in_msg, signal_first_byte_lsb_bit_ndx_in_first_msg_byte)

        num_bytes_in_signal = len(unmasks)

        s_dict['startbit'] = signal_msb_bit_ndx_in_msg

        if num_bytes_in_signal == 1:
            s_dict['byte'] = byte_ndxs_in_msg[0]

            s_dict['mask'] = masks[0]

            s_dict['unmask'] = unmasks[0]

            s_dict['shift'] = shifts[0]
        else:
            info_for_this_signal = []

            for i in range(0, num_bytes_in_signal):
                info_for_this_signal_byte = (byte_ndxs_in_msg[i], masks[i], unmasks[i], widths[i], shifts[i])

                info_for_this_signal.append(info_for_this_signal_byte)

            s_dict["bmuws_info"] = info_for_this_signal  # BMUWS == Byte, Mask, Unmask, Width, Shift.

        return s_dict

    # For CAN:                              1 1 1 1 1 1       2 2 2 2 1 1 1 1
    # Start bit# in mesg: 7 6 5 4 3 2 1 0   5 4 3 2 1 0 9 8   3 2 1 0 9 8 7 6
    #                    |_ _ _ _._ _ _ _| |_ _ _ _._ _ _ _| |_ _ _ _._ _ _ _| ...
    # Start bit# in byte: 7 6 5 4 3 2 1 0   7 6 5 4 3 2 1 0   7 6 5 4 3 2 1 0
    #                         Byte #0           Byte #1           Byte #2
    #
    def get_byte_ndxs_in_msg_and_msb_ndx_in_msg_and_masks_and_unmasks_and_widths_and_shifts(
            self, sname, num_bits_in_signal, msb_bit_ndx_in_msg,
            signal_first_byte_lsb_bit_ndx_in_first_msg_byte=None):
        # NOTE: for LIN msgs, msb_bit_ndx_in_msg = the bit_ndx of the lsb of the signal's first byte.

        # sun暂定  Motorola start bit is msb, Intel start bit is lsb
        start_byte_ndx_in_msg = int(msb_bit_ndx_in_msg / 8)  # msb_bit_ndx_in_msg  is  start_bit

        msb_ndx_in_first_byte = msb_bit_ndx_in_msg % 8

        if signal_first_byte_lsb_bit_ndx_in_first_msg_byte:
            # Intel
            # lsb_ndx_in_first_byte = signal_first_byte_lsb_bit_ndx_in_first_msg_byte % 8
            # number_of_less_significant_bits_in_first_byte_starting_from_the_msb_ndx = \
            #     msb_ndx_in_first_byte + 1 - lsb_ndx_in_first_byte

            lsb_ndx_in_first_byte = msb_ndx_in_first_byte        # byte里lsb离最右边的位数
            number_of_less_significant_bits_in_first_byte_starting_from_the_msb_ndx = \
                8 - lsb_ndx_in_first_byte   # byte里起始位离最左边的位数 + 1      ---- max number_of_bits_in_first_byte

        else:
            # Motorola
            lsb_ndx_in_first_byte = max(msb_ndx_in_first_byte - num_bits_in_signal + 1, 0)  # byte里lsb离最右边的位数

            number_of_less_significant_bits_in_first_byte_starting_from_the_msb_ndx = msb_ndx_in_first_byte + 1  # byte里起始位离最右边的位数 + 1    ---- max number_of_bits_in_first_byte

        num_signal_bits_in_first_byte = \
            min(num_bits_in_signal, number_of_less_significant_bits_in_first_byte_starting_from_the_msb_ndx)  # 在第一字节信号占的bit总数

        # 1.  Do the portion in the initial byte (may be a full byte).
        # Set the initial value of end_byte_ndx_in_msg here,
        # in case 2. or 3. below do not apply to this signal.
        #
        end_byte_ndx_in_msg = start_byte_ndx_in_msg

        byte_ndxs_in_msg = [start_byte_ndx_in_msg]

        num_remaining_bits_in_signal = num_bits_in_signal - num_signal_bits_in_first_byte

        num_bits_to_shift = lsb_ndx_in_first_byte

        shift = max(0, num_bits_to_shift)
        shifts = [shift]

        base_mask = (1 << num_signal_bits_in_first_byte) - 1

        mask = base_mask << shift
        masks = ["{:#010b}".format(mask)]

        unmask = mask ^ 0xff
        unmasks = ["{:#010b}".format(unmask)]

        widths = [num_signal_bits_in_first_byte]

        # 2.  Do the bytes-in-the-middle.
        num_full_bytes_in_the_middle = int(num_remaining_bits_in_signal / 8)

        for i in range(0, num_full_bytes_in_the_middle):
            byte_ndx = i + start_byte_ndx_in_msg + 1
            end_byte_ndx_in_msg = byte_ndx

            byte_ndxs_in_msg.append(end_byte_ndx_in_msg)

            widths.append(min(8, num_remaining_bits_in_signal))

            num_remaining_bits_in_signal -= 8

            shifts.append(0)

            masks.append("{:#010b}".format(0xff))
            unmasks.append("{:#010b}".format(0x00))

        # 3.  Do the remaining bits in the last byte, if any.
        if num_remaining_bits_in_signal > 0:
            end_byte_ndx_in_msg += 1

            byte_ndxs_in_msg.append(end_byte_ndx_in_msg)

            end_bit_ndx_in_msg = self.get_end_bit_ndx_in_msg(num_remaining_bits_in_signal, signal_first_byte_lsb_bit_ndx_in_first_msg_byte)

            widths.append(min(8, num_remaining_bits_in_signal))

            shifts.append(end_bit_ndx_in_msg)

            base_mask = (1 << num_remaining_bits_in_signal) - 1

            mask = base_mask << end_bit_ndx_in_msg
            masks.append("{:#010b}".format(mask))

            unmask = mask ^ 0xff
            unmasks.append("{:#010b}".format(unmask))

        return byte_ndxs_in_msg, msb_bit_ndx_in_msg, masks, unmasks, widths, shifts

    def get_end_bit_ndx_in_msg(self, num_remaining_bits_in_signal, signal_first_byte_lsb_bit_ndx_in_first_msg_byte=None):
        if signal_first_byte_lsb_bit_ndx_in_first_msg_byte:
            return 0
        else:
            return 8 - num_remaining_bits_in_signal

