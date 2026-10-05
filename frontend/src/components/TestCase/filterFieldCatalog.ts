import type { CaseTemplate } from "@/api/caseFeatures";
import type { FilterField } from "./advancedFilter";

export function filterFieldCatalog(
  fields: any[],
  templates: CaseTemplate[],
  members: { id: string; name: string }[],
): FilterField[] {
  const memberOptions = [
    { label: "当前用户", value: "CURRENT_USER" },
    ...members.map((m) => ({ label: m.name, value: m.id })),
  ];
  const catalog: FilterField[] = fields.map((field) => ({
    key: field.fieldKey,
    label: field.fieldLabel,
    type: field.fieldType,
    operators: field.operators?.map(
      (op: string) =>
        ({
          greater_than: "gt",
          less_than: "lt",
          greater_equal: "gte",
          less_equal: "lte",
        })[op] || op,
    ),
    options: field.fieldType === "member" ? memberOptions : field.options,
  }));
  const custom = new Map(
    templates.flatMap((t) => t.fields.map((f) => [f.key, f] as const)),
  );
  for (const f of custom.values())
    catalog.push({
      key: `customFields.${f.key}`,
      label: `自定义 · ${f.name}`,
      type:
        f.type === "textarea"
          ? "text"
          : ["boolean", "multiselect"].includes(f.type)
            ? "select"
            : (f.type as FilterField["type"]),
      showTime: f.type === "date" ? false : undefined,
      options:
        f.type === "boolean"
          ? [
              { label: "是", value: true },
              { label: "否", value: false },
            ]
          : f.options.map((value) => ({ label: value, value })),
    });
  return catalog;
}
