# XAT ECU 库

此包由 XAT 维护，公开入口为 `xat_ecu`。库的安装、导入和使用不依赖 pytest、XAT 测试框架或用例目录。协议、驱动、传输、业务服务和车型数据各自分层；设备库按需安装对应 extra。

```bash
pip install -e xat/packages/ecu
```

开发测试依赖放在 `test` extra 中，不进入运行时依赖。库代码提交在此目录，用例提交在 `xat/cases`，pytest 框架提交在 `xat/framework`。迁移范围和当前未完成部分见仓库的 `docs/XAT功能迁移.md`。
