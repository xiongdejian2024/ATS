import { it, expect } from "vitest";
import { planCandidateFilterFields } from "../planCandidateFilterFields";

it("接口模式使用定义字段，用例等级、变更和用例环境不混入", () => {
  const fields = planCandidateFilterFields(
    { id: "来源", name: "来源" },
    [],
    [],
    [],
    "api",
    undefined,
    "API",
  );
  expect(fields.map((f) => f.key)).toEqual([
    "id",
    "name",
    "moduleId",
    "protocol",
    "method",
    "path",
    "nativeState",
    "tags",
    "caseTotal",
    "planIds",
    "createdBy",
    "createdAt",
    "updatedBy",
    "updatedAt",
  ]);
  expect(fields.find((f) => f.key === "name")?.label).toBe("接口名称");
});
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
    expect(keys).not.toContain("status");
    expect(keys).toContain("nativeState");
    expect(keys).toContain("lastReportStatus");
    expect(keys).toContain("environmentName");
    expect(keys).toContain("planIds");
  }
});

it("原生高级字段提供真实协议环境、独立状态和最近结果及严格布尔变更", () => {
  const catalog = {
    definitions: [],
    environments: [
      {
        id: "环境",
        name: "隔离接口环境",
        address: "http://127.0.0.1",
        revision: 1,
      },
    ],
    protocols: ["HTTP", "TCP"],
    canCreate: true,
    canEdit: true,
  };
  const api = planCandidateFilterFields(
    { id: "项目", name: "项目" },
    [],
    [],
    [],
    "api",
    catalog,
  );
  expect(api.find((f) => f.key === "protocol")?.options).toEqual([
    { label: "HTTP", value: "HTTP" },
    { label: "TCP", value: "TCP" },
  ]);
  expect(api.find((f) => f.key === "environmentName")?.options).toEqual([
    { label: "隔离接口环境", value: "环境" },
  ]);
  expect(
    api.find((f) => f.key === "nativeState")?.options?.map((o) => o.value),
  ).toEqual(["PROCESSING", "DEPRECATED", "DONE"]);
  expect(
    operatorsFor(api.find((f) => f.key === "apiChange")).map((o) => o.value),
  ).toEqual(["equals"]);
  expect(
    api.find((f) => f.key === "apiChange")?.options?.map((o) => o.value),
  ).toEqual([false, true]);
  expect(
    api.find((f) => f.key === "lastReportStatus")?.options?.map((o) => o.value),
  ).toEqual(["SUCCESS", "ERROR", "FAKE_ERROR"]);
  expect(api.map((field) => field.key)).toEqual([
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
  ]);
  expect(
    api
      .find((field) => field.key === "lastReportStatus")
      ?.options?.find((option) => option.value === "FAKE_ERROR")?.label,
  ).toBe("误报");
  const scene = planCandidateFilterFields(
    { id: "项目", name: "项目" },
    [],
    [],
    [],
    "scenario",
    catalog,
  );
  expect(
    scene.find((f) => f.key === "nativeState")?.options?.map((o) => o.value),
  ).toEqual(["UNDERWAY", "DEPRECATED", "COMPLETED"]);
  expect(scene.find((f) => f.key === "stepTotal")).toMatchObject({
    type: "number",
    min: 0,
    precision: 0,
  });
  for (const key of [
    "protocol",
    "path",
    "apiChange",
    "attachment",
    "requirementRef",
  ])
    expect(scene.map((f) => f.key)).not.toContain(key);
});
