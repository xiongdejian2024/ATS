import { filterFieldCatalog } from "@/components/TestCase/filterFieldCatalog";
import type { FilterField } from "@/components/TestCase/advancedFilter";
import type { CaseTemplate } from "@/api/caseFeatures";
import type { CaseFolder } from "@/api/planCaseWorkspace";
import { functionalResultLabels } from "./functionalExecution";

/** 官方计划字段及项目模板；结果和执行人使用计划关联语义。 */
export function planCaseFilterFields(
  project: { id: string; name: string },
  collections: CaseFolder[],
  templates: CaseTemplate[],
  members: { id: string; name: string }[],
): FilterField[] {
  const fields = [
    ["id", "ID", "text"],
    ["name", "用例名称", "text"],
    [
      "collectionId",
      "测试集",
      "select",
      [
        { label: "默认测试集", value: "__default__" },
        ...collections.map((c) => ({ label: c.name, value: c.id })),
      ],
    ],
    ["moduleId", "所属模块", "module"],
    [
      "projectId",
      "所属项目",
      "select",
      [{ label: project.name, value: project.id }],
    ],
    [
      "priority",
      "用例等级",
      "select",
      ["P0", "P1", "P2", "P3"].map((value) => ({ label: value, value })),
    ],
    [
      "reviewResult",
      "评审结果",
      "select",
      Object.entries({
        not_reviewed: "未评审",
        pending: "待评审",
        passed: "已通过",
        rejected: "不通过",
        resubmit: "重新提审",
      }).map(([value, label]) => ({ value, label })),
    ],
    [
      "result",
      "执行结果",
      "select",
      Object.entries(functionalResultLabels).map(([value, label]) => ({
        value,
        label,
      })),
    ],
    ["requirementRef", "关联需求", "text"],
    ["attachment", "关联附件", "text"],
    ["tags", "标签", "tags"],
    ["bugCount", "缺陷数", "number"],
    ["executorId", "执行人", "member"],
    ["createdBy", "创建人", "member"],
    ["createdAt", "创建时间", "date"],
    ["updatedBy", "更新人", "member"],
    ["updatedAt", "更新时间", "date"],
  ].map(([fieldKey, fieldLabel, fieldType, options]) => ({
    fieldKey,
    fieldLabel,
    fieldType,
    options,
  }));
  return filterFieldCatalog(fields, templates, members).map((field) =>
    field.key === "bugCount" ? { ...field, min: 0, precision: 0 } : field,
  );
}
