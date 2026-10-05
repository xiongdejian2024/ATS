import { computed, ref, watch, onScopeDispose, type Ref } from "vue";
import { cloneDeep } from "lodash-es";
import {
  planCaseWorkspaceApi,
  type NativeWorkspaceCondition,
  type NativeWorkspaceSelection,
  type NativeWorkspacePreview,
} from "@/api/planCaseWorkspace";
import {
  pageExclusions,
  selectedPageIds,
} from "@/components/CaseReview/reviewSelection";

/** 用关联实例身份保留跨页选择，全范围只提交条件及排除项。 */
export function usePlanNativeSelection(
  plan: Ref<string>,
  category: Ref<"api" | "scenario">,
  query: Ref<NativeWorkspaceCondition>,
  pageIds: Ref<string[]>,
) {
  const selected = ref<string[]>([]),
    selectAll = ref(false),
    excluded = ref<string[]>([]),
    condition = ref<NativeWorkspaceCondition>({}),
    loading = ref(false),
    working = ref(false),
    error = ref(""),
    summary = ref<NativeWorkspacePreview>();
  let sequence = 0;
  const hasSelection = computed(
    () => selectAll.value || selected.value.length > 0,
  );
  const request = computed<NativeWorkspaceSelection | undefined>(() =>
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
            : { selectIds: [...selected.value] }),
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
      summary.value.canModify &&
      !loading.value &&
      !error.value &&
      !working.value,
  );
  const executeReady = computed(
    () =>
      !!summary.value?.count &&
      !!summary.value.canExecute &&
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
  function keysChanged(keys: (string | number)[]) {
    if (working.value) return;
    const values = keys.map(String);
    if (selectAll.value)
      excluded.value = pageExclusions(excluded.value, pageIds.value, values);
    else {
      // Ant 表格只需提交当前页变化，其他页的显式选择保持不变。
      const current = new Set(pageIds.value);
      selected.value = [
        ...new Set([
          ...selected.value.filter((id) => !current.has(id)),
          ...values.filter((id) => current.has(id)),
        ]),
      ];
    }
  }
  function togglePage() {
    const keys = new Set(pageSelected.value);
    const checked =
      pageIds.value.length > 0 && pageIds.value.every((id) => keys.has(id));
    for (const id of pageIds.value) checked ? keys.delete(id) : keys.add(id);
    keysChanged([...keys]);
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
      const result = await planCaseWorkspaceApi.previewNativeSelection(
        id,
        body,
      );
      if (current === sequence) summary.value = result;
    } catch (exception: any) {
      console.error("核对原生计划选择范围失败，保留选择及排除项", exception);
      if (current === sequence)
        error.value =
          typeof exception.response?.data?.detail === "string"
            ? exception.response.data.detail
            : "选择范围核对失败，请重试";
    } finally {
      if (current === sequence) loading.value = false;
    }
  }
  watch(
    () => JSON.stringify([plan.value, category.value, query.value]),
    clear,
    { flush: "sync" },
  );
  watch(
    () => JSON.stringify(request.value),
    () => void preview(),
  );
  onScopeDispose(() => {
    ++sequence;
  });
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
    executeReady,
    clear,
    all,
    current,
    keysChanged,
    togglePage,
    preview,
  };
}
