import { describe, it, expect } from "vitest";
import {
  initialConditions,
  effectiveConditions,
  operatorsFor,
  nextUnnamedView,
  type FilterField,
} from "./advancedFilter";
const fields: FilterField[] = [
  { key: "id", label: "ID", type: "text" },
  { key: "name", label: "名称", type: "text" },
  { key: "moduleId", label: "模块", type: "module" },
];
describe("高级筛选草稿与持久化迁移", () => {
  it("新建视图取首个空闲编号，不覆盖已有个人视图", () => {
    expect(nextUnnamedView(["未命名视图001", "未命名视图003"])).toBe(
      "未命名视图002",
    );
  });
  it("区分系统默认条件与显式保存的零条件，并隔离草稿引用", () => {
    expect(initialConditions(fields)).toHaveLength(3);
    expect(initialConditions(fields, [])).toEqual([]);
    const saved = [
      { field: "moduleId", operator: "belongs_to", value: ["甲"] },
    ];
    const draft = initialConditions(fields, saved);
    draft[0].value.push("乙");
    expect(saved[0].value).toEqual(["甲"]);
  });
  it("空值不参与逻辑，零和否仍是有效条件", () => {
    const rows = [
      { field: "name", operator: "contains", value: "" },
      { field: "moduleId", operator: "belongs_to", value: [] },
      { field: "tags", operator: "count_gt", value: 0 },
      { field: "isAutomated", operator: "equals", value: false },
      { field: "precondition", operator: "is_empty" },
    ];
    expect(effectiveConditions(rows).map((c) => c.field)).toEqual([
      "tags",
      "isAutomated",
      "precondition",
    ]);
  });
  it("已保存的旧运算保留，同时提供日期区间与标签数量", () => {
    expect(
      operatorsFor({ key: "date", label: "时间", type: "date" }).map(
        (o) => o.value,
      ),
    ).toContain("between");
    expect(
      operatorsFor({ key: "tags", label: "标签", type: "tags" }).map(
        (o) => o.value,
      ),
    ).toContain("count_lt");
    expect(operatorsFor(fields[2], "in").map((o) => o.value)).toContain("in");
  });
});
