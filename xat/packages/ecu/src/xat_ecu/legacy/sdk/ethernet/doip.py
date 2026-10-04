#!/usr/bin/python3
import sys, getopt
import time
from uds_pyclient.logger import setup_logger as setup_logger
from xat_ecu.legacy.sdk.ethernet.doip_payload import doip_payload
from xat_ecu.legacy.sdk.driver.ethernet_lib.tcp_socket import tcp_socket_client
from .uds_cmd import UdsCmdResponse
response_received = False  # Used to perform unit test for DoIP


# ****************************************************************************************
def get_doip_id_from_can_id(can_id):
    if can_id == 0x601:
        return 0xE400   #DoIP functional Addressing ID
    return can_id - 0x600

# ****************************************************************************************
class doip(object):
    # ****************************************
    def __init__(self, server_ip= None, server_port= None, my_ip= None, my_port= None):
        self.log = setup_logger(level="warning", name="(DOIP)")
        self.server_ip = server_ip
        self.server_port = server_port
        self.my_ip = my_ip
        self.my_port = my_port
        self.connection = None
        self.payload = None
        self.current_payload_data=[]
        self._exitFlag = False
        self.client_doip_id = 0x0E80
        self.cb = None

    # ****************************************
    def shutdown(self):
        # print("DoIP: Closing connection")
        if self.connection is not None:
            self.connection.close()
            self.connection = None
    
    def doip_close(self):
        # print("DoIP: Closing connection")
        if self.connection is not None:
            self.connection.close()
            self.connection = None
            # print("DoIP: Connection closed")
    # ****************************************
    def new_connection(self):
        """
        @function new_connection(self)
        @brief This function is used to create a new connection to send data
        @return tcp_socket_client reference to a TCP socket
        """
        s = tcp_socket_client(1, "DoIP TCP Socket")
        try:
            s.connect(self.server_ip, self.server_port)
        except OSError as e:
            self.log.error(str(e) + ' : %s:%d' % (self.server_ip, self.server_port))
            return None
        s.setup_response_callback(self.rx_diags_msgs)
        self.log.debug("TCP client connected")
        s.start()
        return s

    # ****************************************
    def get_doip_header(self, payload_type, size):
        """
        @function get_doip_header(self, payload_type, size)
        @brief This function is used to generate a doip header to send a message
        @param payload_type Type of the payload to use
        @param size of the payload
        @return List header - Header generated for the doip packet
        """
        header = []
        header.append(0x02) #DoIP Version
        header.append(0xFD) #DoIP Inverse Version
        if payload_type == doip_payload.DIAG_MSG_TYPE:
            header.append(0x80) #DoIP Diagnostics request payload type
            header.append(0x01)
        else:
            self.log.error("Invalid payload type")
            raise TypeError("Invalid doip payload_type %s" % payload_type)
        #Set size bytes
        size += 4 # +4 bytes for receiver and transmitter IDs
        header.append((size >> 24) & 0xFF)
        header.append((size >> 16) & 0xFF)
        header.append((size >> 8) & 0xFF)
        header.append(size & 0xFF)
        # Set DoIP ID of receiver
        header.append((self.client_doip_id >> 8) & 0xFF)
        header.append(self.client_doip_id & 0xFF)
        # Set DoIP ID of Transmitter
        header.append((self.server_doip_id >> 8) & 0xFF)
        header.append(self.server_doip_id & 0xFF)
        #print('DoIP Header: [{}]'.format(', '.join(hex(x) for x in header)))
        return header
    
    # ****************************************    
    def send_data(self,can_id, data):
        """
        @function send_data(self,can_id, data)
        @brief This function us used to send a diagnostics request.
        @param can_id CAN id of the ECU to send the data to
        @param data, contains a list with Diags request, first byte must be the SID
        @return False if problems sending request
        @return True if send was ok
        """
        self.request_can_id = can_id
        self.server_doip_id = get_doip_id_from_can_id(can_id)
        if not self.server_doip_id:
            raise LookupError("Unknown DOIP ID from CAN_ID %r" % (can_id))
        payload_data = self.get_doip_header(doip_payload.DIAG_MSG_TYPE, len(data))
        payload_data += data #Add data of the diags request
        if self.connection is None:
            self.connection = self.new_connection()
            if self.connection is None:
                self.log.error("Error connecting to host")
                return False
        self.msg_ack_received = False
        self.msg_ack_type = None
        self.payload_type_expected = doip_payload.DIAG_MSG_POS_ACK_TYPE
        #print ('Tx Payload: [{}]'.format(', '.join(hex(x) for x in payload_data[0:16])))
        result = self.connection.send(payload_data)
        if result < 0:
            return False
        timeout = 0
        while self.msg_ack_received == False:
            time.sleep(.10)
            timeout += 1
            if timeout == 10: #1.0 seconds
                self.log.error("Ack timeout for request [%X:%X]" % (data[0], data[1]))
                return False
        if self.msg_ack_received == True and self.msg_ack_type == doip_payload.DIAG_MSG_POS_ACK_TYPE:
            self.payload_type_expected = doip_payload.DIAG_MSG_TYPE
            return True
        elif self.msg_ack_received == True and self.msg_ack_type == doip_payload.DIAG_MSG_NEG_ACK_TYPE:
            self.log.error("Negative ACK received for request [%X:%X]" % (data[0], data[1]))
            return False
        else:
            self.log.error("No Ack received for request  [%X:%X]" % (data[0], data[1]))
            return False


    # ****************************************
    def setup_data_callback(self, callBack, response_id):
        """
        @function setup_data_callback(self, callBack, response_id)
        @brief This function must be called before sending a diagnostics request to setup the 
               callback for the diagnostics response
        @param callBack Function callback for the message received
        @param response_id Can id of the intended recepient
        """
        #print("Setup DoIP data callback to ")
        #print(callBack)
        self.cb = callBack
        self.response_can_id = response_id
        
    # ****************************************
    def rx_diags_msgs(self, data):
        """
        @function rx_diags_msgs(self, data)
        @brief This function used to receive doip payloads, it is called from the TCP SOCKET
               after new data arrives in the socket. It calls the callback provided
               after a new uds request is complete. After reading from the socket we need to 
               loop in this function looking for doip payloads in the data read from the socket.
        """
        self.current_payload_data += data
        payload = doip_payload()
        while payload.is_complete(self.current_payload_data):
            self.payload = doip_payload()
            payload_data, self.current_payload_data = payload.get_payload_from_data(self.current_payload_data)
            self.payload.add_data(payload_data)
            if self.payload.is_valid() and self.payload.type() == doip_payload.DIAG_MSG_POS_ACK_TYPE:
                #print("Ack received: [{}]".format(', '.join(hex(x) for x in data)))
                self.msg_ack_type = doip_payload.DIAG_MSG_POS_ACK_TYPE
                self.msg_ack_received = True
            elif self.payload.is_valid() and self.payload.type() == doip_payload.DIAG_MSG_NEG_ACK_TYPE:
                #print("Negative Ack received: [{}]".format(', '.join(hex(x) for x in data)))
                self.msg_ack_type = doip_payload.DIAG_MSG_NEG_ACK_TYPE
                self.msg_ack_received = True
            elif self.payload.is_valid() and self.payload.type() == doip_payload.DIAG_MSG_TYPE:
                #print("UDS Response received: [{}]".format(', '.join(hex(x) for x in data)))
                self.uds_response = UdsCmdResponse(self.payload.data()[4], self.payload.data()[5:])
                #check if response recieved is from expected ECU
                if self.response_can_id != (self.request_can_id + 0x80):
                    self.log.error("Error received Response ID :0x%X do not match with expected requested ID :0x%0X" % (self.response_can_id,self.request_can_id))
                elif self.cb: 
                    self.cb(self.uds_response)
            else:
                print("Unexpected DoIP payload: [{}]".format(', '.join(hex(x) for x in data)))
        self.current_payload_data=[]
        return

    # ****************************************
    def waiting_vehicle_announcement(self, req):
        """
        @todo Finish implement this function
        """
        self.log.info("Rx payload type:%s" % (req.get_payload_type()))
        self.log.info("Rx payload size:%s" % (req.get_payload_size()))
        self.log.info("Payload:%s" % (req.get_payload()))
        self.log.info.response_received = True
        return

    def waiting_vehicle_id(self, req):
        """
        @todo Finish implement this function
        """
        self.log.info("Rx payload type:%s" % (req.get_payload_type()))
        self.log.info("Rx payload size:%s" % (req.get_payload_size()))
        self.log.info("Payload:%s" % (req.get_payload()))
        self.response_received = True
        return

    # ****************************************
    def doVehicleDiscovery(self,UDP_IP="localhost", UDP_PORT=13400):
        """
        This function implements vehicle discovery.
        1. Waits for "Vehicle Announcement Message" received from DoIP Gateway in UDP port 13400
        2. Tester will send a "Vehicle Identification Request" in UDP port 13400
        3. Tester wait to receive a "Vehicle Identification Response" in UDP port 13400
        This test pass if:
            Annoucement message is received in time
            Vehicle Identification Response is received in time
        """
        global response_received
        #Setup
        #udp_socket_client
        #self.init_socket("UDP")
        #self.setup_rx(UDP_IP, UDP_PORT)
        self.setup_data_callback(self.waiting_vehicle_announcement,doip_payload.VEHICLE_ANN_TYPE)
        self.start()
        self.log.info("Waiting vehicle announcement")
        self.response_received = False
        self.timeout=0
        while True:
            try:
                if self.response_received:
                    self.log.info("Vehicle announcement received")
                    break
                time.sleep(.1)
            except KeyboardInterrupt:
                self.log.info("Exiting now...")
                self.shutdown()
                time.sleep(1)
                return
            time.sleep(.1)
            self.timeout += 1
            if self.timeout == 600: #1min
                self.log.info("Timeout to receive Vehicle announcement...")
                self.shutdown()
                time.sleep(1)
                return
        #transmit Vehicle ID request
        self.log.info("Sending Vehicle ID Request")
        payload=[0x02,0xFD,0x00,0x01,0x00,0x00,0x00,0x00]
        self.connect(UDP_IP, UDP_PORT)
        self.send(payload, UDP_IP, UDP_PORT)
        #Wait for Vehicle ID response
        self.setup_data_callback(self.waiting_vehicle_id, doip_payload.VEHICLE_ID_RESP_TYPE)
        self.response_received = False
        while True:
            try:
                if self.response_received:
                    self.log.info("Vehicle ID Response received")
                    self.log.info("Test PASS")
                    self.shutdown()
                    time.sleep(1)
                    return
                time.sleep(.1)
            except KeyboardInterrupt:
                self.log.info("Exiting now...")
                self.shutdown()
                time.sleep(1)
                return

