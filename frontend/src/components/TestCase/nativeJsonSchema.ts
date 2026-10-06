/** MS 的 items 为有序元组，defaultValue/enumValues 为编辑扩展字段。 */
export const schemaTypes = [
  "object",
  "array",
  "string",
  "number",
  "integer",
  "boolean",
  "null",
] as const;
export type SchemaType = (typeof schemaTypes)[number];
export interface JsonSchema {
  type: SchemaType;
  enable?: boolean;
  example?: string;
  description?: string;
  defaultValue?: string | number | boolean;
  properties?: Record<string, JsonSchema>;
  items?: JsonSchema[];
  required?: string[];
  enumValues?: string[];
  pattern?: string;
  format?: string;
  minLength?: number;
  maxLength?: number;
  minimum?: number;
  maximum?: number;
  minItems?: number;
  maxItems?: number;
}
export interface SchemaRow extends Omit<
  JsonSchema,
  "properties" | "items" | "required" | "enumValues"
> {
  id: string;
  title: string;
  required: boolean;
  enumValues: string;
  children?: SchemaRow[];
}
let sequence = 0;
export const emptySchema = () =>
  ({ type: "object", properties: {} }) as JsonSchema;
export const newSchemaRow = (
  title = "",
  type: SchemaType = "string",
): SchemaRow => ({
  id: `schema-${++sequence}`,
  title,
  type,
  enable: true,
  required: false,
  example: "",
  description: "",
  defaultValue: "",
  enumValues: "",
  ...(["array", "object"].includes(type) ? { children: [] } : {}),
});
export function readJsonSchema(raw: string): JsonSchema {
  const schema = JSON.parse(raw);
  let count = 0;
  function validate(node: JsonSchema, depth: number) {
    if (++count > 1000 || depth > 20)
      throw new Error("Schema最多20层、1000节点");
    if (!node || typeof node !== "object" || !schemaTypes.includes(node.type))
      throw new Error("Schema类型无效");
    if (node.enable !== undefined && typeof node.enable !== "boolean")
      throw new Error("启用状态无效");
    const fields = [
      "type",
      "enable",
      "description",
      "example",
      "defaultValue",
      "properties",
      "items",
      "required",
      "enumValues",
      "pattern",
      "format",
      "minLength",
      "maxLength",
      "minimum",
      "maximum",
      "minItems",
      "maxItems",
    ];
    if (Object.keys(node).some((k) => !fields.includes(k)))
      throw new Error("含有不支持的Schema字段");
    for (const key of ["example", "description", "pattern"] as const)
      if (
        node[key] !== undefined &&
        (typeof node[key] !== "string" ||
          node[key]!.length > (key === "pattern" ? 512 : 20000))
      )
        throw new Error("Schema文本超出限制");
    if (node.type === "object") {
      if (node.items !== undefined) throw new Error("对象不能包含数组项");
      if (
        node.properties !== undefined &&
        (!node.properties ||
          typeof node.properties !== "object" ||
          Array.isArray(node.properties))
      )
        throw new Error("对象属性格式无效");
      const entries = Object.entries(node.properties || {});
      if (
        entries.length > 200 ||
        entries.some(([name]) => !name.trim() || name.length > 255)
      )
        throw new Error("属性名称不能为空，每层最多200项");
      if (
        node.required &&
        (!Array.isArray(node.required) ||
          new Set(node.required).size !== node.required.length ||
          node.required.some(
            (k) =>
              !Object.prototype.hasOwnProperty.call(node.properties || {}, k),
          ))
      )
        throw new Error("必填名称无效");
      entries.forEach(([, child]) => validate(child, depth + 1));
    } else if (node.type === "array") {
      if (node.properties !== undefined || node.required?.length)
        throw new Error("数组不能包含对象属性");
      if (
        node.items !== undefined &&
        (!Array.isArray(node.items) || node.items.length > 200)
      )
        throw new Error("数组项格式无效或超过200项");
      (node.items || []).forEach((child) => validate(child, depth + 1));
    } else if (
      node.properties !== undefined ||
      node.items !== undefined ||
      node.required?.length
    )
      throw new Error("基础类型不能包含子节点");
    for (const [lo, hi] of [
      ["minLength", "maxLength"],
      ["minimum", "maximum"],
      ["minItems", "maxItems"],
    ] as const) {
      for (const key of [lo, hi])
        if (
          node[key] !== undefined &&
          (!Number.isFinite(node[key]) ||
            (key !== "minimum" &&
              key !== "maximum" &&
              (!Number.isInteger(node[key]) ||
                node[key]! < 0 ||
                node[key]! > (key.endsWith("Items") ? 200 : 20000))))
        )
          throw new Error("范围格式无效");
      if (
        node[lo] !== undefined &&
        node[hi] !== undefined &&
        node[lo]! > node[hi]!
      )
        throw new Error("最小值不能大于最大值");
    }
    if (
      node.enumValues !== undefined &&
      (!Array.isArray(node.enumValues) ||
        !node.enumValues.length ||
        node.enumValues.length > 200 ||
        node.enumValues.some(
          (v) => typeof v !== "string" || !v.trim() || v.length > 20000,
        ))
    )
      throw new Error("枚举格式无效");
    if (
      node.defaultValue !== undefined &&
      !["string", "number", "boolean"].includes(typeof node.defaultValue)
    )
      throw new Error("默认值格式无效");
    if (
      node.format !== undefined &&
      ![
        "date",
        "date-time",
        "email",
        "hostname",
        "ipv4",
        "ipv6",
        "url",
      ].includes(node.format)
    )
      throw new Error("格式无效");
  }
  if (!["object", "array"].includes(schema?.type))
    throw new Error("根节点只能为object或array");
  validate(schema, 1);
  return schema;
}
export function schemaToRows(
  schema: JsonSchema,
  title = "root",
  required = false,
  isRoot = true,
): SchemaRow {
  const {
    properties,
    items,
    required: requiredNames,
    enumValues,
    ...values
  } = schema;
  const row = {
    ...newSchemaRow(title, schema.type),
    ...values,
    required,
    enumValues: (enumValues || []).join("\n"),
  };
  if (schema.type === "object")
    row.children = Object.entries(properties || {}).map(([name, child]) =>
      schemaToRows(child, name, (requiredNames || []).includes(name), false),
    );
  if (schema.type === "array")
    row.children = (items || []).map((child, index) =>
      schemaToRows(child, String(index), false, false),
    );
  if (isRoot) row.id = "root";
  return row;
}
export function rowsToSchema(row: SchemaRow): JsonSchema {
  const { id, title, children, required, enumValues, ...node } = row;
  const result: JsonSchema = node;
  if (row.type === "object") {
    const active = (children || []).filter((child) => child.title !== "");
    if (new Set(active.map((c) => c.title)).size !== active.length)
      throw new Error("同层属性名称不能重复");
    result.properties = Object.fromEntries(
      active.map((child) => [child.title, rowsToSchema(child)]),
    );
    result.required = active
      .filter((child) => child.required)
      .map((child) => child.title);
  } else if (row.type === "array")
    result.items = (children || []).map(rowsToSchema);
  const enums = enumValues.split("\n").filter((value) => value.trim());
  if (enums.length) result.enumValues = enums;
  return result;
}
export function jsonToSchema(raw: string): JsonSchema {
  const value = JSON.parse(raw);
  if (value === null || typeof value !== "object")
    throw new Error("批量JSON根节点须为对象或数组");
  function convert(v: unknown): JsonSchema {
    if (v === null) return { type: "null", enable: true };
    if (Array.isArray(v))
      return { type: "array", enable: true, items: v.map(convert) };
    if (typeof v === "object")
      return {
        type: "object",
        enable: true,
        properties: Object.fromEntries(
          Object.entries(v as Record<string, unknown>).map(([k, c]) => [
            k,
            convert(c),
          ]),
        ),
        required: [],
      };
    return {
      type: typeof v as SchemaType,
      enable: true,
      example: String(v),
      defaultValue: "",
    };
  }
  return readJsonSchema(JSON.stringify(convert(value)));
}
export function walkSchema(row: SchemaRow, fn: (r: SchemaRow) => void) {
  fn(row);
  row.children?.forEach((child) => walkSchema(child, fn));
}
