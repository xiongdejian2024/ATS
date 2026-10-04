"""验证迁入原库和资源的实际行为，不加载任何台架设备。"""
import importlib
import pytest

from xat_ecu import reporting
from xat_ecu.resources import LEGACY_ROOT, resolve_environment
from xat_ecu.legacy.common.data_type_handing import DataTypeHanding, slotid_cyclecode_to_msgid, msgid_to_slotid
from xat_ecu.api.call_tracker import ObjExecutor


def test_legacy_data_conversion_and_flexray_identifier():
    assert DataTypeHanding.to_bytes('01ab') == b'\x01\xab'
    assert DataTypeHanding.to_int([0x01, 0xAB]) == 427
    value = slotid_cyclecode_to_msgid(12, 4)
    assert msgid_to_slotid(value)[0] == 12


def test_vehicle_signal_classes_are_local_and_complete():
    module = importlib.import_module('xat_ecu.legacy.sdk.data.mars1.can_lin_fr_cls.v_1_4_0.connectivitycanfd')
    message = module.DrmfrConnectivityFr03
    assert message.msg_id == 504 and message.msg_length == 64
    assert message.FrntRgtRdrObj7ObjBoxCenterLat.sig_length == 8
    assert 'xat_ecu/legacy' in module.__file__.replace('\\', '/')


def test_call_tracker_preserves_shared_lifecycle_instance():
    assert ObjExecutor() is ObjExecutor()
    assert isinstance(ObjExecutor().start_cache, list)


def test_public_interfaces_do_not_load_unrelated_platforms():
    from xat_ecu.api import CommonBusComm, CommonSdTest, AbcBusComm, AbcSdTest
    assert hasattr(CommonBusComm, '__init__')
    assert hasattr(CommonSdTest, '__init__')
    assert AbcBusComm.__abstractmethods__
    assert AbcSdTest.__abstractmethods__


def test_reporting_injection_and_failure_logs(caplog):
    seen = []
    class Reporter(reporting.LoggingReporter):
        def step(self, title):
            seen.append(title)
            return super().step(title)
    old = reporting.set_reporter(Reporter())
    try:
        with pytest.raises(RuntimeError):
            with reporting.step('软件协议操作'):
                raise RuntimeError('测试异常')
        assert seen == ['软件协议操作']
        assert any(record.exc_info for record in caplog.records)
    finally:
        reporting.set_reporter(old)


def test_config_credentials_are_required_and_resolved(monkeypatch):
    value = {'password': '${XAT_CREDENTIAL_TEST_CONFIG}'}
    monkeypatch.delenv('XAT_CREDENTIAL_TEST_CONFIG', raising=False)
    with pytest.raises(ValueError, match='缺少配置凭证'):
        resolve_environment(value)
    monkeypatch.setenv('XAT_CREDENTIAL_TEST_CONFIG', '软件测试凭证')
    assert resolve_environment(value) == {'password': '软件测试凭证'}


def test_driver_and_vehicle_assets_belong_to_library():
    assert (LEGACY_ROOT / 'sdk/ecu_sim_const.py').is_file()
    assert (LEGACY_ROOT / 'sdk/driver/toomoss/sdk/api/python/ldf_parser.py').is_file()


def test_config_protocol_round_trip():
    pytest.importorskip('google.protobuf')
    from xat_ecu.api.config_center.ConfigMasterV2T_pb2 import ConfSyncData
    from xat_ecu.api.config_center.VehicleCloud_pb2 import VehicleCloudInvoke
    config = ConfSyncData(PbVer='V1', Timestamp=123, ModelName='软件测试', ModelYear='2026')
    config.Confs.add(Domain='bgm', AppName='软件配置', ConfName='测试', PublishID=456, Value=b'{"enabled":true}')
    envelope = VehicleCloudInvoke(body=config.SerializeToString())
    envelope.header.ver = '1'
    restored = VehicleCloudInvoke.FromString(envelope.SerializeToString())
    decoded = ConfSyncData.FromString(restored.body)
    assert decoded.ModelName == '软件测试'
    assert decoded.Confs[0].PublishID == 456
    assert decoded.Confs[0].Value == b'{"enabled":true}'
