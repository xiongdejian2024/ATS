# Agent 日志：持久队列、重连补传和容量边界

## 交付语义

新版控制端在 welcome/auth_success 中声明 `capabilities: ["log_batch_v1"]`。Agent 将 suite/task 日志先提交到本地 SQLite 队列，再逐批发送。每个持久 stream 使用随机 UUID，序号单调递增；控制端在同一数据库事务中追加原始日志并更新游标，commit 成功以后才发送累计 ACK。丢失 ACK / 断线 / Agent 重启会重发，已提交序号不重复追加。

这是「持久队列 + 至少一次传输 + 同一 stream/sequence 的幂等入库」，不是端到端 exactly-once。浏览器实时队列仍是有界、可丢弃实时视窗；它不参与 Agent ACK。断线后的完整事实来源仍是控制端持久日志。

- 序号缺口返回 NACK，不跳过缺失段。
- 数据库写入/commit 失败不 ACK，Agent 保留并重试。
- suite 日志的 execution/suite/environment 必须匹配控制端 TaskQueue 任务，错误归属不入库。direct-task 没有对应持久 TaskQueue 指派记录，仅绑定当前认证 environment + task_id；不能推断它经过 suite 的任务归属检查。
- 累计 ACK 有意覆盖同一 stream 内多个执行，只清理该 stream 已发送且确认持久化的连续前缀。
- ACK 只能回收本 stream、已经发送到控制端的序号；无关 stream、未来序号不能清理队列。
- 新版 session fencing 合并后，batch/ACK 还必须归属于当前认证连接。
- 一个 Agent 工作目录只供一个 Agent 进程、一个控制端/environment 使用。不能共享或随意替换队列文件。

## 容量和行为

| 部位 | 默认边界 | 满额行为 |
| --- | --- | --- |
| Agent 待确认队列 | 64 MiB UTF-8 序列化 payload / 8192 条，以先达到者为准 | 等待 ACK 回收空间，反压输出读取，不驱逐未确认记录 |
| SQLite 文件 | `max_page_count` 限制约 `2 × payload 配额 + 2 MiB` | 写入失败进入反压；DELETE rollback journal 有额外的页/日志头/文件系统开销，预留约另一个数据库文件的空间 |
| 每条 payload | 16 KiB | 大消息按最多 2000 Unicode 字符分块；续块不额外插入换行 |
| 每批 / 在途 | 64 KiB payload JSON / 64 条 / 1 个等待确认批次 | ACK 到达后继续；未确认约每秒重试，新增输出不触发重复风暴 |
| 任务结果摘要 | 尾部 65536 Unicode 字符 + 少量说明 | 明确显示省略字符数；不把全部日志塞入结果 JSON |
| 本地 direct-task 日志副本（含时间/级别） | 单文件 16 MiB / 该类合计 64 MiB / 1024 文件 | 明确报告配额错误并停止对应子进程，不自动删除证据 |
| 本地 XAT 原始副本 | 单执行 16 MiB / XAT 各执行副本合计 64 MiB / 1024 文件 | 同上；与 direct-task 配额分别计量 |
| 控制端新版日志原文 | 每执行或 direct-task 256 MiB UTF-8 | 整批回滚并 NACK `execution_log_quota`，Agent 保留未确认批次 |
| 浏览器历史/实时 | 继续沿用既有尾部查询、队列/视窗限额 | 无需为这一协议扩大浏览器内存 |

本地 SQLite 使用 FULL synchronous、DELETE journal；ACK 删除和序号状态同事务提交。磁盘已满、权限错误或队列配额用尽会明确记日志，执行的输出读取等待恢复，心跳/取消任务继续由独立协程处理。直接任务和 XAT 先写有界本地副本，再提交 spool。被用户取消、进程崩溃或 timeout 时，尚未从操作系统管道读取/尚未提交 spool 的输出无法承诺保留。硬件/文件系统不遵守 fsync 或磁盘损坏也不在耐久保证内。

ACK 失败不影响现有结果/完成消息 outbox，两套队列仍独立。任务完成消息不表示浏览器已收到全部日志，也不代表日志队列已清空。

## 配置和恢复

在现有 Agent YAML 的 `logging` 节点内配置：

```yaml
logging:
  log_spool_max_bytes: 67108864
  log_spool_max_records: 8192
  task_log_max_bytes: 16777216
  task_logs_total_bytes: 67108864
```

Agent spool 路径是启动配置工作目录下的 `log-spool.sqlite3`。它不随控制端后续 welcome 下发的工作目录切换，防止重连后旧队列被遗落。应为 Agent 配置固定工作目录并保留该文件及正在使用的 journal。

控制端可通过 `ATS_MAX_EXECUTION_LOG_BYTES` 配置单执行上限。新增表是 `agent_log_cursors` 和 `agent_task_logs`，可在维护窗口使用 `backend/migrations/add_agent_log_delivery.py` 的幂等 upgrade；现有建表流程也会创建新增表。此改动不迁移或删除旧日志。

