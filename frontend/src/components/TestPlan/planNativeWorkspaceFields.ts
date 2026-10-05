import type { CaseFolder } from "@/api/planCaseWorkspace";
import {
  nativeReportOptions,
  type NativeFilterCatalog,
} from "@/api/nativeCase";
import type { FilterField } from "@/components/TestCase/advancedFilter";
import { planCaseFilterFields } from "./planCaseFilterFields";
import { planCandidateFilterFields } from "./planCandidateFilterFields";

export const planNativeResultOptions = [
  { label: "未执行", value: "PENDING" },
  { label: "执行中", value: "RUNNING" },
  ...nativeReportOptions,
  { label: "跳过", value: "SKIPPED" },
];

/** 官方计划原生字段顺序；执行结果/执行人是关联实例语义，环境来自配置。 */
export function planNativeWorkspaceFields(
  project: { id: string; name: string },
  collections: CaseFolder[],
  members: { id: string; name: string }[],
  category: "api" | "scenario",
  native?: NativeFilterCatalog,
  projects?: { id: string; name: string }[],
): FilterField[] {
  const fields = new Map(
    [
      ...planCaseFilterFields(project, collections, [], members, projects),
      ...planCandidateFilterFields(
        project,
        [],
        [],
        members,
        category,
        native,
      ).filter((f) =>
        [
          "nativeState",
          "protocol",
          "path",
          "environmentName",
          "stepTotal",
        ].includes(f.key),
      ),
    ].map((field) => [field.key, field]),
  );
  fields.set("result", {
    key: "result",
    label: "执行结果",
    type: "select",
    options: planNativeResultOptions,
  });
  fields.get("environmentName")!.label = "执行环境";
  if (category === "scenario") {
    fields.get("name")!.label = "场景名称";
    fields.get("priority")!.label = "场景等级";
  }
  const order =
    category === "api"
      ? [
          "id",
          "name",
          "collectionId",
          "moduleId",
          "projectId",
          "protocol",
          "priority",
          "result",
          "nativeState",
          "bugCount",
          "path",
          "environmentName",
          "tags",
          "executorId",
          "createdBy",
          "createdAt",
          "updatedBy",
          "updatedAt",
        ]
      : [
          "id",
          "name",
          "collectionId",
          "moduleId",
          "projectId",
          "priority",
          "nativeState",
          "result",
          "tags",
          "bugCount",
          "environmentName",
          "stepTotal",
          "executorId",
          "createdBy",
          "createdAt",
          "updatedBy",
          "updatedAt",
        ];
  return order.map((key) => fields.get(key)!);
}

export function planNativeColumns(category: "api" | "scenario") {
  const definition = (
    key: string,
    title: string,
    width: number,
    defaultVisible = true,
    sorter = false,
  ) => ({
    key,
    title,
    width,
    defaultVisible,
    sorter,
    required: ["caseCode", "name"].includes(key),
    dataIndex: key,
    ellipsis: true,
  });
  const id = definition("caseCode", "ID", 150, true, true);
  const name = definition(
    "name",
    category === "api" ? "用例名称" : "场景名称",
    150,
    true,
    true,
  );
  const collection = definition("collectionName", "测试集", 150);
  const level = definition(
    "priority",
    category === "api" ? "用例等级" : "场景等级",
    150,
  );
  const result = definition(
    "nativeResult",
    "执行结果",
    category === "api" ? 150 : 200,
  );
  const state = definition("nativeState", "状态", 150, false);
  const created = definition("createdAt", "创建时间", 200, true, true);
  const updated = definition("updatedAt", "更新时间", 200, true, true);
  const module = definition("moduleName", "所属模块", 200);
  const bugs = definition("bugCount", "缺陷数", 100);
  const project = definition("projectName", "所属项目", 150);
  const environment = definition(
    "nativeExecutionEnvironmentName",
    "执行环境",
    150,
    false,
  );
  const creator = definition("createdByName", "创建人", 130);
  const executor = definition("nativeExecutorName", "执行人", 130);
  return category === "api"
    ? [
        id,
        name,
        definition("protocol", "协议", 150),
        collection,
        created,
        updated,
        bugs,
        level,
        result,
        state,
        definition("path", "路径", 200, false),
        module,
        project,
        environment,
        creator,
        executor,
      ]
    : [
        id,
        name,
        collection,
        level,
        result,
        state,
        created,
        updated,
        module,
        bugs,
        project,
        environment,
        creator,
        executor,
      ];
}
