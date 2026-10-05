import {
  nativeStateOptions,
  nativeReportOptions,
  type NativeCatalog,
} from "@/api/nativeCase";
import type { CaseTemplate } from "@/api/caseFeatures";
import type { FilterField } from "@/components/TestCase/advancedFilter";
import { planCaseFilterFields } from "./planCaseFilterFields";

/** 关联候选使用主用例结果与所属计划，不混入计划实例结果或执行人。 */
export function planCandidateFilterFields(
  project: { id: string; name: string },
  plans: { id: string; name: string }[],
  templates: CaseTemplate[],
  members: { id: string; name: string }[],
  category: string,
  native?: NativeCatalog,
): FilterField[] {
  const excluded = new Set([
    "collectionId",
    "projectId",
    "result",
    "bugCount",
    "executorId",
  ]);
  if (category !== "functional") excluded.add("reviewResult");
  const fields = planCaseFilterFields(project, [], templates, members).filter(
    (f) => !excluded.has(f.key),
  );
  fields.splice(4, 0, {
    key: "status",
    label: "执行结果",
    type: "select",
    options: Object.entries({
      not_executed: "未执行",
      pending: "待执行",
      running: "执行中",
      passed: "通过",
      failed: "失败",
      blocked: "阻塞",
      error: "错误",
      skipped: "跳过",
    }).map(([value, label]) => ({ value, label })),
  });
  fields.splice(7, 0, {
    key: "planIds",
    label: "所属测试计划",
    type: "select",
    operators: ["equals"],
    operatorsOnly: true,
    options: plans.map((p) => ({ value: p.id, label: p.name })),
  });
  if (category !== "functional") {
    const commonKeys = new Set([
      "id",
      "name",
      "moduleId",
      "priority",
      "tags",
      "planIds",
      "createdBy",
      "createdAt",
      "updatedBy",
      "updatedAt",
    ]);
    const common = fields.filter((f) => commonKeys.has(f.key));
    const extra: FilterField[] = [
      {
        key: "nativeState",
        label: "状态",
        type: "select",
        options: nativeStateOptions(category),
      },
      {
        key: "lastReportStatus",
        label: "执行结果",
        type: "select",
        options: nativeReportOptions,
      },
      {
        key: "environmentName",
        label: category === "api" ? "用例环境" : "场景环境",
        type: "select",
        options: (native?.environments || []).map((e) => ({
          label: e.name,
          value: e.id,
        })),
      },
    ];
    if (category === "api")
      extra.unshift(
        {
          key: "protocol",
          label: "协议",
          type: "select",
          options: (native?.protocols || []).map((value) => ({
            label: value,
            value,
          })),
        },
        {
          key: "apiChange",
          label: "接口参数变更",
          type: "select",
          operators: ["equals"],
          operatorsOnly: true,
          options: [
            { label: "无变更", value: false },
            { label: "有变更", value: true },
          ],
        },
        { key: "path", label: "路径", type: "text" },
      );
    else
      extra.push({
        key: "stepTotal",
        label: "步骤数",
        type: "number",
        min: 0,
        precision: 0,
      });
    const fieldMap = new Map(
      [...common, ...extra].map((field) => [field.key, field]),
    );
    const priority = fieldMap.get("priority")!;
    priority.label = category === "api" ? "用例等级" : "场景等级";
    if (category === "scenario") fieldMap.get("name")!.label = "场景名称";
    const order =
      category === "api"
        ? [
            "id",
            "name",
            "moduleId",
            "protocol",
            "priority",
            "apiChange",
            "path",
            "nativeState",
            "lastReportStatus",
            "planIds",
            "environmentName",
            "tags",
            "createdBy",
            "createdAt",
            "updatedBy",
            "updatedAt",
          ]
        : [
            "id",
            "name",
            "moduleId",
            "priority",
            "nativeState",
            "lastReportStatus",
            "tags",
            "environmentName",
            "stepTotal",
            "planIds",
            "createdBy",
            "createdAt",
            "updatedBy",
            "updatedAt",
          ];
    return order.map((key) => fieldMap.get(key)!);
  }
  return fields;
}