处理 NACK/满额时先归档所需本地原始副本或按需求增大配额；不要删除未 ACK spool 来「恢复」。`gap` 且控制端要求的序号已不存在，表示游标/备份/工作目录不一致，需要人工核对，不能宣称日志完整。不可恢复 NACK 会停止该 stream 自动发送并保留证据；控制端同时向执行人（或节点创建人）保存一条去重的站内诊断通知。Agent 在配额反压或永久拒绝期间生成终态时，将原因写入持久 completion message，并由完成通知展示，不等待日志空间。解决归属/配额/游标问题后重启 Agent 重试。一个 stream 覆盖该 Agent 所有日志，因此某执行被拒绝会阻塞同 stream 后续日志，这是选择保存证据的显式反压边界。

## 兼容性与明确未完成的边界

- 日志协议支持 UTF-8 文本，保留空白、换行、CR/tab 和跨读取块 Unicode。包含 NUL 的二进制输出明确 NACK `unsupported_nul`，整批不入库、spool 保留并进入可见阻塞；不能宣称支持二进制日志。SQLite `length/substr(TEXT)` 无法正确处理 NUL，需要后续字节流/分块存储设计。
- 新控制端仍接受旧 `test_suite_log`。旧协议没有序号或持久 ACK，无法提供补传去重；旧 handler 的历史 LONGTEXT 追加行为保持兼容。
- 支持 session v2 但没有 `log_batch_v1` capability 的控制端，新 Agent 明确警告后使用旧日志消息，socket send 成功即回收。完全不支持 session v2 的旧控制端会被新版 Agent 拒绝连接，不会进入此降级路径。该模式是 best-effort，不能将 send 成功解释为控制端入库成功。升级回 durable 模式时，保留的剩余数据原子变成新的 stream，避免将旧 socket-send 序号当成控制端游标；旧发送过的部分无法追溯保证。
- 新版 ingestion 用数据库端 append 和长度投影，不把完整历史载入 Python；底层仍是 LONGTEXT，数据库可能复制整段内容。它不是分块对象存储，也没有全局跨执行 retention。单执行配额不等于控制端总磁盘配额。
- 原日志小 JSON 请求保持兼容；超预算请求明确返回 413。浏览器现在使用带授权的冻结快照/有界分段导出，直接逐段写文件或逐次下载编号片段，不在内存合并整份日志；见[原始日志有界下载](原始日志有界下载.md)。控制端底层分块存储/全局保留策略仍是独立后续工作。
- direct-task 日志有独立持久表；现有产品没有相应日志浏览 UI。本提交不新增通用 API 测试功能或报告系统。
- 只在隔离 SQLite、loopback HTTP/WS 和软件子进程中验证；未动生产、硬件、网络/安全设置，未宣称 MySQL 故障恢复/多控制端 HA 或磁盘断电实测。

## 验证

`tests/test_agent_log_delivery.py` 覆盖：重开 SQLite、未确认配额不淘汰、磁盘满反压/取消、失 ACK 后重试、重复/重叠 batch、缺口/错误归属 NACK、事务提交失败、整批配额回滚、SQL 不读完整历史、大 Unicode/控制转义分块、旧协议升级、单在途避免重复风暴、本地日志配额与结果摘要。

有界 soak 连续把超过 30 MiB 内容送过 256 KiB payload 队列（8000 条），验证 Python 峰值低于 3 MiB、磁盘复用且不超过 page cap。真实 HTTP + WebSocket + Agent + XAT 用例在控制端已提交、ACK 被丢弃后断线，离线继续生成输出并重连补传，验证无重复原文、结果完成以及现有尾部/全文 API。

### 2026-10-08 三分钟实际观测

报告：`docs/validation/agent-log-soak-2026-10-08.json`。隔离真实 SQLite 入库，真实磁盘 spool，传输 fault harness（不是网络吞吐测量）：前 20% 正常；20–40% 断线；40–70% ACK 延迟 120ms（超过 100ms 重试周期）；后 30% 恢复并排空。

- 180.04 秒，生产 / 入库 12,200 条；原始 payload 文本 2,549,800 bytes，持久原文加消息分隔符为 2,561,999 bytes。
- 发送 1,211 批、16,870 条 wire records，处理 1,210 次 ACK；重试没有扩大最终记录数。
- pending 峰值 128 条 / 39,808 bytes（128 条额度确实触发了反压），SQLite 文件峰值 61,440 bytes；结束 pending 0 条 / 0 bytes。
- Python tracemalloc 峰值 996,880 bytes；慢 ACK 的延迟任务峰值 3。
- 独立控制心跳探针运行 3,066 次，最大间隔 1.221 秒。同步 SQLite/文件 I/O 仍会造成事件循环延迟，不宣称硬实时；网络断线和满队列没有阻止探针继续运行。
- 另有短期 8,000 条 / 超过 30 MiB 的磁盘复用压力测试，以及独立真实 loopback WebSocket 断线补传测试。不同测试各自证明其边界，不将 harness 吞吐说成生产网络或 MySQL 性能。
