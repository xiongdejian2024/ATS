# MeterSphere V3 用例与计划对齐记录

基线：2026-10-05 核对的 MeterSphere V3 官方手册及 v3.6.9-lts。保留 ATS 品牌、Python 后端和 SAT / ECU / XAT 执行器；独立实现功能和交互，不引入 Java。验收只使用隔离数据库与离线软件节点，不执行真实台架。

官方资料：
- 用例：https://metersphere.io/docs/v3.x/user_manual/test_case/test_case/
- 评审：https://metersphere.io/docs/v3.x/user_manual/test_case/test_case_review/
- 模板：https://metersphere.io/docs/v3.x/user_manual/project_management/template_management/
- 计划：https://metersphere.io/docs/v3.x/user_manual/test_plan/test_plan/
- 报告：https://metersphere.io/docs/v3.x/user_manual/test_plan/test_plan_report/

## 验收清单

只有代码、持久化、权限、软件测试和浏览器操作均检查后，才能记为完成。已有回归通过不代表以下功能等价。

| 功能组 | 必需行为 | 状态 |
| --- | --- | --- |
| 用例基础管理 | 模块层级与排序、字段与步骤、筛选视图、批量操作 | 开发中 |
| 脑图 | 模块→用例→前置/步骤/预期，编辑、增删、复制、快捷键、刷新保持 | 开发中 |
| 用例模板 | 可编辑默认模板、自定义字段与值；社区版基线为一套默认模板 | 开发中 |
| 导入导出 | Excel/CSV、XMind，选择范围、步骤拆分、重复覆盖选项 | 开发中 |
| 关联追踪 | 需求、缺陷、前后置用例、自动化用例、关联评审和计划 | 开发中 |
| 用例协作 | 真实附件、评论、关注通知、分享、变更记录 | 开发中 |
| 回收站 | 软删除、恢复、明确彻底删除 | 开发中 |
| 评审 | 单人最后有效结论、多人全通过、建议、逐条评审人、周期、复制编辑、批量、重提审、历史、脑图 | 开发中 |
| 计划管理 | 模块与标签、日期筛选、关注归档、批量管理、完整复制 | 开发中 |
| 计划组 | 整组执行、定时、聚合报告 | 开发中 |
| 计划编排 | 功能/API/场景、测试点树、上级配置继承、环境节点、重复关联、自动更新关联结果 | 开发中 |
| 计划执行 | 串并行、失败停止、阈值、分工、逐步骤结果、评论附件缺陷、脑图执行 | 开发中 |
| 计划报告 | 独立批次、总结、测试点与缺陷明细、分享有效期、中文 PDF | 开发中 |
| 现有功能 | 原用例/计划/套、Agent/XAT、任务调度、可配置 AI 回归；原数据保持 | 待回归 |

## 开发日志

- 2026-10-05：用户授权按官方功能清单复刻。启动用例后端、用例前端、计划前后端三个并行工作；主线程负责整合、迁移、PDF 和浏览器验收。每个可验收功能分批提交并推送 GitHub。
- 2026-10-05：现有 ECharts 用于脑图布局，保留现有 Vue/Ant Design；现有依赖没有 PDF 引擎，选择 ReportLab，使用 pypdf 检查导出内容。XMind XML 使用 defusedxml 解析，不自行实现 XML 解析器。
