"""独立 ECU 库验收，全部使用内存传输，不访问硬件或旧仓库。"""
import ast
from collections import deque
from pathlib import Path
import subprocess
import sys

import pytest

from xat_ecu import VehicleSDK
from xat_ecu.core.errors import DiagnosticError, HardwareError, TimeoutError
from xat_ecu.core.events import Event, EventBus, EventType
from xat_ecu.core.plugin import PluginRegistry
from xat_ecu.core.types import BusMessage, BusType, EcuInfo
from xat_ecu.hal.adapter import BaseHardwareAdapter
from xat_ecu.protocol.doip.payload import DoipPayloadBuilder, DoipPayloadParser
from xat_ecu.services.diagnostic import DiagnosticService
from xat_ecu.services.flash import FlashService
from xat_ecu.transport.can import CANTransport
from xat_ecu.vehicle.base import VehicleProfile


class MemoryTransport:
    bus_type = BusType.CAN
    is_open = False

    def __init__(self, responses=()):
        self.responses = deque(responses)
        self.sent = []

    def open(self, config):
        self.is_open = True

    def close(self):
        self.is_open = False

    def send_message(self, message):
        self.sent.append(message.data)

    def receive_message(self, timeout):
        if self.responses:
            return BusMessage(msg_id=0, data=self.responses.popleft())
        return None


def profile():
    result = VehicleProfile("软件测试", "1")
    result.ecu_map["BGM"] = EcuInfo(name="BGM")
    result.ecu_map["TCAM"] = EcuInfo(name="TCAM")
    return result


def diagnostic(responses):
    transport = MemoryTransport(responses)
    service = DiagnosticService(profile(), lambda *args, **kwargs: transport)
    service.connect("BGM")
    return service, transport


def test_sdk_constructs_and_cleans_injected_transport():
    transport = MemoryTransport([b"\x62\xf1\x90VIN"])
    calls = []

    def factory(**kwargs):
        calls.append(kwargs)
        return transport

    with VehicleSDK("软件测试", "1", profile=profile(), transport_factory=factory) as sdk:
        sdk.diagnostic.connect("BGM")
        result = sdk.diagnostic.read_did(0xF190)
        assert result.is_positive and result.data == b"\xf1\x90VIN"
    assert transport.sent == [b"\x22\xf1\x90"]
    assert calls[0]["transport_type"] == "doip"
    assert not transport.is_open


def test_unknown_vehicle_fails_with_traceback(tmp_path, caplog):
    with pytest.raises(ValueError):
        VehicleSDK("缺失车型", "1", config_dir=str(tmp_path))
    assert any(record.exc_info for record in caplog.records)


def test_vehicle_configuration_loads_without_original_repository(tmp_path):
    folder = tmp_path / "vehicle_data" / "软件测试" / "1"
    folder.mkdir(parents=True)
    (folder / "ecu_network.yaml").write_text("ecu_map_id:\n  BGM: [4098, 1792, 1800, null, null, '127.0.0.1', null]\n")
    with VehicleSDK("软件测试", "1", config_dir=str(tmp_path)) as sdk:
        assert sdk.profile.get_ecu_info("BGM").doip_id == 4098


def test_negative_response_preserves_nrc():
    service, transport = diagnostic([b"\x7f\x22\x31"])
    response = service.read_did(0xF190)
    assert not response.is_positive and response.nrc == 0x31


def test_pending_and_unrelated_responses_are_filtered():
    service, transport = diagnostic([b"\x50\x01", b"\x7f\x11\x78", b"\x7f\x22\x78", b"\x62\xf1\x90VIN"])
    assert service.read_did(0xF190).raw_data == b"\x62\xf1\x90VIN"


def test_pending_cannot_extend_total_deadline(monkeypatch):
    service, transport = diagnostic([b"\x7f\x22\x78"] * 10)
    ticks = iter([0, 0.1, 0.2, 1.1])
    monkeypatch.setattr("xat_ecu.services.diagnostic.time.monotonic", lambda: next(ticks))
    with pytest.raises(TimeoutError):
        service.send_raw(b"\x22\xf1\x90", timeout=1)


def test_security_access_removes_subfunction_from_seed():
    service, transport = diagnostic([b"\x67\x01\x12\x34", b"\x67\x02"])
    seen = []

    def algorithm(seed, level):
        seen.append((seed, level))
        return b"\xab\xcd"

    assert service.security_access(1, algorithm).is_positive
    assert seen == [(b"\x12\x34", 1)]
    assert transport.sent[-1] == b"\x27\x02\xab\xcd"


def test_missing_security_algorithm_cannot_echo_seed():
    service, transport = diagnostic([b"\x67\x71\x12\x34"])
    with pytest.raises(DiagnosticError):
        service.security_access(0x71)
    assert len(transport.sent) == 1


