import type { FilterField } from "@/components/TestCase/advancedFilter";
import { reviewStates } from "@/components/Table/reviewColumns";

export function reviewIndexFilterFields(
  members: { id: string; name: string }[],
): FilterField[] {
  const memberOptions = [
    { label: "当前用户", value: "CURRENT_USER" },
    ...members.map((m) => ({ label: m.name, value: m.id })),
  ];
  return [
    { key: "id", label: "评审 ID", type: "text" },
    { key: "number", label: "编号", type: "number", min: 1, precision: 0 },
    { key: "name", label: "名称", type: "text" },
    { key: "description", label: "描述", type: "text" },
    { key: "lifecycle", label: "状态", type: "select", options: reviewStates },
    {
      key: "mode",
      label: "模式",
      type: "select",
      options: [
        { label: "单人", value: "single" },
        { label: "多人", value: "multiple" },
      ],
    },
    { key: "moduleId", label: "所属模块", type: "module" },
    {
      key: "reviewerId",
      label: "评审人",
      type: "member",
      options: memberOptions,
    },
    {
      key: "createdBy",
      label: "创建人",
      type: "member",
      options: memberOptions,
    },
    { key: "tags", label: "标签", type: "tags" },
    { key: "caseCount", label: "用例数", type: "number", min: 0, precision: 0 },
    {
      key: "passRate",
      label: "通过率 (%)",
      type: "number",
      min: 0,
      precision: 2,
    },
    ...[
      ["createdAt", "创建时间"],
      ["startTime", "开始时间"],
      ["endTime", "结束时间"],
    ].map(([key, label]) => ({ key, label, type: "date" as const })),
  ];
}
