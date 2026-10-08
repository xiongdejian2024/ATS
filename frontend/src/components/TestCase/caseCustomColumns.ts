import type { FilterField } from "./advancedFilter";
import type {
  DisplayColumn,
  TableDisplay,
  ColumnVisibility,
} from "@/components/Table/tableDisplay";
import dayjs from "dayjs";

const customPrefix = "customFields.";
const customKey = /^customFields\.[A-Za-z][A-Za-z0-9_]*$/;

/** 自定义列沿用已授权加载的模板字段目录，未加载字段不当作可排序字段。 */
export function caseCustomColumns(fields: FilterField[]) {
  const unique = new Map(
    fields.filter((f) => customKey.test(f.key)).map((f) => [f.key, f]),
  );
  return [...unique.values()].map((field) => ({
    key: field.key,
    title: field.label,
    dataIndex: ["customFields", field.key.slice(customPrefix.length)],
    width: 180,
    ellipsis: true,
    defaultVisible: false,
    sorter: false,
    filters: undefined,
    fieldType: field.type,
  }));
}

export function caseCustomValue(
  value: unknown,
  type?: FilterField["type"],
): string {
  if (value === undefined || value === null || value === "") return "-";
  if (typeof value === "boolean") return value ? "是" : "否";
  if (Array.isArray(value))
    return value.length ? value.map((v) => String(v)).join("、") : "-";
  if (type === "date" && typeof value === "string" && dayjs(value).isValid())
    return dayjs(value).format("YYYY-MM-DD");
  return typeof value === "string" || typeof value === "number"
    ? String(value)
    : "-";
}

/** 保存当前列时保留尚未加载/暂时不可用的自定义列偏好；只存编号、宽度和可见性。 */
export function retainUnavailableCaseColumns(
  next: TableDisplay,
  previous: unknown,
  definitions: DisplayColumn[],
  submitted: ColumnVisibility[] = next.columns,
): TableDisplay {
  const known = new Set(definitions.map((d) => d.key));
  const retained = new Map<
    string,
    { key: string; visible: boolean; width?: number }
  >();
  const columns =
    previous && typeof previous === "object"
      ? (previous as { columns?: unknown }).columns
      : undefined;
  for (const column of [
    ...(Array.isArray(columns) ? columns : []),
    ...submitted,
  ]) {
    if (
      !column ||
      typeof column.key !== "string" ||
      !customKey.test(column.key) ||
      known.has(column.key) ||
      typeof column.visible !== "boolean"
    )
      continue;
    retained.set(column.key, {
      key: column.key,
      visible: column.visible,
      ...(typeof column.width === "number" &&
      Number.isFinite(column.width) &&
      column.width > 0
        ? { width: Math.max(80, column.width) }
        : {}),
    });
  }
  const combined = new Map(
    [...next.columns, ...retained.values()].map((c) => [c.key, c]),
  );
  const validOrder = (items: any[]) => [
    ...new Set(items.map((c) => c?.key).filter((key) => combined.has(key))),
  ];
  const previousOrder = validOrder(Array.isArray(columns) ? columns : []),
    submittedOrder = validOrder(submitted);
  const unknownSubmitted = submittedOrder.some((key) => !known.has(key));
  const remaining = [...submittedOrder];
  const order = unknownSubmitted
    ? submittedOrder
    : previousOrder
        .map((key) => (known.has(key) ? remaining.shift()! : key))
        .filter(Boolean);
  const ordered = [
    ...new Set([...order, ...remaining, ...previousOrder, ...combined.keys()]),
  ];
  const required = definitions.filter((d) => d.required).map((d) => d.key);
  return {
    ...next,
    columns: [...required, ...ordered.filter((key) => !required.includes(key))]
      .filter((key) => combined.has(key))
      .map((key) => combined.get(key)!),
  };
}