def test_can_receives_one_message_only():
    class Adapter:
        is_connected = True
        calls = 0

        def recv_message(self, timeout):
            self.calls += 1
            return {"msg_id": 123, "data": b"\x01"}

        def receive(self, timeout):
            raise AssertionError("扩展接收接口不应再调用原始接收")

    adapter = Adapter()
    transport = CANTransport(adapter)
    transport.open({})
    assert transport.receive_message().msg_id == 123
    assert adapter.calls == 1


def test_simulator_lifecycle_and_responses():
    with VehicleSDK("软件测试", "1", profile=profile()) as sdk:
        sdk.simulator.start_simulation(exclude_dut=["TCAM"])
        assert sdk.simulator.get_simulated_ecus() == ["BGM"]
        sdk.simulator.set_mock_response("BGM", 0x22, b"\xf1\x90VIN")
        assert sdk.simulator.get_response_for("BGM", 0x22) == b"\x62\xf1\x90VIN"
        sdk.simulator.set_nrc("BGM", 0x22, 0x31)
        assert sdk.simulator.get_response_for("BGM", 0x22) == b"\x7f\x22\x31"
    assert not sdk.simulator.is_running
    assert sdk.simulator.get_simulated_ecus() == []


def test_doip_encoding_and_invalid_headers():
    payload = DoipPayloadBuilder.build_diagnostic_message(0xE80, 0x1002, b"\x22\xf1\x90")
    header = DoipPayloadBuilder.build_header(2, 0x8001, len(payload))
    assert DoipPayloadParser.parse_header(header) == (2, 0x8001, 7)
    assert DoipPayloadParser.parse_diagnostic_message(payload) == (0xE80, 0x1002, b"\x22\xf1\x90")
    assert DoipPayloadParser.parse_header(b"\x02\x02" + header[2:]) is None


def test_event_failure_keeps_other_subscribers_and_traceback(caplog):
    bus = EventBus()
    bus.clear()
    seen = []

    def fail(event):
        raise RuntimeError("测试订阅者异常")

    kind = next(iter(EventType))
    bus.subscribe(kind, fail)
    bus.subscribe(kind, seen.append)
    event = Event(kind)
    bus.publish(event)
    assert seen == [event]
    assert any(record.exc_info for record in caplog.records)
    bus.clear()


def test_plugin_factory_can_register_dependency():
    PluginRegistry.clear()

    def factory():
        PluginRegistry.register("依赖", object())
        return "实例"

    PluginRegistry.register_factory("测试", factory)
    assert PluginRegistry.get("测试") == "实例"
    PluginRegistry.clear()


def test_unimplemented_flash_never_reports_success():
    flash = FlashService(None)
    for call in [lambda: flash.flash_standard_ecu("不存在.bin"), lambda: flash.verify_flash("BGM"), lambda: flash.download_firmware("https://example.invalid/firmware")]:
        with pytest.raises(NotImplementedError):
            call()


def test_library_import_and_execution_does_not_load_test_framework():
    script = '''
import sys, importlib.abc
class BlockTestFramework(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname.split(".")[0] in {"pytest", "framework", "allure", "test_case", "sat_framework", "ecu_simulator", "automotive_sdk", "sdk_interface", "xat_cases"}:
            raise RuntimeError("库依赖了框架或旧模块：" + fullname)
sys.meta_path.insert(0, BlockTestFramework())
from xat_ecu import VehicleSDK
from xat_ecu.vehicle.base import VehicleProfile
with VehicleSDK("软件测试", "1", profile=VehicleProfile("软件测试", "1")) as sdk:
    sdk.simulator.start_simulation(ecus=["BGM"])
    assert sdk.simulator.get_response_for("BGM", 0x22) == b"\\x62"
from xat_ecu.api import CommonBusComm, CommonSdTest, AbcBusComm
assert hasattr(CommonBusComm, "__init__")
assert not {"groot2", "paramiko", "scapy", "can"}.intersection(sys.modules)
'''
    subprocess.run([sys.executable, "-I", "-c", script], check=True, capture_output=True, text=True)


def test_modular_library_has_no_reverse_imports():
    root = Path(__file__).parents[1] / "src" / "xat_ecu"
    blocked = {"pytest", "allure", "framework", "xat_cases", "test_case", "sat_framework", "sdk_interface", "ecu_simulator", "automotive_sdk"}
    for path in root.rglob("*.py"):
        if "legacy" in path.parts or "api" in path.parts:
            continue
        for node in ast.walk(ast.parse(path.read_text(), filename=str(path))):
            names = [alias.name for alias in node.names] if isinstance(node, ast.Import) else [node.module or ""] if isinstance(node, ast.ImportFrom) and not node.level else []
            assert all(name.split(".")[0] not in blocked for name in names), str(path)
