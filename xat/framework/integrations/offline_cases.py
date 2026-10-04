"""通过 XAT fixture 使用实际 SAT 和 ECU 模块，不连接台架。"""

import pytest


@pytest.mark.sat
def test_caseid_sat_import(sat_types):
    report = sat_types.ReportInfo(total=1, passed=1, failed=0)
    assert report.to_dict()["passed"] == 1
    assert sat_types.CaseStatus.finished.value == 2


@pytest.mark.ecu
def test_caseid_ecu_positive(ecu_simulator):
    ecu_simulator.set_mock_response("OFFLINE", 0x22, b"\xf1\x90ATS")
    assert ecu_simulator.get_response_for("OFFLINE", 0x22) == b"\x62\xf1\x90ATS"


@pytest.mark.ecu
def test_caseid_ecu_negative(ecu_simulator):
    ecu_simulator.set_nrc("OFFLINE", 0x22, 0x31)
    assert ecu_simulator.get_response_for("OFFLINE", 0x22) == b"\x7f\x22\x31"
    ecu_simulator.set_mock_response("OFFLINE", 0x22, b"OK")
    assert ecu_simulator.get_response_for("OFFLINE", 0x22) == b"\x62OK"


@pytest.mark.ecu
def test_caseid_ecu_lifecycle(ecu_simulator):
    ecu_simulator.start_simulation(ecus=["OFFLINE", "DUT"], exclude_dut=["DUT"])
    assert ecu_simulator.is_running
    assert ecu_simulator.get_simulated_ecus() == ["OFFLINE"]
    ecu_simulator.stop_simulation()
    assert not ecu_simulator.is_running
    assert ecu_simulator.get_response_for("OFFLINE", 0x22) is None
