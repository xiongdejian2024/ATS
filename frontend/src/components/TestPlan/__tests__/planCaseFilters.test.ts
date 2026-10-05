import { it, expect } from "vitest";
import { planCaseFilterFields } from "../planCaseFilterFields";
import { functionalListingState } from "../functionalExecution";
import type { CaseTemplate } from "@/api/caseFeatures";
import { initialConditions } from "@/components/TestCase/advancedFilter";

it("计划字段覆盖官方范围，结果/人员/测试集使用关联值，缺陷数限制整数", () => {
  const fields = planCaseFilterFields(
    { id: "项目", name: "项目名称" },
    [{ id: "点", name: "测试集", count: 2 }],
    [],
    [{ id: "成员", name: "张三" }],
  );
  expect(fields.map((f) => f.key)).toEqual([
    "id",
    "name",
    "collectionId",
    "moduleId",
    "projectId",
    "priority",
    "reviewResult",
    "result",
    "requirementRef",
    "attachment",
    "tags",
    "bugCount",
    "executorId",
    "createdBy",
    "createdAt",
    "updatedBy",
    "updatedAt",
  ]);
  expect(fields.find((f) => f.key === "executorId")?.options).toEqual([
    { label: "当前用户", value: "CURRENT_USER" },
    { label: "张三", value: "成员" },
  ]);
  expect(fields.find((f) => f.key === "collectionId")?.options?.[0]).toEqual({
    label: "默认测试集",
    value: "__default__",
  });
  expect(fields.find((f) => f.key === "bugCount")).toMatchObject({
    min: 0,
    precision: 0,
  });
  expect(fields.find((f) => f.key === "projectId")?.options).toEqual([
    { label: "项目名称", value: "项目" },
  ]);
  expect(
    initialConditions(fields, undefined, [
      "id",
      "name",
      "moduleId",
      "collectionId",
    ]).map((c) => [c.field, c.operator]),
  ).toEqual([
    ["id", "contains"],
    ["name", "contains"],
    ["moduleId", "belongs_to"],
    ["collectionId", "belongs_to"],
  ]);
});

it("计划自定义字段仍复用日期、否、零和多选类型，不能混成文本", () => {
  const fields = planCaseFilterFields(
    { id: "项目", name: "项目" },
    [],
    [
      {
        id: "模板",
        name: "模板",
        defaults: {},
        isDefault: false,
        fields: [
          {
            key: "date",
            name: "日期",
            type: "date",
            options: [],
            required: false,
            default: null,
          },
          {
            key: "enabled",
            name: "启用",
            type: "boolean",
            options: [],
            required: false,
            default: null,
          },
        ],
      } as CaseTemplate,
    ],
    [],
  );
  expect(fields.find((f) => f.key === "customFields.date")).toMatchObject({
    type: "date",
    showTime: false,
  });
  expect(
    fields.find((f) => f.key === "customFields.enabled")?.options?.[1].value,
  ).toBe(false);
});

it("执行深链接保留完整高级OR和个人视图，非法JSON由后端拒绝，不能静默放宽范围", () => {
  const raw = JSON.stringify({
    conditions: [
      { field: "result", operator: "equals", value: "passed" },
      { field: "executorId", operator: "belongs_to", value: ["CURRENT_USER"] },
    ],
    logic: "or",
  });
  expect(
    functionalListingState({ caseFilters: raw, caseViewId: "视图" }),
  ).toMatchObject({ filters: raw, viewId: "视图" });
  expect(functionalListingState({ caseFilters: "{" }).filters).toBe("{");
  expect(functionalListingState({ caseFilters: ["重复"] }).filters).toBe(
    '["重复"]',
  );
});
