import { cloneDeep } from "lodash-es";
export interface FilterCondition {
  field: string;
  operator: string;
  value?: any;
}
export interface FilterField {
  key: string;
  label: string;
  type: "text" | "select" | "number" | "date" | "tags" | "module";
  operators?: string[];
  options?: { label: string; value: any }[];
}
export type FilterLogic = "and" | "or";
export type ViewSaveMode = "create" | "update" | "copy";
export const filterOperators: Record<string, string> = {
  contains: "包含",
  not_contains: "不包含",
  equals: "等于",
  not_equals: "不等于",
  is_empty: "为空",
  is_not_empty: "不为空",
  belongs_to: "属于",
  not_belongs_to: "不属于",
  in: "属于",
  not_in: "不属于",
  gt: "大于",
  lt: "小于",
  gte: "大于等于",
  lte: "小于等于",
  between: "介于",
  count_gt: "数量大于",
  count_lt: "数量小于",
};
const common = {
  text: [
    "contains",
    "not_contains",
    "is_empty",
    "is_not_empty",
    "equals",
    "not_equals",
  ],
  select: ["belongs_to", "not_belongs_to", "is_empty", "is_not_empty"],
  module: ["belongs_to", "not_belongs_to"],
  number: ["gt", "lt", "equals", "is_empty", "is_not_empty"],
  date: ["between", "gt", "lt", "is_empty", "is_not_empty"],
  tags: ["is_empty", "contains", "not_contains", "count_lt", "count_gt"],
};
export const noValue = (operator: string) =>
  ["is_empty", "is_not_empty"].includes(operator);
export const collectionValue = (operator: string) =>
  ["in", "not_in", "belongs_to", "not_belongs_to"].includes(operator);
export function operatorsFor(field?: FilterField, current?: string) {
  return [
    ...new Set([
      ...(common[field?.type || "text"] || common.text),
      ...(field?.operators || []),
      ...(current ? [current] : []),
    ]),
  ]
    .filter((value) => value in filterOperators)
    .map((value) => ({ value, label: filterOperators[value] }));
}
export function initialConditions(
  fields: FilterField[],
  conditions?: FilterCondition[],
) {
  return conditions !== undefined
    ? cloneDeep(conditions)
    : ["id", "name", "moduleId"]
        .filter((key) => fields.some((f) => f.key === key))
        .map((field) => ({
          field,
          operator: field === "moduleId" ? "belongs_to" : "contains",
          value: undefined,
        }));
}
export function effectiveConditions(rows: FilterCondition[]) {
  return cloneDeep(
    rows.filter(
      (row) =>
        noValue(row.operator) ||
        (row.value !== undefined &&
          row.value !== null &&
          row.value !== "" &&
          (!Array.isArray(row.value) || row.value.length > 0)),
    ),
  );
}

export function nextUnnamedView(names: string[]) {
  for (let index = 1; index <= 10; index++) {
    const name = `未命名视图${String(index).padStart(3, "0")}`;
    if (!names.includes(name)) return name;
  }
  return "";
}

export function selectionValues(value: any): any[] {
  if (value === undefined || value === null || value === "") return [];
  return Array.isArray(value) ? value : [value];
}