# ****************************************************************************************
#                                UNIT TESTING FOR DoIP
# ****************************************************************************************
def test_cb(req):
    global response_received
    print("Rx payload type:%s" % (req.get_payload_type()))
    print("Rx payload size:%s" % (req.get_payload_size()))
    print("Payload:%s" % (req.get_payload()))
    response_received = True
    return

# ****************************************************************************************
def test_send_callBack(req):
    print("Diagnostics msg received")
    print("Response:0x%X" % (req.get_response_code()))
    print('Data: [{}]'.format(', '.join(hex(x) for x in req.get_data())))
    return

def testSend(IP, PORT, SERVER_IP, SERVER_PORT, payload, count):
    global response_received
    #Setup
    doipTester = doip(IP, PORT,"172.16.141.130", 13400)
    doipTester.setup_data_callback(test_send_callBack, 0x685)
    #Run unit test
    while count > 0:
        print('Tx Data: [{}]'.format(', '.join(hex(x) for x in payload)))
        doipTester.send_data(0x605,payload)
        try:
            time.sleep(.1)
        except KeyboardInterrupt:
            doipTester.shutdown()
            time.sleep(1)
            return
        count -= 1

# ****************************************************************************************
def testReceive(IP="localhost", PORT=13400, SERVER="localhost"):
    global response_received
    #Setup
    doipTester = doip(IP, PORT, SERVER, PORT)
    #doipTester.init_socket(socketType)
    #doipTester.setup_rx(UDP_IP, UDP_PORT)
    doipTester.setup_data_callback(test_cb)
    doipTester.start()
    print("Reception enabled")
    while(True):
        response_received = False
        while True:
            try:
                if response_received:
                    print("-------------------------------------")
                    break
                time.sleep(.1)
            except KeyboardInterrupt:
                print("Exiting now...")
                doipTester.shutdown()
                time.sleep(1)
                return

