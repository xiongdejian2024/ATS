import type { FilterField } from "@/components/TestCase/advancedFilter";
import { reportResultOptions } from "@/api/planReports";
export function reportIndexFilterFields(
  members: { id: string; name: string }[],
): FilterField[] {
  return [
    { key: "id", label: "报告 ID", type: "text" },
    { key: "name", label: "报告名称", type: "text" },
    { key: "planName", label: "所属计划名称", type: "text" },
    { key: "operator", label: "操作人姓名", type: "text" },
    {
      key: "kind",
      label: "报告类型",
      type: "select",
      options: [
        { value: "PLAN", label: "普通报告" },
        { value: "GROUP", label: "集成报告" },
      ],
    },
    {
      key: "resultStatus",
      label: "结果",
      type: "select",
      options: [
        ...reportResultOptions,
        { value: "completed", label: "已完成" },
      ],
    },
    {
      key: "triggerMode",
      label: "触发方式",
      type: "select",
      options: [
        { value: "manual", label: "手动触发" },
        { value: "cron", label: "定时触发" },
      ],
    },
    {
      key: "executorId",
      label: "操作人",
      type: "member",
      options: [
        { value: "CURRENT_USER", label: "当前用户" },
        ...members.map((m) => ({ value: m.id, label: m.name })),
      ],
    },
    {
      key: "passRate",
      label: "通过率 (%)",
      type: "number",
      min: 0,
      precision: 2,
    },
    { key: "createTime", label: "操作时间", type: "date" },
    { key: "completedAt", label: "结束时间", type: "date" },
  ];
}
