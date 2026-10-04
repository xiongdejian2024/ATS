import os
import re

import yaml


class ParseTBConfig(object):
    def __init__(self, tbconfig):
        self.tbconfig = tbconfig
        self.yaml_content = self.get_yaml()

    def get_yaml(self):
        with open(self.tbconfig, 'rb') as f:
            yaml_content = list(yaml.safe_load_all(f))
        return yaml_content[0]

    def get_bus(self):
        return self.yaml_content.get("bus")


class AscConvert:
    def __init__(self, tb_cfg, asc_path, output_dir='./output'):
        self.tb_cfg = tb_cfg
        self.asc_path = asc_path
        self.output_dir = output_dir
        self.bus = self.get_bus()
        self.channel_bus_mapping = dict()
        self.asc_file_list = []
        self.header = ''
        self.file_obj = dict()

    def get_bus(self):
        return ParseTBConfig(self.tb_cfg).get_bus()

    def get_can_bus_name_by_channel(self):
        for bus_name, channel in self.bus.items():
            # 同星CAN
            if 'eth' in bus_name:
                continue
            if 'cem' in bus_name:
                continue
            if 'fr' in bus_name:
                continue
            if isinstance(channel, list):
                channel_id = channel[1] + 1
            # PCAN
            else:
                channel_id = int(channel[3:]) + 1
            self.channel_bus_mapping[channel_id] = bus_name

    def get_asc_file_by_channel(self):
        for bus_name in self.bus.keys():
            if 'eth' not in bus_name and 'fr' not in bus_name:
                self.asc_file_list.append(f'{bus_name}.asc')

    def open_file_obj(self):
        for bus_name in self.bus.keys():
            if 'eth' not in bus_name and 'fr' not in bus_name:
                self.file_obj[bus_name] = open(f'{self.output_dir}/{bus_name}.asc', 'w')

    def write_header(self):
        for bus_name in self.bus.keys():
            if 'eth' not in bus_name and 'fr' not in bus_name:
                self.file_obj[bus_name].write(self.header)

    def close_file_obj(self):
        if self.file_obj:
            for bus_name, obj in self.file_obj.items():
                obj.close()
                print(f'关闭{bus_name}.asc')

    def create_dir(self):
        if not os.path.exists(self.output_dir):
            os.mkdir(self.output_dir)

    def parse_asc(self):
        try:
            self.create_dir()
            print(f'创建目录成功，路径为: {self.output_dir}')
            self.get_asc_file_by_channel()
            print(f'获取写入的文件{self.asc_file_list}')
            self.get_can_bus_name_by_channel()
            print(f'根据通道成功获取总线')
            self.open_file_obj()
            print(f'打开所有文件')
            line_index = 1
            with open(self.asc_path) as f:
                for raw_line in f:
                    if line_index <= 2:
                        self.header += raw_line
                    else:
                        new_line = re.sub(r'\s+', ' ', raw_line, 10)
                        line_list = new_line.split(' ')[1:]
                        trace_type = self.get_trace_type(line_list)
                        if line_index == 3:
                            self.write_header()
                        else:
                            self.file_obj[trace_type].write(raw_line)
                    line_index += 1
        except Exception as e:
            __import__("logging").getLogger(__name__).exception("XAT 捕获异常：xat/tools/asc_tools/asc_convert.py")
            print(f'error: {str(e)}')
        finally:
            self.close_file_obj()

    def get_trace_type(self, line_list):
        # Lin
        if 'L' in line_list[1]:
            channel_id = int(line_list[1][1:])
            return f'cem_lin{channel_id}'
        # CANFD
        if 'CANFD' in line_list[1]:
            channel_id = int(line_list[2])
            return self.channel_bus_mapping[channel_id]
        else:
            channel_id = int(line_list[1])
            return self.channel_bus_mapping[channel_id]


if __name__ == '__main__':
    ac = AscConvert(tb_cfg='/root/xdj/sat/bench_config/soa_bench_025.yaml',
                    asc_path='/root/test_case_log/test_unlock_caseid_1567926.asc')
    ac.parse_asc()
