# MS V3 用例与计划功能交付记录

日期：2026-10-05。功能独立实现于 ATS，保留 Python 后端、ATS 品牌与 SAT/ECU/XAT 执行器。按用户要求分批提交并推送 GitHub。本轮验收不执行真实台架，不连接真实AI服务。

## 完成范围

用例：列表与筛选视图、批量操作、模块、可编辑脑图、模板/自定义字段、真实附件、需求/缺陷/用例/自动化关联、评论关注、回收站、Excel/CSV/XMind导入导出、独立评审及历史。

计划：模块标签/日期筛选、关注归档和完整复制；功能/API/场景三类测试点、层级配置继承、重复关联、分工、串并行与失败策略；计划组整组执行/定时/聚合报告；独立快照批次、手工逐步骤回填、证据与缺陷、总结、中文PDF、限时可撤销分享。

## 验证结果

| 检查 | 实际结果 |
| --- | --- |
| Python完整软件回归 | `python -m pytest tests -q`：141 passed，16 warnings，74.47秒 |
| 最后计划组/PDF定向回归 | 9 passed |
| 前端单元测试 | 12 passed |
| 前端类型检查/生产构建 | 通过；最终构建9.71秒 |
| GitHub业务代码检查 | `94bf58d` 的[工作流37224450840](https://github.com/xiongdejian2024/ATS/actions/runs/37224450840)全部成功 |
| 浏览器真实离线计划组 | 4条Agent/XAT软件用例+1条手工逐步骤回填，组及成员全部完成，5/5通过 |
| 报告PDF | 页面下载，中文文本、实际步骤结果、结论与风险均正确 |
| 分享 | 页面创建后200；页面撤销后404 |
| 数据迁移 | 备份后增量升级，隔离副本原39表旧列逐行SHA256一致，幂等再次执行0步骤 |
| 正式数据与服务 | 100条用例、7个计划；页面读取正常、后端healthy、原Agent在线、活动任务0 |

已有Pydantic/SQLAlchemy等弃用或关系配置警告和前端大包提示保留，未影响本轮测试。浏览器实测范围详见 `MS-V3用例计划对齐清单.md` 与各模块文档；复杂权限、并发、多个评审人的结论组合、过期与幂等主要通过软件回归验证。

## 服务与证据

正式服务：[ATS](http://127.0.0.1:5173)。后端：http://127.0.0.1:8000/health。Docker继续提供原MySQL、Redis、RabbitMQ、MinIO；后端、Agent和Celery使用其原数据运行。

隔离18805/13305服务及两个迁移验证数据库已关闭/删除；正式服务继续运行。原数据备份保存在 `/Users/xiongdejian/Library/Application Support/ATS/docker/ms-v3-backup-20261005-015714`，包含私有配置，不提交GitHub。

本地证据（不提交业务内容）：
- `evidence/ms-v3-group-run.json`：最终组批次5项100%完成。
- `evidence/ms-v3-cases.xlsx`、`evidence/ms-v3-cases.xmind`：页面真实导出，重新上传校验5条均有效。
- `evidence/ms-v3-plan-report.pdf`、`evidence/ms-v3-group-report.pdf`：页面下载的中文报告。
- `evidence/ms-v3-mind-desktop-final.png`、`ms-v3-mind-narrow-final.png`：脑图桌面与窄屏。
- `evidence/ms-v3-plan-narrow-final.png`、`ms-v3-group-desktop.png`、`ms-v3-group-narrow.png`：执行报告与组报告视觉核验。
- `evidence/ms-v3-live-cases.png`、`ms-v3-live-plans.png`、`ms-v3-live-api.json`：正式服务原数据与接口读取。
- `/tmp/ats-ms-delivery-full-tests.log`：最终软件回归日志。

## 功能边界

本次实现用例和计划工作流；API/场景通过ATS现有执行模板运行。未复制MeterSphere完整Java API调试引擎、全部商业插件或全部平台，界面保留ATS品牌，不宣称像素级1:1。本轮未执行真实台架；AI配置维持可设置能力，未接真实模型。
