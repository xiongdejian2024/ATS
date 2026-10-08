export const reportCards = [
  { key: "overview", title: "执行概况", required: true },
  { key: "analysis", title: "执行分析" },
  { key: "testSets", title: "测试集分析" },
  { key: "defects", title: "缺陷分析" },
  { key: "configuration", title: "冻结执行配置" },
];
export interface ReportCardPreference {
  key: string;
  visible: boolean;
}
export function normalizeReportCards(value: unknown): ReportCardPreference[] {
  const known = new Set(reportCards.map((c) => c.key)),
    stored = new Map<string, ReportCardPreference>();
  if (Array.isArray(value))
    for (const row of value) {
      if (
        row &&
        typeof row === "object" &&
        known.has(row.key) &&
        typeof row.visible === "boolean" &&
        !stored.has(row.key)
      )
        stored.set(row.key, { key: row.key, visible: row.visible });
    }
  stored.delete("overview");
  return [
    { key: "overview", visible: true },
    ...stored.values(),
    ...reportCards
      .filter((c) => c.key !== "overview" && !stored.has(c.key))
      .map((c) => ({ key: c.key, visible: true })),
  ];
}
export function reportCardsKey(
  actor: string,
  project: string,
  kind: "PLAN" | "GROUP",
) {
  return `ats:report-cards:${encodeURIComponent(actor)}:${encodeURIComponent(project)}:${kind}`;
}
export function readReportCards(
  storage: Pick<Storage, "getItem">,
  key: string,
) {
  try {
    const value = storage.getItem(key);
    return normalizeReportCards(value ? JSON.parse(value) : undefined);
  } catch (error) {
    console.error("读取报告卡片配置失败", error);
    return normalizeReportCards(undefined);
  }
}
