# XAT 的 SAT / ECU Simulator 集成

目标目录是当前 ATS 仓库内的 `xat/`。同级独立 `python_project/xat` 不属于本次修改范围。

## 架构与使用

XAT 管理 pytest Hook、fixture、用例选择和结果；SAT 提供原框架的数据类型、配置和台架用例；ECU 项目的 `automotive_sdk` 提供模拟与 SDK 服务。现有源码通过路径配置加载，不复制到 ATS，也不自动执行设备初始化。

ATS 前端 → 后端队列 → Agent → XAT → SAT / ECU 模块 → XAT 结果 → Agent ACK 补传 → ATS 入库、统计和报告。

前端“测试任务”编辑器选择“使用 XAT 软件验收”，命令为 `xat --mode offline`。Agent 从自身配置读取源码与 Python 路径，启动 `python -m framework`；进程超时、取消、并发隔离和磁盘补传由 Agent 管理。旧 `ats-sat` 命令兼容，但同样通过 XAT 执行。单用例执行、取消、重连结果恢复均支持两种命令。

在 ATS 根目录运行：

```bash
PYTHONPATH=xat .venv-integration/bin/python -m framework \
  --mode offline \
  --sat-root ../sat --ecu-root ../ecu-simulator \
  --output-dir /tmp/xat-software-check
```

也可以安装 XAT 后使用入口：

```bash
uv pip install --python .venv-integration/bin/python -e ./xat --no-deps
.venv-integration/bin/xat --mode offline \
  --sat-root ../sat --ecu-root ../ecu-simulator \
  --output-dir /tmp/xat-software-check
```

`--no-deps` 仅适用于已经按 `requirements-integration.txt` 安装依赖的环境。全新环境应安装 XAT 声明的依赖。日志、JSON 结果和 JUnit XML 在输出目录中。

## XAT 用例中的 fixture

```python
def test_caseid_response(ecu_simulator, sat_types):
    ecu_simulator.start_simulation(ecus=["ECU"])
    ecu_simulator.set_mock_response("ECU", 0x22, b"OK")
    assert ecu_simulator.get_response_for("ECU", 0x22) == b"\x62OK"
    assert sat_types.ReportInfo(total=1, passed=1).passed == 1
```

- `sat_types`：原 SAT 的 `utils.data_type` 模块。
- `sat_runtime`：原 SAT 数据类型、台架 YAML 和用例 YAML；在台架模式中可按需导入其他 SAT 模块。
- `ecu_simulator`：原 ECU SDK 的 `SimulatorService`，每个测试独立创建，结束后自动停止和清空。
- `ecu_profile`：默认 `None`，用例可覆盖为 SDK 的车型配置。
- `ecu_sdk`：原 `VehicleSDK` 的诊断、总线、信号、刷写与模拟服务入口；需要台架模式、硬件许可，并覆盖 `ecu_sdk_options` 提供车型与版本等参数。通过上下文管理器清理资源。

自定义软件用例使用 `--tests /path/to/test_software.py`。离线模式显式加载 XAT Hook 和集成插件，关闭 SAT conftest 及插件自动加载，不初始化台架设备。

## 用例选择与准确结果

`--selection /path/to/selection.json` 接受编号到 ATS ID 的映射：

```json
{"ecu_positive": "case-uuid-1", "ecu_negative": "case-uuid-2"}
```

同时兼容原 `test_cases.json` 的 `case_codes` / `case_ids` 数组；编号和 ID 必须一一对应，拒绝空选择和重复编号。未传选择文件时运行全部收集到的用例。

支持完整 pytest node ID、`ats_case` 标记、参数化 ID、SAT 的 `_caseid_` 单编号和多数字编号。结果在 setup/call/teardown 全部结束后写入；setup 或 teardown 失败记为 error。所选用例未完成会产生 error，进程不能返回成功。

XAT 原来的故意失败示例保持不变。直接运行该文件仍是 2 通过、1 失败，自动验收验证这一真实行为。

## 台架入口与边界

默认禁止台架模式。显式允许后，原 SAT conftest 加载原 Hook 和 `ecu` fixture，保留既有 SAT 用例运行流程，同时使用 XAT 选择和结果适配：

```bash
PYTHONPATH=xat .venv-integration/bin/python -m framework \
  --mode sat --allow-hardware \
  --sat-root /path/to/sat --ecu-root /path/to/ecu-simulator \
  --tests test_case/your_domain/test_your_feature.py \
  --bench-config bench_config/your_bench.yaml \
  --case-config test_case/your_domain/config/latest_config.yaml \
  --output-dir /path/to/run-output
```

上面的命令是台架使用说明，本次未执行。真实 SAT 依赖、原 ECU 硬件与网络初始化需要台架环境；软件验收只证明 XAT 的接入、fixture 生命周期和结果行为，以及实际 SAT 数据类型 / ECU 内存模拟功能。

也可直接使用 pytest：先设置 `PYTHONPATH=xat`，加载 `-p framework.hooks -p framework.integrations.plugin`，传入 `--xat-mode offline`、`--sat-root`、`--ecu-root`、`--xat-results`。XAT 目录内的 `conftest.py` 已注册两个插件。
