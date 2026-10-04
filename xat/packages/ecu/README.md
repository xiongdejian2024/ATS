# XAT ECU 库

此包由 XAT 维护，公开入口为 `xat_ecu`。库的安装、导入和使用不依赖 pytest、XAT 测试框架或用例目录。协议、驱动、传输、业务服务和车型数据各自分层；设备库按需安装对应 extra。

```bash
pip install -e xat/packages/ecu
```

开发测试依赖放在 `test` extra 中，不进入运行时依赖。库代码提交在此目录，用例提交在 `xat/cases`，pytest 框架提交在 `xat/framework`。迁移范围和当前未完成部分见仓库的 `docs/XAT功能迁移.md`。

原车型库在 `xat_ecu.legacy`，原公共 SDK 接口在 `xat_ecu.api`。这些均由 XAT 自有源码提供，不读取旧项目。公共业务接口按方法加载驱动和平台依赖；运行库不依赖 pytest、Allure 或用例。框架通过 `xat_ecu.reporting.set_reporter` 注入报告接收器。

车型生成代码、配置、驱动绑定和原真实刷写实现已迁入。现代 `VehicleSDK.flash` 原先为占位实现，已禁止直接报告成功；车型刷写仍由 `xat_ecu.legacy.ecu_sim.sd_tester.Sd_Tester` 的真实实现提供。实际刷写未执行。

可选能力依赖分别安装：`[can]`、`[ssh]`、`[serial]`、`[security]`、`[network]`、`[protocols]`。私有平台集成仍需要对应平台维护的依赖及用户凭证，默认导入不会加载它们。
