/** 跨页全选时只记录排除项，当前页操作保留其他页排除项。 */
export function pageExclusions(
  excluded: string[],
  pageIds: string[],
  selectedKeys: string[],
) {
  const values = new Set(excluded),
    selected = new Set(selectedKeys);
  for (const id of pageIds) {
    if (selected.has(id)) values.delete(id);
    else values.add(id);
  }
  return [...values];
}
export function selectedPageIds(pageIds: string[], excluded: string[]) {
  const values = new Set(excluded);
  return pageIds.filter((id) => !values.has(id));
}
