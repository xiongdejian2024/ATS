# XAT 用例包

原 SAT 用例已迁入 `src/xat_cases/legacy` 和 `src/xat_cases/dp2`。原 ECU 库的测试和示例在 `src/xat_cases/library_archive`，库发布包不包含 pytest 测试代码。用例通过 `framework` fixture 和 `xat_ecu` API 调用能力，不修改库源码。

本包独立维护版本，独立提交；GitHub 只做静态语法检查，不执行车辆/台架用例。日常软件用例可通过 XAT CLI 显式指定 `--tests`；设备模式需要节点配置和明确硬件开关。原用例所需的 JSON、CSV、Excel、YAML、协议等输入资源保留；凭证改为用户提供环境变量。
