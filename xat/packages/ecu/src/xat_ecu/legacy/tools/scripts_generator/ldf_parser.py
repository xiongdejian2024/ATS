# update 2022-1-5
"""
Created on May 21, 2017

@author: altran

@description: LDF_parser parses LDF files.

@reference: https://microchipdeveloper.com/lin:protocol-app-ldf
@reference: https://stackoverflow.com/questions/44005022/lin-descriptor-file-parser
"""
import os
import re
import sys
import copy
from argparse import ArgumentParser

# From: https://pypi.org/project/ucanlintools/
# This downloadable library seems to be incomplete at present:
#   from ucanlintools.LDF_parser import parseLDF
# so we're using our existing script instead:


class LinMessage(object):
    """
    Class to define LIN Messages.
    """
    def __init__(self, message_id, message_name, length_bytes, originator, cycle_time, schedule):
        """
        LIN Message Initializer.

        :param message_id: <int> The lin message id
        :param message_name: <string> The name of the lin message
        :param length_bytes: <int> The length of the lin message, in bytes
        :param originator: <string> The lin bus that originates the lin message
        :param cycle_time: <float> The cycle time of the lin message
        :param schedule:
        :type schedule:
        """
        self.msg_id = message_id
        self.msg_name = message_name
        self.msg_length = length_bytes
        self.originator = originator
        self.msg_cyc = cycle_time
        self.schedule = schedule

        # List of signals within the message
        self.signals = []


class LinSignal(object):
    """
    Class to define Lin Signals.
    """

    def __init__(
        self, parent_message_id, signal_name, start_bit, length_bits, initial_value, originator, receivers, comments):
        """
        CAN Signal Initializer

        :param parent_message_id: <int> the lin id of the lin message containing the signal
        :type parent_message_id:
        :param signal_name: <string> the name of the signal
        :type signal_name:
        :param start_bit: <int> the bit that the signal starts at
        :type start_bit:
        :param length_bits: <int> length of the signal in bits
        :type length_bits:
        :param initial_value:
        :type initial_value:
        :param originator:
        :type originator:
        :param receivers:
        :type receivers:
        :param comments:
        :type comments:
        """
        self.parent_message_id = parent_message_id
        self.signal_name = signal_name
        self.start_bit = start_bit
        self.length_bits = length_bits
        self.initial_value = initial_value
        self.originator = originator
        self.receivers = receivers
        self.comments = comments

        self.choices = None


