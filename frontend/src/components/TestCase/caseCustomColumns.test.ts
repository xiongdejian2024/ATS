import { describe, it, expect } from "vitest";
import {
  caseCustomColumns,
  caseCustomValue,
  retainUnavailableCaseColumns,
} from "./caseCustomColumns";
import { normalizeDisplay } from "@/components/Table/tableDisplay";

describe("用例自定义字段列和异步目录偏好", () => {
  it("未加载列保留相对顺序，提交包含隐藏草稿时采用本次完整顺序", () => {
    const base = [
      { key: "id", title: "ID", required: true },
      { key: "name", title: "名称", required: true },
      { key: "tags", title: "标签" },
    ];
    const original = {
      columns: [
        { key: "id", visible: true },
        { key: "name", visible: true },
        { key: "customFields.model", visible: true, width: 200 },
        { key: "tags", visible: true },
      ],
    };
    const normalized = normalizeDisplay(original, base),
      saved = retainUnavailableCaseColumns(normalized, original, base);
    expect(saved.columns.map((c) => c.key)).toEqual([
      "id",
      "name",
      "customFields.model",
      "tags",
    ]);
    const submitted = [
      ...normalized.columns,
      { key: "customFields.model", visible: false, width: 400 },
    ];
    const changed = retainUnavailableCaseColumns(
      normalized,
      original,
      base,
      submitted,
    );
    expect(changed.columns.map((c) => c.key)).toEqual([
      "id",
      "name",
      "tags",
      "customFields.model",
    ]);
    expect(changed.columns.at(-1)).toEqual({
      key: "customFields.model",
      visible: false,
      width: 400,
    });
  });
  it("只映射稳定自定义字段编号，重复目录不会重复列或伪造服务端排序", () => {
    const fields = [
      { key: "name", label: "名称", type: "text" },
      { key: "customFields.model", label: "车型", type: "select" },
      { key: "customFields.model", label: "更新车型名称", type: "select" },
      { key: "customFields.__proto__", label: "拒绝", type: "text" },
    ] as any;
    const columns = caseCustomColumns(fields);
    expect(columns).toHaveLength(1);
    expect(columns[0]).toMatchObject({
      key: "customFields.model",
      title: "更新车型名称",
      dataIndex: ["customFields", "model"],
      sorter: false,
      defaultVisible: false,
    });
  });
  it("保留false和0，日期和多选显示文本，HTML当普通文本", () => {
    expect(caseCustomValue(false)).toBe("否");
    expect(caseCustomValue(0)).toBe("0");
    expect(caseCustomValue(["A", "B"])).toBe("A、B");
    expect(caseCustomValue([])).toBe("-");
    expect(caseCustomValue("2026-10-08", "date")).toBe("2026-10-08");
    expect(caseCustomValue("<img src=x>")).toBe("<img src=x>");
  });
  it("字段未加载时保存基础列不丢自定义偏好；目录到达后恢复宽度和可见性", () => {
    const base = [
      { key: "id", title: "ID", required: true },
      { key: "name", title: "名称", required: true },
    ];
    const original = {
      columns: [
        { key: "id", visible: true },
        { key: "name", visible: true },
        { key: "customFields.model", visible: true, width: 260 },
        { key: "obsolete", visible: true, secret: "discard" },
      ],
      pageSize: 30,
    };
    const saved = retainUnavailableCaseColumns(
      normalizeDisplay(original, base),
      original,
      base,
    );
    expect(saved.columns).toContainEqual({
      key: "customFields.model",
      visible: true,
      width: 260,
    });
    expect(JSON.stringify(saved)).not.toContain("secret");
    expect(saved.columns.some((c) => c.key === "obsolete")).toBe(false);
    const available = [
      ...base,
      { key: "customFields.model", title: "车型", defaultVisible: false },
    ];
    const restored = normalizeDisplay(saved, available);
    expect(
      restored.columns.find((c) => c.key === "customFields.model"),
    ).toEqual({ key: "customFields.model", visible: true, width: 260 });
    expect(restored.pageSize).toBe(30);
    const hiddenDraft = retainUnavailableCaseColumns(
      normalizeDisplay(saved, base),
      saved,
      base,
      [{ key: "customFields.model", visible: false, width: 400 }],
    );
    expect(
      hiddenDraft.columns.find((c) => c.key === "customFields.model"),
    ).toEqual({ key: "customFields.model", visible: false, width: 400 });
    expect(
      normalizeDisplay(hiddenDraft, available).columns.find(
        (c) => c.key === "customFields.model",
      ),
    ).toEqual({ key: "customFields.model", visible: false, width: 400 });
  });
});
