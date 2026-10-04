# XAT 自动化测试框架

XAT 由 ATS 仓库内的源码维护。原 SAT 的 pytest 生命周期、Hook、参数、调度与报告代码位于 `framework/automotive`；原 ECU Simulator 的协议、驱动、车型库和 SDK 接口位于独立的 `packages/ecu`。运行时不读取旧 SAT 或 ECU 仓库。

框架、库、用例分别打包和检查：

| 部分 | 开发目录 | 独立安装 |
|---|---|---|
| pytest 框架 | `xat/framework` | `pip install -e ./xat` |
| ECU 库 | `xat/packages/ecu/src/xat_ecu` | `pip install -e './xat/packages/ecu[protocols]'` |
| 用例与输入数据 | `xat/cases/src/xat_cases` | `pip install -e ./xat/cases` |

框架自身不安装 ECU 库；库不导入 pytest、Allure、框架或用例。需要 ECU 的用例由使用方安装对应库和可选设备依赖。原用例使用 `xat_ecu.api` 公共接口，库里的共享状态和配置协议不再依赖用例代码。GitHub 按三个目录分别触发检查。

在 ATS 根目录安装上述框架和库后运行软件验收：

```bash
python -m framework --mode offline --output-dir /tmp/xat-results
```

ATS 前端任务命令为 `xat --mode offline`。Agent 使用配置的 Python 解释器启动同一框架，传入选中的用例和独立输出目录；完成后回传日志、结果、JUnit 和报告。

目前公共 fixture 为 `sat_runtime`、`sat_types`、`ecu_profile`、`ecu_simulator`、`ecu_sdk_options`、`ecu_sdk`。`sat_*` 名称为已有用例兼容入口，源码已归属 XAT。`ecu_simulator` 使用逐用例隔离的内存传输；`ecu_sdk` 仅允许显式台架模式。迁入生命周期支持模块、类、函数前后置，清理失败会记录为错误。

真实台架入口默认关闭。本次不执行台架 Hook、车辆用例、刷写或设备连接。车型生成代码及设备绑定的静态迁移不代表硬件兼容性验收。原模块化库的刷写 API 是占位实现，现明确拒绝报告成功；原实际刷写源码保留在独立库 `legacy/ecu_sim/sd_tester.py`。

原项目缺少车型依赖的历史工具按用户选择保留在 `tools/archive/ecu`，不作为可运行功能。具体来源、归档与凭证注入清单见 [功能迁移记录](../docs/XAT功能迁移.md) 和 [使用说明](../docs/XAT_SAT_ECU_INTEGRATION.md)。原 XAT 的故意失败示例仍保留，结果会准确报告失败。