class LdfParser(object):
    """
    Class to parse LDFs.
    """
    
    def __init__(self, config):
        """
        Constructor
        
        :param config: <dict> dictionary containing the configuration information
        """
        self.lin_message_list = []
        self.lin_messages_info = {}
        self.lin_signals_info = {}
        success = self.__get_config_info(config)
        if success:
            pass
        else:
            sys.exit(1)

        # Store the "NormalTable" entries so it's available for use by everyone in the call tree.
        self.msg_cycle_times = {"NormalTable": []}

    """ Initializers """
    def __get_config_info(self, config):
        """
        Get Config Info parses necessary information from the config dictionary
        
        :param config: <dict> Dictionary containing the configuration information
        :return success: <boolean> True on successful parse, False otherwise
        """
        success = False
        try:
            self.ldf_file_path = config["LDF File"]
            success = True
        except:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/packages/ecu/src/xat_ecu/legacy/tools/scripts_generator/ldf_parser.py")
            print ("Failed to parse the necessary configuration information.")

        return success

    """ Main Functions """
    def get_messages(self):
        """
        Get Messages returns a list of all messages parsed out of the LDF.

        :return lin_message_list: <list of LinMessage> A list of LinMessage objects generated when parsing the LDF
        """
        return copy.deepcopy(self.lin_message_list)

    def parse_ldf(self, caller_bus_name=None):
        """
        Parse LDF does the main work of parsing the LDF file.
        """
        with open(self.ldf_file_path, "r+") as ldf:
            filename = os.path.basename(self.ldf_file_path)
            bus_name = filename.split("_")[1].upper() if caller_bus_name is None else caller_bus_name

            encoding_lookup = None
            encoding_dict = None

            for line in ldf:
                line = line.strip()
                re_line = re.sub(r'\s', "", line)

                # Parse Signals {}
                if re_line.upper() == 'SIGNALS{':
                    for line in ldf:
                        if line.strip() == '}':
                            break

                        if line.strip() == "":
                            continue

                        line_split = re.sub(r'[:,;]', " ", line).strip().split()
                        signal_name = line_split[0].strip()     # In Compass we preserve the mixed-case: no.upper()

                        if signal_name.startswith('Sig_'):
                            signal_name = re.sub(r'^Sig_', "", signal_name).strip()
                        if signal_name == 'VEHCRASHIND':
                            signal_name += '_{}'.format(bus_name)

                        length_bits = int(line_split[1].strip())
                        initial_value = int(line_split[2].strip())

                        originator_and_receivers_and_comments = line_split[3:]
                        try:
                            comments_start_ndx = originator_and_receivers_and_comments.index("//")
                            comments = originator_and_receivers_and_comments[comments_start_ndx:]

                            originator_and_receivers = \
                                [x.strip().upper()
                                 for x in originator_and_receivers_and_comments[:comments_start_ndx]]

                        except ValueError as err:
                            originator_and_receivers = \
                                [x.strip().upper() for x in originator_and_receivers_and_comments]

                            # If no "//" found, there are no comments in this line.
                            comments = []

                        self.lin_signals_info[signal_name] = {
                            "length_bits": length_bits,
                            "initial_value": initial_value,
                            "originator": originator_and_receivers[0],
                            "receivers": originator_and_receivers[1:],
                            "comments": comments,
                            "choices": {}
                        }
                # Parse Frames {}
                elif re_line.upper() == 'FRAMES{':
                    for line in ldf:
                        if line.strip() == '}':
                            break

                        if line.strip() == "":
                            continue

                        if '{' in line:
                            line_split = re.sub(r'[:,{]', " ", line).strip().split()
                            current_message_name = line_split[0].strip().upper()
                            if current_message_name.startswith('FRM_'):
                                current_message_name = re.sub(r'^FRM_', "", current_message_name).strip()
                            current_id = int(line_split[1].strip())
                            originator = line_split[2].strip().upper()
                            length_bytes = int(line_split[3].strip())
                            self.lin_messages_info[current_message_name] = {}
                            self.lin_messages_info[current_message_name]['id'] = current_id
                            self.lin_messages_info[current_message_name]['originator'] = originator
                            self.lin_messages_info[current_message_name]['length_bytes'] = length_bytes
                            self.lin_messages_info[current_message_name]['cycle_time'] = 0

                            for line in ldf:
                                if line.strip() == '}':
                                    break

                                if line.strip() == "":
                                    continue

                                line_split = re.sub(r'[,;]', " ", line).strip().split()
                                signal_name = line_split[0].strip()  # In Compass we preserve the mixed-case: no.upper()

                                if signal_name.startswith('Sig_'):
                                    signal_name = re.sub(r'^Sig_', "", signal_name).strip()

                                if signal_name == 'VEHCRASHIND':
                                    signal_name += '_{}'.format(bus_name)

                                start_bit = int(line_split[1])
                                self.lin_signals_info[signal_name]['start_bit'] = start_bit
                                self.lin_signals_info[signal_name]['parent_id'] = current_id
                # Parse Schedule_tables {}
                elif re_line.upper() == 'SCHEDULE_TABLES{':
                    message_count = None
                    total_cycle_time = 0

                    for line in ldf:
                        if line.strip() == '}':
                            break

                        if line.strip() == "":
                            continue

                        re_line = re.sub(r'\s', "", line.strip())

                        # if re_line.upper() == 'NORMALTABLE_NT2{' or \
                        # re_line.upper() == 'ST_MAIN{' or \
                        # re_line.upper() == 'NormalTable_Gemini_EU {' or \
                        # re_line.upper() == 'NormalTable_Gemini_CN {':
                        # if ('NORMALTABLE_NT2' in re_line.upper()) or ('NORMALTABLE_FORCE' in re_line.upper()) or (re_line.upper() == 'ST_MAIN{'):
                        if 'NORMALTABLE' in re_line.upper() or re_line.upper() == 'ST_MAIN{':
                            message_count = {}
                            total_cycle_time = 0

                            for line in ldf:
                                if line.strip() == '}':
                                    break

                                if line.strip() == "":
                                    continue

                                line_split = re.sub(r"[;]", " ", line).strip().split()

                                message_name = line_split[0].upper()

                                if message_name.startswith('FRM_'):
                                    message_name = re.sub(r'^FRM_', "", message_name).strip()

                                message_cycle_time = int(line_split[2])

                                # Store the "NormalTable" entries to pass back to the caller.
                                if message_name in self.msg_cycle_times:
                                    self.msg_cycle_times[message_name].append(message_cycle_time)
                                else:
                                    self.msg_cycle_times[message_name] = [message_cycle_time]

                                # Store the overall order of NormalTable entries too.
                                self.msg_cycle_times["NormalTable"].append((message_name, message_cycle_time))

                                if message_name not in message_count:
                                    message_count[message_name] = 1
                                else:
                                    message_count[message_name] += 1

                                total_cycle_time += message_cycle_time

                        elif re_line.upper() == 'DIAGREQONLY{' or re_line.upper() == 'DIAGRESPONLY{' or \
                             re_line.upper() == 'ST_MASTERREQ{' or re_line.upper() == 'ST_SLAVERESP{':

                            for line in ldf:
                                if line.strip() == '}':
                                    break

                                if line.strip() == "":
                                    continue

                                line_split = re.sub(r'[;]', " ", line).strip().split()
                                message_name = line_split[0].upper()

                                if message_name.startswith('FRM_'):
                                    message_name = re.sub(r'^FRM_', "", message_name).strip()

                                if message_name in self.lin_messages_info:
                                    self.lin_messages_info[message_name]['schedule'] = re_line[:-1]

                    if message_count is None:
                        raise RuntimeError("No NormalTable found in .ldf file!")

                    for message_name, count in message_count.items():
                        self.lin_messages_info[message_name]["cycle_time"] = (total_cycle_time / count) / 1000
                        # Output "Normal" as "Cyclic", to match CAN msg jargon,
                        # to combine CAN & LIN routing test auto-generation into one script.
                        self.lin_messages_info[message_name]["schedule"] = "Cyclic"

                # Parse Signal_encoding_types {}
                elif re_line.upper() == 'SIGNAL_ENCODING_TYPES{':
                    encoding_lookup = {}
                    for line in ldf:
                        if line.strip() == '}':
                            break

                        if line.strip() == "":
                            continue

                        if '{' in line:
                            # In Compass we preserve the mixed-case: no.upper()
                            encoding_name = re.sub(r'{', "", line).strip()
                            encoding_lookup[encoding_name] = {}

                            for line in ldf:
                                if line.strip() == '}':
                                    break

                                if line.strip() == "":
                                    continue

                                if line.strip().upper().startswith('LOGICAL_VALUE'):
                                    line_split = line.strip().split(',')
                                    enum_key = int(line_split[1].strip())
                                    # In Compass we preserve the mixed-case: no.upper()
                                    enum_value = re.sub(r'[;"]', "", line_split[2]).strip()
                                    encoding_lookup[encoding_name][enum_key] = enum_value

                # Parse Signal_representation {}
                elif re_line.upper() == 'SIGNAL_REPRESENTATION{':
                    encoding_dict = {}
                    for line in ldf:
                        if line.strip() == '}':
                            break

                        if line.strip() == "":
                            continue

                        line_split = re.sub(r'[ ]*[,;:][ ]*', " ", line).strip().split()
                        lookup_name = line_split[0]  # In Compass we preserve the mixed-case: no.upper()
                        encoding_dict[lookup_name] = []

                        for i in range(len(line_split) - 1):
                            signal_name = line_split[i + 1]  # In Compass we preserve the mixed-case: no.upper()

                            if signal_name.startswith('Sig_'):
                                signal_name = re.sub(r'^Sig_', "", signal_name).strip()

                            if signal_name == 'VEHCRASHIND':
                                signal_name += '_{}'.format(bus_name)

                            encoding_dict[lookup_name].append(signal_name)

            # Cross reference Signal Representation with Signal Encoding Types
            if encoding_dict is not None:
                for lookup_name, signals in encoding_dict.items():
                    for signal_name in signals:
                        for enum_key, enum_value in encoding_lookup[lookup_name].items():
                            self.lin_signals_info[signal_name]['choices'][enum_key] = enum_value

            # Create lin_message_list
            for message_name, value in self.lin_messages_info.items():
                schedule = value["schedule"] if "schedule" in value else "None"

                # Create a new message
                message_name = LinMessage(
                    value['id'], message_name, value['length_bytes'],
                    value['originator'], value['cycle_time'], schedule)

                # Add message to the list of messages
                self.lin_message_list.append(message_name)

            # Add Signals to messages in lin_message_list
            for signal_name, value in self.lin_signals_info.items():
                # Create a new signal
                signal = LinSignal(
                    value["parent_id"], signal_name, value["start_bit"], value["length_bits"],
                    value["initial_value"], value["originator"], value["receivers"], value["comments"])

                signal.choices = copy.deepcopy(value["choices"])

                # Add signal to message
                for message_name in self.lin_message_list:
                    if message_name.msg_id == value["parent_id"]:
                        message_name.signals.append(signal)


def main(ldf_file):
    config_info = {"LDF File": ldf_file}

    D = LdfParser(config_info)
    D.parse_ldf()

    messages_list = D.get_messages()
    print(messages_list)


def parse_args():
    argparser = ArgumentParser(description="Parse LDF File")

    argparser.add_argument('-l', '--ldf', help='Full path to LDF file to parse.', required=True)

    return argparser


if __name__ == "__main__":
    args = parse_args().parse_args()
    main(args.ldf)
