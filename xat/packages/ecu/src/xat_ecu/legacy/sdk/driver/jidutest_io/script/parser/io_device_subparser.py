import sys
import warnings
import argparse
from nidaqmx.system import System, Device
from nidaqmx.errors import DaqError, DaqWarning
from jidutest_io.script.parser.main_parser import MainParser
from jidutest_io.constant import NiDeviceType
from jidutest_io.utils.color_cli import (rgb_green,
                                        rgb_red,
                                        rgb_blue)
from jidutest_io.utils.io_device import (get_device_type,
                                        get_str,
                                        is_valid_io_device,
                                        is_valid_ipv4_address)


warnings.filterwarnings("error")


@MainParser.RegisterSubparser("io-show-dev", [
    {"arg_name": "names", "type": str, "help": "IO device name", "nargs": "*", "default": ""}],
    "show device by name")
def io_show_dev(args: argparse.Namespace) -> None:
    param_name_list = args.names
    
    system = System()

    if not param_name_list:
        for device in system.devices:
            sys.stdout.write(rgb_green('Name') + ': ' + rgb_blue(f'{device.name:<24}') + 
                             rgb_green('Category') + ': ' + rgb_blue(f'{device.product_category:<40}') +
                             rgb_green('Type') + ': ' + rgb_blue(f'{device.product_type:<20}') +
                             rgb_green('Number') + ': ' + rgb_blue(f'{device.product_num:<10}') +
                             rgb_green('Serial Number') + ': ' + rgb_blue(f'{device.dev_serial_num:<10}\n')
                             )
        return
    
    for param_name in param_name_list:
        if not is_valid_io_device(param_name):
            sys.stderr.write(rgb_red(f'Device name {param_name} is invalid \n\n'))
            continue
        device = system.devices[param_name]
        
        sys.stdout.write(rgb_green('Name') + ': ' + rgb_blue(device.name) + "\n" +
                         rgb_green('Category') + ': ' + rgb_blue(device.product_category) + "\n" +
                         rgb_green('Type') + ': ' + rgb_blue(device.product_type) + "\n" +
                         rgb_green('Serial Number') + ': ' + rgb_blue(device.dev_serial_num) + "\n"
                         )
        
        device_type = get_device_type(device)
        
        if device_type is NiDeviceType.cDAQ:
            sys.stdout.write(rgb_green('Hostname') + ': ' + rgb_blue(device.tcpip_hostname) + "\n" +
                             rgb_green('IP') + ': ' + rgb_blue(device.tcpip_ethernet_ip) + "\n" +
                             rgb_green('Bustype') + ': ' + rgb_blue(device.bus_type) + "\n\n"
                             )

        if "cModule" in device_type.name:
            sys.stdout.write(rgb_green('cDAQ chassis') + ': ' + rgb_blue(device.compact_daq_chassis_device) + "\n" +
                             rgb_green('cDAQ slot') + ': ' + rgb_blue(device.compact_daq_slot_num) + "\n"
                             )
            
        if device_type is NiDeviceType.cModule_AI:
            sys.stdout.write(rgb_green('AI Channels') + "\n" + rgb_blue(get_str(device.ai_physical_chans.channel_names) + "\n\n"))
        if device_type is NiDeviceType.cModule_AO:
            sys.stdout.write(rgb_green('AO Channels') + "\n" + rgb_blue(get_str(device.ao_physical_chans.channel_names) + "\n\n"))
        if device_type is NiDeviceType.cModule_CI:
            sys.stdout.write(rgb_green('CI Channels') + "\n" + rgb_blue(get_str(device.ci_physical_chans.channel_names) + "\n\n"))
        if device_type is NiDeviceType.cModule_CO:
            sys.stdout.write(rgb_green('CO Channels') + "\n" + rgb_blue(get_str(device.co_physical_chans.channel_names) + "\n\n"))
        if device_type is NiDeviceType.cModule_DI:
            sys.stdout.write(rgb_green('DI Ports') + rgb_blue(get_str(device.di_ports.channel_names) + "\n"))
            sys.stdout.write(rgb_green('DI Lines') + "\n" + rgb_blue(get_str(device.di_lines.channel_names) + "\n\n"))
        if device_type is NiDeviceType.cModule_DO:
            sys.stdout.write(rgb_green('DO Ports') + rgb_blue(get_str(device.do_ports.channel_names) + "\n"))
            sys.stdout.write(rgb_green('DO Lines') + "\n" + rgb_blue(get_str(device.do_lines.channel_names) + "\n\n"))