# ****************************************************************************************
def waiting_payload_type(req):
    global response_received
    print("Rx:%s" % (req.get_payload_type()))
    print("Rx payload size:%s" % (req.get_payload_size()))
    print("Payload:%s" % (req.get_payload()))
    response_received = True
    return

# ****************************************************************************************
def testVehicleDiscovery(UDP_IP="localhost", UDP_PORT=13400):
    doipTester = doip(21, "DoIP Rx Thread")
    doipTester.doVehicleDiscovery(UDP_IP, UDP_PORT)
    return

# ****************************************************************************************
def read_file(filename):
    # Open a file
    fo = open(filename, "r+")
    sim_str = fo.read()
    data = list(sim_str)
    new_data = []
    byte_counter = 0
    new_byte = 0x00
    for letter in data:
        byte_counter = byte_counter + 1
        if byte_counter == 1:
            new_byte = letter
        else:
            new_byte = new_byte + letter
            # print("%s",new_byte)
            new_data.append(new_byte)
            byte_counter = 0
    val = [int(x, base=16) for x in new_data]
    val = bytes(val)
    val = list(val)
    # print(val[0:100])

    # Close opend file
    fo.close()
    return val

# ****************************************************************************************
def printHelp():
    print('test.py -t <test name> -i <IP address> -p <port> -d <data> -c <repeat>')

