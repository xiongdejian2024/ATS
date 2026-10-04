/** 跨页保留完整用例对象，删除取消的选择；未知键不生成虚构用例。 */
export function mergeCaseSelection<T extends { id: string }>(
  previous: Map<string, T>,
  keys: (string | number)[],
  page: T[],
): Map<string, T> {
  const selectedIds = new Set(keys.map(String));
  const selected = new Map(
    Array.from(previous).filter(([id]) => selectedIds.has(id)),
  );
  for (const row of page)
    if (selectedIds.has(row.id)) selected.set(row.id, row);
  return selected;
}
