/** 表格显示偏好只保存字段编号、可见状态和数字列宽。 */
export interface DisplayColumn {
  key: string;
  title: string;
  required?: boolean;
  defaultVisible?: boolean;
}
export interface ColumnVisibility {
  key: string;
  visible: boolean;
  width?: number;
}
export interface TableDisplay {
  columns: ColumnVisibility[];
  pageSize: number;
  includeDescendants: boolean;
}
export const pageSizes = [10, 20, 30, 40, 50];
export const columnMinWidth = (key: string) => (key === "tags" ? 216 : 80);
function validWidth(width: unknown, key: string): number | undefined {
  return typeof width === "number" && Number.isFinite(width) && width > 0
    ? Math.max(columnMinWidth(key), width)
    : undefined;
}
export function resizableColumn<T extends { key: string; width: number }>(
  column: T,
  preference: ColumnVisibility,
) {
  return {
    ...column,
    width:
      validWidth(preference.width, column.key) ??
      Math.max(column.width, columnMinWidth(column.key)),
    minWidth: columnMinWidth(column.key),
    resizable: true,
  };
}
export function normalizeDisplay(
  value: unknown,
  definitions: DisplayColumn[],
): TableDisplay {
  const input =
    value && typeof value === "object" ? (value as Partial<TableDisplay>) : {};
  const known = new Map(definitions.map((column) => [column.key, column]));
  const stored = new Map<string, ColumnVisibility>();
  if (Array.isArray(input.columns))
    for (const item of input.columns) {
      if (
        item &&
        known.has(item.key) &&
        typeof item.visible === "boolean" &&
        !stored.has(item.key)
      )
        stored.set(item.key, {
          key: item.key,
          visible: item.visible,
          width: validWidth(item.width, item.key),
        });
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
        : (stored.get(key)?.visible ??
          known.get(key)?.defaultVisible !== false),
      ...(stored.get(key)?.width === undefined
        ? {}
        : { width: stored.get(key)!.width }),
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
