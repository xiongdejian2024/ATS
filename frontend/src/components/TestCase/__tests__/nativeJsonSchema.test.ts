import { describe, expect, it } from "vitest";
import {
  readJsonSchema,
  jsonToSchema,
  schemaToRows,
  rowsToSchema,
  newSchemaRow,
} from "../nativeJsonSchema";

describe("MS Schema 树形协议与导入", () => {
  it("保留对象必填、禁用节点、元组顺序与全部高级字段", () => {
    const schema = {
      type: "object",
      properties: {
        list: {
          type: "array",
          items: [
            {
              type: "integer",
              example: "7",
              defaultValue: 9,
              minimum: 1,
              maximum: 10,
              enumValues: ["7", "8"],
              enable: false,
            },
            {
              type: "string",
              example: "中文",
              defaultValue: "缺省",
              pattern: "[A-Z]{3}",
              format: "date",
              minLength: 1,
              maxLength: 10,
              description: "说明",
            },
          ],
          minItems: 1,
          maxItems: 4,
        },
      },
      required: ["list"],
    };
    const rows = schemaToRows(readJsonSchema(JSON.stringify(schema)));
    expect(rows.children![0].required).toBe(true);
    expect(rows.children![0].children!.map((c) => c.title)).toEqual(["0", "1"]);
    expect(rowsToSchema(rows)).toMatchObject(schema);
  });
  it("JSON批量转换保留null/布尔/嵌套数值，浮点与整数均按MS转number", () => {
    const schema = jsonToSchema(
      '{"n":7,"f":true,"empty":null,"a":["中文",2.5,{"v":false}]}',
    );
    expect(schema.properties!.n).toMatchObject({
      type: "number",
      example: "7",
    });
    expect(schema.properties!.f).toMatchObject({
      type: "boolean",
      example: "true",
    });
    expect(schema.properties!.empty.type).toBe("null");
    expect(schema.properties!.a.items![2].properties!.v.example).toBe("false");
  });
  it("空尾行不进入Schema，重复名不能折叠覆盖，__proto__是普通JSON键", () => {
    const root = schemaToRows(
      readJsonSchema(
        '{"type":"object","properties":{"__proto__":{"type":"string"}}}',
      ),
    );
    root.children!.push(newSchemaRow());
    expect(Object.keys(rowsToSchema(root).properties!)).toEqual(["__proto__"]);
    root.children!.push(newSchemaRow("__proto__"));
    expect(() => rowsToSchema(root)).toThrow("重复");
  });
  it.each([
    '{"type":"string"}',
    '{"type":"object","$ref":"http://external.test"}',
    '{"type":"array","items":{"type":"string"}}',
    '{"type":"object","required":["missing"]}',
    '{"type":"object","properties":{"a":{"type":"string","minLength":4,"maxLength":3}}}',
    '{"type":"object","properties":{"a":{"type":"integer","enumValues":[]}}}',
  ])("拒绝非法草稿且不生成替代树 %s", (raw) =>
    expect(() => readJsonSchema(raw)).toThrow(),
  );
});
