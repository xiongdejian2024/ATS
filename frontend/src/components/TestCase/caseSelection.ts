import { computed, ref, watch, type Ref } from "vue";
import { cloneDeep } from "lodash-es";
import { caseGovernanceApi, type CaseSelection } from "@/api/caseGovernance";
import {
  pageExclusions,
  selectedPageIds,
} from "@/components/CaseReview/reviewSelection";

/** 只保留当前筛选范围和排除项，不从服务器拉取所有页ID。 */
export function useCaseSelection(
  project: Ref<string>,
  query: Ref<Record<string, unknown>>,
  selected: Ref<string[]>,
  pageIds: Ref<string[]>,
) {
  const selectAll = ref(false),
    excluded = ref<string[]>([]);
  const condition = ref<Record<string, unknown>>({});
  const loading = ref(false),
    error = ref(""),
    working = ref(false);
  const count = ref<number>(),
    permissions = ref<Record<string, boolean>>({});
  const hasSelection = computed(
    () => selectAll.value || selected.value.length > 0,
  );
  const request = computed<CaseSelection | undefined>(() =>
    !hasSelection.value
      ? undefined
      : selectAll.value
        ? {
            selectAll: true,
            excludeIds: [...excluded.value],
            condition: cloneDeep(condition.value),
          }
        : { caseIds: [...selected.value] },
  );
  const pageSelected = computed(() =>
    selectAll.value
      ? selectedPageIds(pageIds.value, excluded.value)
      : selected.value,
  );
  const ready = computed(
    () => !!count.value && !loading.value && !error.value && !working.value,
  );
  let sequence = 0;
  function clear() {
    ++sequence;
    selectAll.value = false;
    excluded.value = [];
    selected.value = [];
    count.value = undefined;
    error.value = "";
    permissions.value = {};
    loading.value = false;
  }
  function all() {
    if (working.value) return;
    condition.value = cloneDeep(query.value);
    selected.value = [];
    excluded.value = [];
    selectAll.value = true;
  }
  function current() {
    if (working.value) return;
    selectAll.value = false;
    excluded.value = [];
    selected.value = [...pageIds.value];
  }
  function keysChanged(keys: string[]) {
    if (working.value) return;
    if (selectAll.value)
      excluded.value = pageExclusions(excluded.value, pageIds.value, keys);
    else selected.value = keys;
  }
  async function preview() {
    const current = ++sequence,
      p = project.value,
      body = request.value;
    count.value = undefined;
    error.value = "";
    permissions.value = {};
    if (!p || !body) {
      loading.value = false;
      return;
    }
    loading.value = true;
    try {
      const result = await caseGovernanceApi.previewSelection(p, body);
      if (current !== sequence || p !== project.value) return;
      count.value = result.count;
      permissions.value = result.permissions;
    } catch (exception: any) {
      console.error("核对主用例选择范围失败，保留排除项", exception);
      if (current === sequence)
        error.value =
          exception.response?.data?.detail || "选择范围核对失败，请重试";
    } finally {
      if (current === sequence) loading.value = false;
    }
  }
  watch(() => JSON.stringify([project.value, query.value]), clear, {
    flush: "sync",
  });
  watch(
    () => JSON.stringify([project.value, request.value]),
    () => {
      void preview();
    },
  );
  return {
    selectAll,
    excluded,
    working,
    loading,
    error,
    count,
    permissions,
    ready,
    hasSelection,
    request,
    pageSelected,
    clear,
    all,
    current,
    keysChanged,
    preview,
  };
}

export function saveReviewSelection(
  projectId: string,
  selection: CaseSelection,
  storage = sessionStorage,
) {
  const key = `ats-case-selection:${crypto.randomUUID()}`;
  storage.setItem(key, JSON.stringify({ projectId, selection }));
  return key;
}

export function readReviewSelection(
  projectId: string,
  key: string,
  storage = sessionStorage,
): CaseSelection {
  if (!key.startsWith("ats-case-selection:"))
    throw new Error("评审范围标识无效");
  const raw = storage.getItem(key);
  if (!raw) throw new Error("评审选择范围已过期，请返回用例列表重新选择");
  const data = JSON.parse(raw);
  if (data.projectId !== projectId || !data.selection?.selectAll)
    throw new Error("评审选择范围不属于当前项目");
  return cloneDeep(data.selection);
}
