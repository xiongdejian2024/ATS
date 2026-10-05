import { computed, ref, type Ref } from "vue";
import type {
  CaseFolder,
  CandidateModuleSelection,
  CandidateSelectionPreview,
} from "@/api/planCaseWorkspace";
import { cloneDeep } from "lodash-es";

export interface CandidateModulesContext {
  enabled: Ref<boolean>;
  modules: Ref<CaseFolder[]>;
  rows: Ref<{ id: string; moduleId?: string | null }[]>;
}
/** 模块ID表示精确归属；点击父节点时按完整目录展开，不受模块搜索影响。 */
export function moduleDescendants(
  modules: CaseFolder[],
  root: string,
): string[] {
  if (root === "all") return ["unassigned", ...modules.map((row) => row.id)];
  const found = new Set([root]);
  let size = 0;
  while (size !== found.size) {
    size = found.size;
    modules.forEach((row) => {
      if (row.parentId && found.has(row.parentId)) found.add(row.id);
    });
  }
  return [...found];
}
export function useCandidateModules(
  context: CandidateModulesContext,
  summary: Ref<CandidateSelectionPreview | undefined>,
) {
  const maps = ref<Record<string, CandidateModuleSelection>>({});
  const hasSelection = computed(() =>
    Object.values(maps.value).some(
      (entry) => entry.selectAll || entry.selectIds.length > 0,
    ),
  );
  const entryFor = (key: string) => maps.value[key] || maps.value.all;
  function keyFor(row: { moduleId?: string | null }) {
    return context.modules.value.some((module) => module.id === row.moduleId)
      ? row.moduleId!
      : "unassigned";
  }
  const pageSelected = computed(() =>
    context.rows.value
      .filter((row) => {
        const entry = entryFor(keyFor(row));
        return entry?.selectAll
          ? !entry.excludeIds.includes(row.id)
          : entry?.selectIds.includes(row.id);
      })
      .map((row) => row.id),
  );
  function check(key: string, checked: boolean) {
    if (key === "all") {
      maps.value = checked
        ? { all: { selectAll: true, selectIds: [], excludeIds: [] } }
        : {};
      return;
    }
    const next = cloneDeep(maps.value);
    for (const id of moduleDescendants(context.modules.value, key)) {
      if (checked || next.all)
        next[id] = { selectAll: checked, selectIds: [], excludeIds: [] };
      else delete next[id];
    }
    maps.value = next;
  }
  function keysChanged(keys: string[]) {
    const selected = new Set(keys),
      next = cloneDeep(maps.value);
    for (const row of context.rows.value) {
      const key = keyFor(row),
        entry = (next[key] ||= cloneDeep(
          next.all || { selectAll: false, selectIds: [], excludeIds: [] },
        ));
      if (entry.selectAll)
        entry.excludeIds = selected.has(row.id)
          ? entry.excludeIds.filter((id) => id !== row.id)
          : [...new Set([...entry.excludeIds, row.id])];
      else
        entry.selectIds = selected.has(row.id)
          ? [...new Set([...entry.selectIds, row.id])]
          : entry.selectIds.filter((id) => id !== row.id);
      if (!entry.selectAll && !entry.selectIds.length && !next.all)
        delete next[key];
    }
    maps.value = next;
  }
  function current() {
    // 当前页加入选择；其他页的已选项和排除项保持，符合模块表格联动契约。
    keysChanged(context.rows.value.map((row) => row.id));
  }
  function counts(key: string) {
    const values = moduleDescendants(context.modules.value, key).map(
      (id) => summary.value?.moduleCounts?.[id],
    );
    return {
      total: values.reduce((n, value) => n + (value?.total || 0), 0),
      selected: values.reduce((n, value) => n + (value?.selected || 0), 0),
    };
  }
  function checked(key: string) {
    const value = counts(key);
    if (value.total) return value.selected === value.total;
    return moduleDescendants(context.modules.value, key).every(
      (id) => entryFor(id)?.selectAll && !entryFor(id)?.excludeIds.length,
    );
  }
  function halfChecked(key: string) {
    const value = counts(key);
    return value.selected > 0 && value.selected < value.total;
  }
  const treeChecked = computed(() => ({
    checked: context.modules.value
      .filter((row) => checked(row.id))
      .map((row) => row.id),
    halfChecked: context.modules.value
      .filter((row) => halfChecked(row.id))
      .map((row) => row.id),
  }));
  return {
    maps,
    hasSelection,
    pageSelected,
    check,
    current,
    keysChanged,
    checked,
    halfChecked,
    treeChecked,
    counts,
  };
}
