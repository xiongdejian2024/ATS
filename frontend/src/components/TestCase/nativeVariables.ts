export interface NativeVariable {
  name: string;
  value: string;
  enable: boolean;
  description: string;
}
export function readNativeVariables(raw: string): NativeVariable[] {
  const data: unknown = JSON.parse(raw);
  if (!Array.isArray(data) || data.length > 100)
    throw new Error("变量最多100项");
  const names = new Set<string>();
  const rows = data.map((item) => {
    if (
      !item ||
      typeof item !== "object" ||
      Array.isArray(item) ||
      Object.keys(item).some(
        (k) => !["name", "value", "enable", "description"].includes(k),
      )
    )
      throw new Error("变量配置无效");
    const row = {
      name: item.name,
      value: item.value ?? "",
      enable: item.enable ?? true,
      description: item.description ?? "",
    };
    if (
      typeof row.name !== "string" ||
      !row.name.trim() ||
      row.name.length > 255 ||
      /[${}\r\n\0]/.test(row.name) ||
      names.has(row.name) ||
      typeof row.value !== "string" ||
      row.value.length > 20000 ||
      typeof row.enable !== "boolean" ||
      typeof row.description !== "string" ||
      row.description.length > 1000
    )
      throw new Error("变量名称不能重复，名称、值或说明超过限制");
    names.add(row.name);
    return row;
  });
  if (new TextEncoder().encode(JSON.stringify(rows)).length > 65536)
    throw new Error("变量声明总量不能超过64KiB");
  return rows;
}
