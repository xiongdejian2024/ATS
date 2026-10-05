import { describe, it, expect } from "vitest";
import { filterFieldCatalog } from "./filterFieldCatalog";
import { operatorsFor, selectionValues } from "./advancedFilter";
import type { CaseTemplate } from "@/api/caseFeatures";

describe("官方人员与自定义筛选字段目录", () => {
  it("人员提供动态当前用户及项目成员，文本附件不混入人员选项", () => {
    const catalog = filterFieldCatalog(
      [
        { fieldKey: "createdBy", fieldLabel: "创建人", fieldType: "member" },
        { fieldKey: "updatedBy", fieldLabel: "更新人", fieldType: "member" },
        { fieldKey: "attachment", fieldLabel: "关联附件", fieldType: "text" },
      ],
      [],
      [{ id: "用户甲", name: "张三" }],
    );
    expect(catalog[0].options).toEqual([
      { label: "当前用户", value: "CURRENT_USER" },
      { label: "张三", value: "用户甲" },
    ]);
    expect(catalog[1].options).toEqual(catalog[0].options);
    expect(catalog[2].options).toBeUndefined();
    expect(operatorsFor(catalog[0]).map((o) => o.value)).toEqual([
      "belongs_to",
      "not_belongs_to",
      "is_empty",
      "is_not_empty",
    ]);
    expect(selectionValues("用户甲")).toEqual(["用户甲"]);
  });
  it("自定义日期仅选日期，系统时间仍选时分秒；否与多选使用正确值类型", () => {
    const fields = [
      { key: "deadline", name: "截止日期", type: "date", options: [] },
      { key: "enabled", name: "启用", type: "boolean", options: [] },
      {
        key: "choices",
        name: "环境",
        type: "multiselect",
        options: ["甲", "乙"],
      },
    ].map((f) => ({
      ...f,
      required: false,
      default: null,
    })) as CaseTemplate["fields"];
    const catalog = filterFieldCatalog(
      [{ fieldKey: "createdAt", fieldLabel: "创建时间", fieldType: "date" }],
      [{ id: "模板", name: "模板", fields, defaults: {}, isDefault: false }],
      [],
    );
    expect(catalog[0].showTime).toBeUndefined();
    expect(catalog[1].showTime).toBe(false);
    expect(catalog[2].options?.[1].value).toBe(false);
    expect(catalog[3].type).toBe("select");
    expect(catalog[3].options?.map((o) => o.value)).toEqual(["甲", "乙"]);
  });
});