@MainParser.RegisterSubparser("io-add-dev", [
    {"arg_name": "ipaddress", "type": str, "help": "ip address"}],
    "add network device")
def io_add_dev(args: argparse.Namespace) -> None:
    if not is_valid_ipv4_address(args.ipaddress):
        sys.exit(rgb_red(f'IPv4 address {args.ipaddress} is invalid \n'))
    try:
        dev = Device("").add_network_device(args.ipaddress, attempt_reservation=True)
        sys.stdout.write(str(dev)+"\n")
    except DaqWarning:
        sys.exit(rgb_red(f'Device with {args.ipaddress} exists \n'))
    except DaqError:
        sys.exit(rgb_red(f'Device with {args.ipaddress} is unreachabled or not NI device \n'))


@MainParser.RegisterSubparser("io-del-dev", [
    {"arg_name": "name", "type": str, "help": "Del IO device name"}],
    "delete network device")
def io_del_dev(args: argparse.Namespace) -> None:
    if not is_valid_io_device(args.name):
        sys.exit(rgb_red(f'Device name {args.name} is invalid \n'))
    try:
        Device(f"{args.name}").delete_network_device()
        sys.stdout.write(f"device {args.name} is deleted\n")
    except DaqError:
        sys.exit(f"Device {args.name} not support to be deleted\n")
        
        
@MainParser.RegisterSubparser("io-resv-dev",[
    {"arg_name": "name", "type": str, "help": "reserve the IO device "}],
    "reserve network device")
def io_resv_dev(args: argparse.Namespace) -> None:
    if not is_valid_io_device(args.name):
        sys.exit(rgb_red(f'Device name {args.name} is invalid \n'))
    try:
        Device(f"{args.name}").reserve_network_device(override_reservation=True)
        sys.stdout.write(f"device {args.name} is reserved\n")
    except DaqError:
        sys.exit("reserve is Error\n")


@MainParser.RegisterSubparser("io-unresv-dev",[
    {"arg_name": "name", "type": str, "help": "unreserve the IO device "}],
    "unreserve network device")
def io_unresv_dev(args: argparse.Namespace) -> None:
    if not is_valid_io_device(args.name):
        sys.exit(rgb_red(f'Device name {args.name} is invalid \n'))
    try:
        Device(f"{args.name}").unreserve_network_device()
        sys.stdout.write(f"device {args.name} is unreserved\n")
    except DaqError:
        sys.exit("network device is not reserved for this host \n")


@MainParser.RegisterSubparser("io-reset",[
    {"arg_name": "name", "type": str, "help": "reset the IO device "}],
    "reset network device")
def io_reset_dev(args: argparse.Namespace) -> None:
    if not is_valid_io_device(args.name):
        sys.exit(rgb_red(f'Device name {args.name} is invalid \n'))
    try:
        Device(f"{args.name}").reset_device()
        sys.stdout.write(f"device {args.name} is reset\n")
    except DaqError:
        sys.exit(":network device is not reset for this host \n")
        

@MainParser.RegisterSubparser("io-self-test",[
    {"arg_name": "name", "type": str, "help": "self test the IO device"}],
    "device self test")
def io_self_test(args: argparse.Namespace) -> None:
    if not is_valid_io_device(args.name):
        sys.exit(rgb_red(f'Device name {args.name} is invalid \n'))
    try:
        Device(f'{args.name}').self_test_device()
        sys.stdout.write(f"device {args.name} self test finish \n")
    except DaqError:
        sys.exit(":network device is not reset for this host \n")
