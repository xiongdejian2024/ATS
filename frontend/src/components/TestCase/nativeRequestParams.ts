/** 参数表保持顺序、启停和描述；旧字符串键值对象按原值载入。 */
export interface RequestParam {
  key: string;
  value: string;
  enable: boolean;
  paramType:
    | "string"
    | "integer"
    | "number"
    | "boolean"
    | "array"
    | "json"
    | "file";
  files?: import("@/api/nativeRequestFiles").FileReference[];
  required: boolean;
  encode: boolean;
  description: string;
  lengthRange: number[];
}
export const paramTypes = ["string", "integer", "number", "boolean", "array"];
export function blankParam(): RequestParam {
  return {
    key: "",
    value: "",
    enable: true,
    paramType: "string",
    required: false,
    encode: true,
    description: "",
    lengthRange: [],
  };
}
export function readParams(raw: string): RequestParam[] {
  const value = JSON.parse(raw);
  if (!value || typeof value !== "object")
    throw new Error("参数须为对象或参数列表");
  const rows = Array.isArray(value)
    ? value
    : Object.entries(value).map(([key, item]) => {
        if (typeof item !== "string") throw new Error("请求参数值须为字符串");
        return { key, value: item };
      });
  return rows.map((row) => {
    if (
      !row ||
      typeof row !== "object" ||
      typeof row.key !== "string" ||
      typeof row.value !== "string"
    )
      throw new Error("参数须包含字符串名称和值");
    return { ...blankParam(), ...row };
  });
}
export function filledParams<T extends RequestParam>(rows: T[]): T[] {
  return rows.filter(
    (row) =>
      row.key !== "" ||
      row.value !== "" ||
      row.description !== "" ||
      !!row.files?.length,
  );
}
export function validParams(
  rows: RequestParam[],
  headers = false,
  multipart = false,
) {
  const filled = filledParams(rows);
  if (filled.length > 200) throw new Error("参数最多200项");
  const keys = new Set<string>();
  for (const row of filled) {
    if (
      ![...paramTypes, ...(multipart ? ["json", "file"] : [])].includes(
        row.paramType,
      )
    )
      throw new Error("参数类型无效");
    if (!multipart && ["json", "file"].includes(row.paramType))
      throw new Error("此参数表不支持文件或JSON类型");
    if (multipart && row.paramType === "json" && row.enable && row.value)
      JSON.parse(row.value);
    if (row.files?.length && row.paramType !== "file")
      throw new Error("只有文件参数可以关联文件");
    if ((row.files?.length || 0) > 20) throw new Error("每个参数最多20个文件");
    if (
      new Set((row.files || []).map((file) => file.fileId)).size !==
      (row.files?.length || 0)
    )
      throw new Error("同一参数不能重复选择相同文件");
    for (const file of row.files || [])
      if (
        !/^[a-zA-Z0-9_-]{1,36}$/.test(file.fileId) ||
        /[\x00\r\n/\\]/.test(file.fileAlias || "")
      )
        throw new Error("请求文件引用或别名无效");
    if (!row.key.trim() || row.key.length > 255 || row.value.length > 20000)
      throw new Error("请填写参数名称，名称最多255字符，值最多20000字符");
    if (row.enable) {
      const key = headers ? row.key.toLowerCase() : row.key;
      if (keys.has(key)) throw new Error("启用的参数名称不能重复");
      keys.add(key);
    }
    if (
      row.lengthRange.length &&
      (row.lengthRange.length !== 2 ||
        !row.lengthRange.every(Number.isInteger) ||
        row.lengthRange[0] < 0 ||
        row.lengthRange[1] < row.lengthRange[0])
    )
      throw new Error("请填写完整的非负参数长度范围");
  }
  return filled;
}
export function batchParams(raw: string, headers = false) {
  const rows = raw
    .split(/\r?\n/)
    .filter((line) => line.trim())
    .map((line) => {
      const colon = line.indexOf(":");
      if (colon < 1) throw new Error("批量参数每行使用名称:值格式");
      return {
        ...blankParam(),
        key: line.slice(0, colon).trim(),
        value: line.slice(colon + 1).trim(),
      };
    });
  return validParams(rows, headers);
}
export function paramCount(raw: string) {
  try {
    return readParams(raw).filter((row) => row.key && row.enable).length;
  } catch (exception) {
    console.error("请求参数徽标计算失败", exception);
    return 0;
  }
}
