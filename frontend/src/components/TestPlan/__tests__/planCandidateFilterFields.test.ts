import { it, expect } from "vitest";
import { planCandidateFilterFields } from "../planCandidateFilterFields";
import {
  operatorsFor,
  initialConditions,
} from "@/components/TestCase/advancedFilter";

it("功能关联字段使用主用例结果，计划归属只提供官方等于，默认三条件", () => {
  const fields = planCandidateFilterFields(
    { id: "项目", name: "项目" },
    [{ id: "计划", name: "真实计划" }],
    [],
    [{ id: "成员", name: "张三" }],
    "functional",
  );
  const keys = fields.map((f) => f.key);
  expect(keys).toEqual(
    expect.arrayContaining([
      "id",
      "name",
      "moduleId",
      "reviewResult",
      "status",
      "requirementRef",
      "attachment",
      "planIds",
      "createdBy",
      "createdAt",
      "updatedBy",
      "updatedAt",
      "tags",
      "priority",
    ]),
  );
  for (const key of ["result", "collectionId", "bugCount", "executorId"])
    expect(keys).not.toContain(key);
  expect(
    operatorsFor(fields.find((f) => f.key === "planIds")).map((o) => o.value),
  ).toEqual(["equals"]);
  expect(fields.find((f) => f.key === "planIds")?.options).toEqual([
    { label: "真实计划", value: "计划" },
  ]);
  expect(initialConditions(fields).map((c) => c.field)).toEqual([
    "id",
    "name",
    "moduleId",
  ]);
  expect(fields.find((f) => f.key === "createdBy")?.options?.[0].value).toBe(
    "CURRENT_USER",
  );
});

it("API及场景共同字段不会出现功能评审与关联实例字段", () => {
  for (const category of ["api", "scenario"]) {
    const keys = planCandidateFilterFields(
      { id: "项目", name: "项目" },
      [],
      [],
      [],
      category,
    ).map((f) => f.key);
    for (const key of [
      "reviewResult",
      "result",
      "collectionId",
      "bugCount",
      "executorId",
    ])
      expect(keys).not.toContain(key);
    expect(keys).toContain("status");
    expect(keys).toContain("planIds");
  }
});
