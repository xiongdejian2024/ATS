import type { CaseFolder } from "@/api/planCaseWorkspace";
export interface FolderNode extends CaseFolder {
  key: string;
  title: string;
  children?: FolderNode[];
}
export function caseFolderTree(rows: CaseFolder[], keyword = ""): FolderNode[] {
  const byId = new Map(rows.map((row) => [row.id, row])),
    visible = new Set<string>();
  for (const row of rows.filter((row) =>
    row.name.toLocaleLowerCase().includes(keyword.trim().toLocaleLowerCase()),
  )) {
    let current: CaseFolder | undefined = row;
    const seen = new Set<string>();
    while (current && !seen.has(current.id)) {
      visible.add(current.id);
      seen.add(current.id);
      current = current.parentId ? byId.get(current.parentId) : undefined;
    }
  }
  const filtered = rows.filter((row) => visible.has(row.id)),
    ids = new Set(filtered.map((row) => row.id)),
    seen = new Set<string>();
  const build = (row: CaseFolder): FolderNode => {
    seen.add(row.id);
    const children = filtered
      .filter((item) => item.parentId === row.id && !seen.has(item.id))
      .map(build);
    return {
      ...row,
      key: row.id,
      title: row.name,
      children: children.length ? children : undefined,
    };
  };
  const roots = filtered
    .filter((row) => !row.parentId || !ids.has(row.parentId))
    .map(build);
  for (const row of filtered) if (!seen.has(row.id)) roots.push(build(row));
  return roots;
}
