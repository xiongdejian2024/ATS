import type { FilterField } from "@/components/TestCase/advancedFilter";
import type { PlanGroup } from "@/api/planOrchestration";
export function planIndexFilterFields(
  members: { id: string; name: string }[],
  groups: PlanGroup[],
): FilterField[] {
  return [
    { key: "id", label: "计划 ID", type: "text" },
    { key: "planNumber", label: "编号", type: "text" },
    { key: "name", label: "名称", type: "text" },
    { key: "description", label: "描述", type: "text" },
    {
      key: "status",
      label: "状态",
      type: "select",
      options: [
        { value: "not_started", label: "未开始" },
        { value: "running", label: "进行中" },
        { value: "completed", label: "已完成" },
        { value: "paused", label: "已暂停" },
        { value: "overdue", label: "已逾期" },
      ],
    },
    {
      key: "planType",
      label: "类型",
      type: "select",
      options: [
        { value: "manual", label: "手动测试" },
        { value: "automated", label: "自动化测试" },
        { value: "mixed", label: "混合测试" },
        { value: "functional", label: "功能测试" },
      ],
    },
    {
      key: "ownerId",
      label: "负责人",
      type: "member",
      options: [
        { value: "CURRENT_USER", label: "当前用户" },
        ...members.map((m) => ({ value: m.id, label: m.name })),
      ],
    },
    { key: "moduleId", label: "所属模块", type: "module" },
    {
      key: "groupId",
      label: "计划组",
      type: "select",
      options: [
        { value: "__ungrouped__", label: "未分组" },
        ...groups.map((g) => ({ value: g.id, label: g.name })),
      ],
    },
    { key: "tags", label: "标签", type: "tags" },
    ...[
      ["archived", "归档"],
      ["followed", "我关注的"],
    ].map(([key, label]) => ({
      key,
      label,
      type: "select" as const,
      options: [
        { value: "true", label: "是" },
        { value: "false", label: "否" },
      ],
    })),
    ...[
      ["createdAt", "创建时间"],
      ["updatedAt", "更新时间"],
      ["startDate", "开始日期"],
      ["endDate", "结束日期"],
    ].map(([key, label]) => ({ key, label, type: "date" as const })),
  ];
}
