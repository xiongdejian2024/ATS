import sys
import argparse
from nidaqmx.task import Task
from nidaqmx.errors import DaqReadError, DaqWriteError
from jidutest_io.script.parser.main_parser import MainParser
from jidutest_io.utils.io_device import NiDeviceType
from jidutest_io.utils.io_device import get_channel_type


@MainParser.RegisterSubparser("io-set",[
    {"arg_name": "channel",    "type": str, "help": "io bus channel"},
    {"arg_name": "value",      "type": int, "help": "io value", "choices": [0,1]},
    {"arg_name": "--timeout",  "type": int, "help": "", "default": 10}],
    "set io status")
def io_set(args: argparse.Namespace) -> None:
    channel = args.channel
    channel_type = get_channel_type(channel)
    if not channel_type:
        sys.exit(f"Channel {channel} is not invalid \n")

    with Task() as io_task:
        if channel_type is NiDeviceType.cModule_DO:
            io_task.do_channels.add_do_chan(channel)
            try:
                io_task.write(bool(args.value), timeout=args.timeout)
                sys.stdout.write(f"Switch state to: {'ON' if bool(args.value) else 'OFF'}")
            except DaqWriteError:
                raise
                sys.exit(f"this value is Error\n")
        else:
            sys.exit(f"Channel {channel} type is {channel_type}, not supported")


@MainParser.RegisterSubparser("io-get",[
    {"arg_name": "channel",    "type": str, "help": "io bus channel"},
    {"arg_name": "--timeout",  "type": int, "help": "", "default": 10}],
    "get io status")
def io_get(args: argparse.Namespace) -> None:
    channel = args.channel
    channel_type = get_channel_type(channel)
    if not channel_type:
        sys.exit(f"Channel {channel} is not invalid \n")
        
    with Task() as io_task:
        if channel_type is NiDeviceType.cModule_DI:
            io_task.di_channels.add_di_chan(channel)
            try:
                sys.stdout.write(str(io_task.read(timeout=args.timeout))+"\n")
            except DaqReadError:
                raise
                sys.stderr.write(f"dont have io signal\n")
        else:
            sys.exit(f"Channel {channel} type is {channel_type}, not supported")
