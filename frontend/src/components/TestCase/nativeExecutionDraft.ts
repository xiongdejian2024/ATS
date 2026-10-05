import { ref, watch } from "vue";
export interface ExecutionEditorProps {
  modelValue: string;
  category: string;
  apiCases: { id: string; name: string }[];
  disabled?: boolean;
}
export function useNativeExecutionDraft(
  props: ExecutionEditorProps,
  events: {
    update(value: string): void;
    error(value: string): void;
    draft(value: string): void;
  },
) {
  const enabled = ref(false),
    method = ref("GET"),
    timeout = ref<number | null>(10000),
    redirects = ref(false),
    stop = ref(true);
  const query = ref("{}"),
    headers = ref("{}"),
    bodyType = ref("none"),
    body = ref("null"),
    assertions = ref("[]"),
    error = ref("");
  const steps = ref<{ apiCaseId: string; enabled: boolean }[]>([]);
  const methods = [
    "GET",
    "POST",
    "PUT",
    "PATCH",
    "DELETE",
    "HEAD",
    "OPTIONS",
  ].map((value) => ({ value, label: value }));
  const bodyTypes = ["none", "json", "text", "form"].map((value) => ({
    value,
    label: value === "none" ? "无请求体" : value,
  }));
  let adopting = false,
    output = "";
  function object(raw: string): Record<string, any> {
    const result = JSON.parse(raw);
    if (!result || typeof result !== "object" || Array.isArray(result))
      throw new Error("配置须为JSON对象");
    return result;
  }
  watch(
    () => props.modelValue,
    (value) => {
      if (value === output) return;
      adopting = true;
      try {
        const root = object(value),
          data = root[props.category === "api" ? "request" : "scenario"];
        enabled.value = !!data;
        method.value = data?.method ?? "GET";
        timeout.value = data?.timeoutMs ?? 10000;
        redirects.value = data?.followRedirects ?? false;
        query.value = JSON.stringify(data?.query ?? {}, null, 2);
        headers.value = JSON.stringify(data?.headers ?? {}, null, 2);
        bodyType.value = data?.bodyType ?? "none";
        body.value =
          bodyType.value === "text"
            ? (data?.body ?? "")
            : JSON.stringify(data?.body ?? null, null, 2);
        assertions.value = JSON.stringify(data?.assertions ?? [], null, 2);
        stop.value = data?.stopOnFailure ?? true;
        steps.value = structuredClone(data?.steps ?? []);
        error.value = "";
        events.error("");
        events.draft("");
      } catch (failure) {
        console.error("加载原生执行编辑配置失败", failure);
        error.value = "配置JSON无效，请修正请求参数后重试";
        events.error(error.value);
      } finally {
        adopting = false;
      }
    },
    { immediate: true, flush: "sync" },
  );
  function publish() {
    if (adopting) return;
    events.draft(
      JSON.stringify([
        enabled.value,
        method.value,
        timeout.value,
        redirects.value,
        query.value,
        headers.value,
        bodyType.value,
        body.value,
        assertions.value,
        stop.value,
        steps.value,
      ]),
    );
    try {
      const root = object(props.modelValue),
        key = props.category === "api" ? "request" : "scenario";
      if (!enabled.value) delete root[key];
      else if (props.category === "api")
        root.request = {
          method: method.value,
          timeoutMs: timeout.value,
          followRedirects: redirects.value,
          query: object(query.value),
          headers: object(headers.value),
          bodyType: bodyType.value,
          body:
            bodyType.value === "none"
              ? null
              : bodyType.value === "text"
                ? body.value
                : JSON.parse(body.value),
          assertions: JSON.parse(assertions.value),
        };
      else {
        if (
          !steps.value.length ||
          steps.value.some((s) => !s.apiCaseId) ||
          !steps.value.some((s) => s.enabled)
        )
          throw new Error("场景须选择并启用至少一个API步骤");
        root.scenario = { steps: steps.value, stopOnFailure: stop.value };
      }
      output = JSON.stringify(root, null, 2);
      events.update(output);
      error.value = "";
      events.error("");
    } catch (failure) {
      console.error("原生执行编辑配置校验失败，保留草稿", failure);
      error.value = "请检查参数JSON、请求体、断言及启用的场景步骤";
      events.error(error.value);
    }
  }
  watch(
    [
      enabled,
      method,
      timeout,
      redirects,
      query,
      headers,
      bodyType,
      body,
      assertions,
      stop,
      steps,
    ],
    publish,
    { deep: true, flush: "sync" },
  );
  function toggle(value: boolean | string | number) {
    enabled.value = value === true;
  }
  function move(index: number, direction: number) {
    const [step] = steps.value.splice(index, 1);
    steps.value.splice(index + direction, 0, step);
  }

  return {
    enabled,
    method,
    timeout,
    redirects,
    stop,
    query,
    headers,
    bodyType,
    body,
    assertions,
    error,
    steps,
    methods,
    bodyTypes,
    toggle,
    move,
  };
}
