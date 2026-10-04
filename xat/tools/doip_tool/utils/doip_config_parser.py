import json
import os


class DoIPConfigParser:
    def __init__(self, json_file=None) -> None:
        if json_file is None:
            json_file = os.path.join(os.path.dirname(__file__), '../config/DoIPConfig.json')
        self.jsonfile = json_file
        self.doipconfig = None
        self.ecu_ip = None
        self.ecu_logical_address = None
        self.tester_ip = None
        self.tester_logical_address = None
        self.logical_functional_address = None
        self.doip_tcp_port = None
        self.Routing_activation_type = None
        self.Wait_before_reconnect_attempt = None
        self.Interval_between_attempts = None
        self.Maximum_number_of_attempts = None
        self.Timing_P6_client = None
        self.Timing_P6_client_extended = None
        self.Timing_P2_server = None
        self.Timing_P2_server_extended = None
        self.suppress_positive_response = None

        with open(self.jsonfile, 'r') as load_f:
            self.doipconfig = json.load(load_f)
            # self.ecu_ip = self.doipconfig['ecu_ip']
            # print(self.ecu_ip)
            # self.ecu_logical_address = int(self.doipconfig['ecu_logical_address'], 16)
            # self.tester_ip = self.doipconfig['tester_ip']
            # self.tester_logical_address = int(self.doipconfig['tester_logical_address'], 16)
            # self.logical_functional_address = int(self.doipconfig['logical_functional_address'], 16)
            # self.doip_tcp_port = self.doipconfig['doip_tcp_port']
            # self.Routing_activation_type = self.doipconfig['Routing_activation_type']
            # self.Wait_before_reconnect_attempt = self.doipconfig['Wait_before_reconnect_attempt']
            # self.Interval_between_attempts = self.doipconfig['Interval_between_attempts']
            # self.Maximum_number_of_attempts = self.doipconfig['Maximum_number_of_attempts']
            # self.Timing_P6_client = self.doipconfig['Timing_P6_client']
            # self.Timing_P6_client_extended = self.doipconfig['Timing_P6_client_extended']
            # self.Timing_P2_server = self.doipconfig['Timing_P2_server']
            # self.Timing_P2_server_extended = self.doipconfig['Timing_P2_server_extended']
            # self.suppress_positive_response = int(self.doipconfig['suppress_positive_response'])


if __name__ == '__main__':
    d = DoIPConfigParser()
    print(d.ecu_ip)
