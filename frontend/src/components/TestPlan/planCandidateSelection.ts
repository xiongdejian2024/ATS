import { computed, ref, watch, type Ref } from "vue";
import { cloneDeep } from "lodash-es";
import {
  planCaseWorkspaceApi,
  type CandidateCondition,
  type CandidateSelection,
  type CandidateSelectionPreview,
} from "@/api/planCaseWorkspace";
import {
  pageExclusions,
  selectedPageIds,
} from "@/components/CaseReview/reviewSelection";

/** 范围全选只传筛选条件与排除项，预览失败时保留当前选择。 */
export function usePlanCandidateSelection(
  plan: Ref<string>,
  category: Ref<CandidateSelection["category"]>,
  query: Ref<CandidateCondition>,
  pageIds: Ref<string[]>,
) {
  const selected = ref<string[]>([]),
    selectAll = ref(false),
    excluded = ref<string[]>([]),
    condition = ref<CandidateCondition>({}),
    loading = ref(false),
    working = ref(false),
    error = ref(""),
    summary = ref<CandidateSelectionPreview>();
  let sequence = 0;
  const hasSelection = computed(
    () => selectAll.value || selected.value.length > 0,
  );
  const request = computed<CandidateSelection | undefined>(() =>
    !hasSelection.value
      ? undefined
      : {
          category: category.value,
          ...(selectAll.value
            ? {
                selectAll: true,
                excludeIds: [...excluded.value],
                condition: cloneDeep(condition.value),
              }
            : { caseIds: [...selected.value] }),
        },
  );
  const pageSelected = computed(() =>
    selectAll.value
      ? selectedPageIds(pageIds.value, excluded.value)
      : selected.value,
  );
  const ready = computed(
    () =>
      !!summary.value?.count &&
      summary.value.canAssociate &&
      !loading.value &&
      !error.value &&
      !working.value,
  );
  function clear() {
    ++sequence;
    selected.value = [];
    excluded.value = [];
    selectAll.value = false;
    summary.value = undefined;
    error.value = "";
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
    selected.value = selectAll.value
      ? [...pageIds.value]
      : [...new Set([...selected.value, ...pageIds.value])];
    selectAll.value = false;
    excluded.value = [];
  }
  function keysChanged(keys: string[]) {
    if (working.value) return;
    if (selectAll.value)
      excluded.value = pageExclusions(excluded.value, pageIds.value, keys);
    else selected.value = [...keys];
  }
  function togglePage() {
    const currentKeys = new Set(pageSelected.value);
    const allChecked =
      pageIds.value.length > 0 &&
      pageIds.value.every((id) => currentKeys.has(id));
    if (allChecked) pageIds.value.forEach((id) => currentKeys.delete(id));
    else pageIds.value.forEach((id) => currentKeys.add(id));
    keysChanged([...currentKeys]);
  }
  async function preview() {
    const current = ++sequence,
      id = plan.value,
      body = request.value;
    summary.value = undefined;
    error.value = "";
    if (!id || !body) {
      loading.value = false;
      return;
    }
    loading.value = true;
    try {
      const result = await planCaseWorkspaceApi.previewCandidates(id, body);
      if (current === sequence && id === plan.value) summary.value = result;
    } catch (exception: any) {
      console.error("核对计划关联范围失败，保留筛选条件与排除项", exception);
      if (current === sequence)
        error.value =
          exception.response?.data?.detail || "选择范围核对失败，请重试";
    } finally {
      if (current === sequence) loading.value = false;
    }
  }
  watch(() => JSON.stringify([plan.value, category.value]), clear, {
    flush: "sync",
  });
  watch(
    () => JSON.stringify(query.value),
    () => {
      if (selectAll.value) clear();
    },
    { flush: "sync" },
  );
  watch(
    () => JSON.stringify(request.value),
    () => {
      void preview();
    },
  );
  return {
    selected,
    selectAll,
    excluded,
    loading,
    working,
    error,
    summary,
    hasSelection,
    request,
    pageSelected,
    ready,
    clear,
    all,
    current,
    keysChanged,
    togglePage,
    preview,
  };
}
