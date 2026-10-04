

class CCUMCUAD:
    ip_address = "172.20.5.22"
    mac_address = "02:00:00:00:20:22"
    vlan_id = 5

    class SocketAdMcuSoAdUDP:
        port_number = 30501
        transport_protocol = "UDP"

    class SocketMulticast:
        port_number = 30501
        transport_protocol = "UDP"

    class SocketAdMcuTCPServer:
        port_number = 30503
        transport_protocol = "TCP"


class CCUMCUCD:
    ip_address = "172.20.5.12"
    mac_address = "02:00:00:00:20:12"
    vlan_id = 5

    class SocketMulticast:
        port_number = 30501
        transport_protocol = "UDP"

    class SocketCdMcuSoAdUDP:
        port_number = 30501
        transport_protocol = "UDP"

    class SocketCdMcuTCPServer:
        port_number = 30503
        transport_protocol = "TCP"


class CCUNAD:
    ip_address = "172.20.5.31"
    mac_address = "02:00:00:00:20:31"
    vlan_id = 5

    class SocketMulticast:
        port_number = 30501
        transport_protocol = "UDP"

    class SocketCdNadSoAdUDP:
        port_number = 30501
        transport_protocol = "UDP"

    class SocketCdNadTCPClient1:
        port_number = 30513
        transport_protocol = "TCP"


class CCUSOCCD:
    ip_address = "172.20.5.11"
    mac_address = "02:00:00:00:20:13"
    vlan_id = 5

    class SocketMulticast:
        port_number = 30501
        transport_protocol = "UDP"

    class SocketCdSocSoAdUDP:
        port_number = 30501
        transport_protocol = "UDP"

    class SocketCdSocTCPClient2:
        port_number = 30523
        transport_protocol = "TCP"

    class SocketCdSocTCPClient1:
        port_number = 30513
        transport_protocol = "TCP"

    class SocketCdSocLogCdMcuSoAdUDP:
        port_number = 30506
        transport_protocol = "UDP"

    class SocketCdSocPMTCPClient:
        port_number = 30504
        transport_protocol = "TCP"

    class SocketCdSocTCPClient3:
        port_number = 30533
        transport_protocol = "TCP"

    class SocketCdSocTCPClient4:
        port_number = 30543
        transport_protocol = "TCP"

    class SocketCdSocLogLcuLSoAdUDP:
        port_number = 30507
        transport_protocol = "UDP"

    class SocketCdSocLogLcuRSoAdUDP:
        port_number = 30508
        transport_protocol = "UDP"


class LCUL:
    ip_address = "172.20.5.1"
    mac_address = "02:00:00:00:20:01"
    vlan_id = 5

    class SocketMulticast:
        port_number = 30501
        transport_protocol = "UDP"

    class SocketLcuLSoAdUDP:
        port_number = 30501
        transport_protocol = "UDP"

    class SocketLcuLTCPServer:
        port_number = 30503
        transport_protocol = "TCP"


class LCUR:
    ip_address = "172.20.5.2"
    mac_address = "02:00:00:00:20:02"
    vlan_id = 5

    class SocketMulticast:
        port_number = 30501
        transport_protocol = "UDP"

    class SocketLcuRSoAdUDP:
        port_number = 30501
        transport_protocol = "UDP"

    class SocketLcuRTCPServer:
        port_number = 30503
        transport_protocol = "TCP"


class CCUSOCAD:
    ip_address = "172.20.5.21"
    mac_address = "02:00:00:00:20:21"
    vlan_id = 5

    class SocketAdSocSoAdUDP:
        port_number = 30501
        transport_protocol = "UDP"

    class SocketAdSocTCPClient2:
        port_number = 30523
        transport_protocol = "TCP"