# ****************************************************************************************
def main(argv):
    global exitFlag
    test = "tx"
    ipAddress = "localhost"
    serverIP = "localhost"
    port = 13400
    payload = [0x10,0x01]
    count = 1
    try:
        opts, args = getopt.getopt(argv,"ht:i:p:d:c:s:",["test=","ipAddress=","port=","data=","count=", "serverAddress="])
    except getopt.GetoptError:
        printHelp()
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            printHelp()
            return
        elif opt in ("-t", "--test"):
            test = arg
        elif opt in ("-i", "--ipAddress"):
            ipAddress = arg
        elif opt in ("-p", "--port"):
            port = int(arg)
        elif opt in ("-s", "--serverAddress"):
            serverIP = arg
        elif opt in ("-c", "--count"):
            count = int(arg)
        elif opt in ("-d", "--data"):
            data = arg
            data=data.split(',')
            payload=[]
            for value in data:
                payload.append(int(value,16))


    print("Running %s test" % (test))
    if test == "discover":
        testVehicleDiscovery(ipAddress, port)
    elif test == "file":
        read_file(filename)
    elif test == "tx":
        testSend(ipAddress, port, serverIP, port, payload, count )
    elif test == "rx":
        testReceive(ipAddress, port)
    else:
        print("Invalid test specified: %s" % (test))
    print("Test End")
    return

# ****************************************************************************************
if __name__ == '__main__':
    if len(sys.argv) < 2:
        printHelp()
        sys.exit(0)
    main(sys.argv[1:])


