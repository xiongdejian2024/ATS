/** 表格显示偏好只保存字段编号和布尔值，不存放组件或可执行内容。 */
export interface DisplayColumn {
  key: string;
  title: string;
  required?: boolean;
  defaultVisible?: boolean;
}
export interface ColumnVisibility {
  key: string;
  visible: boolean;
}
export interface TableDisplay {
  columns: ColumnVisibility[];
  pageSize: number;
  includeDescendants: boolean;
}
export const pageSizes = [10, 20, 30, 40, 50];
export function normalizeDisplay(
  value: unknown,
  definitions: DisplayColumn[],
): TableDisplay {
  const input =
    value && typeof value === "object" ? (value as Partial<TableDisplay>) : {};
  const known = new Map(definitions.map((column) => [column.key, column]));
  const stored = new Map<string, boolean>();
  if (Array.isArray(input.columns))
    for (const item of input.columns) {
      if (
        item &&
        known.has(item.key) &&
        typeof item.visible === "boolean" &&
        !stored.has(item.key)
      )
        stored.set(item.key, item.visible);
    }
  const locked = definitions.filter((column) => column.required);
  const movable = [...stored.keys()].filter((key) => !known.get(key)?.required);
  for (const column of definitions)
    if (!column.required && !movable.includes(column.key))
      movable.push(column.key);
  return {
    columns: [...locked.map((column) => column.key), ...movable].map((key) => ({
      key,
      visible: known.get(key)?.required
        ? true
        : (stored.get(key) ?? known.get(key)?.defaultVisible !== false),
    })),
    pageSize: pageSizes.includes(input.pageSize as number)
      ? input.pageSize!
      : 20,
    includeDescendants:
      typeof input.includeDescendants === "boolean"
        ? input.includeDescendants
        : true,
  };
}
export function displayStorageKey(
  userId: string,
  projectId: string,
  table: string,
) {
  return `ats:table-display:${encodeURIComponent(userId)}:${encodeURIComponent(projectId)}:${table}`;
}
export function readDisplay(
  storage: Pick<Storage, "getItem">,
  key: string,
  definitions: DisplayColumn[],
): TableDisplay {
  try {
    const raw = storage.getItem(key);
    return normalizeDisplay(raw ? JSON.parse(raw) : undefined, definitions);
  } catch (error) {
    console.error("读取表格显示配置失败，使用默认显示", error);
    return normalizeDisplay(undefined, definitions);
  }
}
