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
  return fields;
}
