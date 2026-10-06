import {
  useCandidateModules,
  type CandidateModulesContext,
} from "./planCandidateModules";
import { computed, ref, watch, type Ref } from "vue";
import { basicCondition } from "./planCandidateBasic";
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
  moduleContext?: CandidateModulesContext,
  project?: Ref<string | undefined>,
  extras?: Ref<
    Pick<
      CandidateSelection,
      | "syncCase"
      | "apiCaseCollectionId"
      | "apiScenarioCollectionId"
      | "resourceType"
    >
  >,
  previewRequest?: (
    id: string,
    selection: CandidateSelection,
  ) => Promise<CandidateSelectionPreview>,
) {
  const selected = ref<string[]>([]),
    selectAll = ref(false),
    excluded = ref<string[]>([]),
    condition = ref<CandidateCondition>({}),
    loading = ref(false),
    working = ref(false),
    error = ref(""),
    summary = ref<CandidateSelectionPreview>();
  const modules = moduleContext
    ? useCandidateModules(moduleContext, summary)
    : undefined;
  const moduleMode = computed(() => !!moduleContext?.enabled.value);
  let sequence = 0;
  const hasSelection = computed(() =>
    moduleMode.value
      ? !!modules?.hasSelection.value
      : selectAll.value || selected.value.length > 0,
  );
  const request = computed<CandidateSelection | undefined>(() =>
    !hasSelection.value
      ? undefined
      : {
          category: category.value,
          ...(project?.value ? { projectId: project.value } : {}),
          ...extras?.value,
          ...(moduleMode.value && modules
            ? {
                moduleMaps: cloneDeep(modules.maps.value),
                condition: {
                  ...basicCondition(query.value),
                  search: query.value.search,
                  priority: query.value.priority,
                  folder: "all",
                },
              }
            : selectAll.value
              ? {
                  selectAll: true,
                  excludeIds: [...excluded.value],
                  condition: cloneDeep(condition.value),
                }
              : extras?.value.resourceType === "API"
                ? {
                    definitionIds: [...selected.value],
                    ...(Object.keys(basicCondition(query.value)).length
                      ? { condition: basicCondition(query.value) }
                      : {}),
                  }
                : {
                    caseIds: [...selected.value],
                    ...(Object.keys(basicCondition(query.value)).length
                      ? { condition: basicCondition(query.value) }
                      : {}),
                  }),
        },
  );
  const pageSelected = computed(() =>
    moduleMode.value && modules
      ? modules.pageSelected.value
      : selectAll.value
        ? selectedPageIds(pageIds.value, excluded.value)
        : selected.value,
  );
  const ready = computed(
    () =>
      !!(summary.value?.selectedDefinitionCount ?? summary.value?.count) &&
      summary.value.canAssociate &&
      !loading.value &&
      !error.value &&
      !working.value,
  );
  function clear() {
    ++sequence;
    if (modules) modules.maps.value = {};
    selected.value = [];
    excluded.value = [];
    selectAll.value = false;
    summary.value = undefined;
    error.value = "";
    loading.value = false;
  }
  function all() {
    if (working.value) return;
    if (moduleMode.value && modules) {
      modules.check(query.value.folder || "all", true);
      return;
    }
    condition.value = cloneDeep(query.value);
    selected.value = [];
    excluded.value = [];
    selectAll.value = true;
  }
  function current() {
    if (working.value) return;
    if (moduleMode.value && modules) {
      modules.current();
      return;
    }
    selected.value = selectAll.value
      ? [...pageIds.value]
      : [...new Set([...selected.value, ...pageIds.value])];
    selectAll.value = false;
    excluded.value = [];
  }
  function keysChanged(keys: string[]) {
    if (working.value) return;
    if (moduleMode.value && modules) {
      modules.keysChanged(keys);
      return;
    }
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
  function restore(body: CandidateSelection) {
    clear();
    if (body.moduleMaps && modules)
      modules.maps.value = cloneDeep(body.moduleMaps);
    else {
      selected.value = [
        ...(body.resourceType === "API"
          ? body.definitionIds || []
          : body.caseIds || []),
      ];
      selectAll.value = !!body.selectAll;
      excluded.value = [...(body.excludeIds || [])];
      condition.value = cloneDeep(body.condition || {});
    }
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
      const result = await (
        previewRequest || planCaseWorkspaceApi.previewCandidates
      )(id, body);
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
  watch(
    () =>
      JSON.stringify([
        plan.value,
        category.value,
        project?.value,
        extras?.value.resourceType,
      ]),
    clear,
    {
      flush: "sync",
    },
  );
  watch(
    () =>
      JSON.stringify(
        moduleMode.value
          ? {
              search: query.value.search,
              priority: query.value.priority,
              protocols: query.value.protocols,
              methods: query.value.methods,
              createdBy: query.value.createdBy,
              filters: query.value.filters,
              mine: query.value.mine,
            }
          : query.value,
      ),
    () => {
      if (moduleMode.value || selectAll.value) clear();
    },
    { flush: "sync" },
  );
  watch(moduleMode, clear, { flush: "sync" });
  watch(() => JSON.stringify(basicCondition(query.value)), clear, {
    flush: "sync",
  });
  watch(
    () => JSON.stringify(request.value),
    () => {
      void preview();
    },
  );
  return {
    modules,
    moduleMode,
    scopeAll: computed(() =>
      moduleMode.value && modules
        ? modules.checked(query.value.folder || "all")
        : selectAll.value,
    ),
    checkModule: (key: string, checked: boolean) => {
      if (!working.value && modules) modules.check(key, checked);
    },
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
    restore,
  };
}
