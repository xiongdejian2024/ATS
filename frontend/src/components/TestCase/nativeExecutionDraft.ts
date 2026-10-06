import { ref, watch } from "vue";
import { readParams, validParams } from "./nativeRequestParams";
import { readResponseAssertions } from "./nativeResponseAssertions";
import { requestMethods } from "@/components/TestPlan/planCandidateBasic";
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
    responseAssertions = ref("[]"),
    error = ref("");
  const steps = ref<{ apiCaseId: string; enabled: boolean }[]>([]);
  const rest = ref("[]"),
    authType = ref("NONE"),
    basicUser = ref(""),
    basicPassword = ref(""),
    digestUser = ref(""),
    digestPassword = ref("");
  const connectTimeout = ref<number | null>(),
    responseTimeout = ref<number | null>();
  const methods = requestMethods.map((value) => ({ value, label: value }));
  const bodyTypes = ["none", "json", "text", "form"].map((value) => ({
    value,
    label: (
      {
        none: "none",
        json: "json",
        text: "raw",
        form: "x-www-form-urlencoded",
      } as Record<string, string>
    )[value],
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
        query.value = JSON.stringify(
          data?.queryParams ?? data?.query ?? {},
          null,
          2,
        );
        headers.value = JSON.stringify(
          data?.headerParams ?? data?.headers ?? {},
          null,
          2,
        );
        rest.value = JSON.stringify(data?.restParams ?? []);
        authType.value = data?.authConfig?.authType || "NONE";
        basicUser.value = data?.authConfig?.basicAuth?.userName || "";
        basicPassword.value = data?.authConfig?.basicAuth?.password || "";
        digestUser.value = data?.authConfig?.digestAuth?.userName || "";
        digestPassword.value = data?.authConfig?.digestAuth?.password || "";
        connectTimeout.value = data?.connectTimeoutMs;
        responseTimeout.value = data?.responseTimeoutMs;
        bodyType.value = data?.bodyType ?? "none";
        body.value =
          bodyType.value === "text"
            ? (data?.body ?? "")
            : JSON.stringify(data?.formParams ?? data?.body ?? null, null, 2);
        assertions.value = JSON.stringify(data?.assertions ?? [], null, 2);
        responseAssertions.value = JSON.stringify(
          data?.responseAssertions ?? [],
        );
        readResponseAssertions(responseAssertions.value);
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
        responseAssertions.value,
        stop.value,
        steps.value,
        rest.value,
        authType.value,
        basicUser.value,
        basicPassword.value,
        digestUser.value,
        digestPassword.value,
        connectTimeout.value,
        responseTimeout.value,
      ]),
    );
    try {
      const root = object(props.modelValue),
        key = props.category === "api" ? "request" : "scenario";
      if (!enabled.value) delete root[key];
      else if (props.category === "api") {
        const pairs = (raw: string, headers = false) => {
          const data = JSON.parse(raw);
          if (Array.isArray(data))
            return { value: {}, rows: validParams(readParams(raw), headers) };
          const value = object(raw);
          readParams(raw);
          return { value, rows: undefined };
        };
        const q = pairs(query.value),
          h = pairs(headers.value, true);
        const form = bodyType.value === "form" ? pairs(body.value) : undefined;
        const restRows = validParams(readParams(rest.value));
        root.request = {
          ...(root.request || {}),
          method: method.value,
          timeoutMs: timeout.value,
          followRedirects: redirects.value,
          query: q.value,
          headers: h.value,
          bodyType: bodyType.value,
          body:
            bodyType.value === "none"
              ? null
              : form
                ? form.value
                : bodyType.value === "text"
                  ? body.value
                  : JSON.parse(body.value),
          assertions: JSON.parse(assertions.value),
          responseAssertions: readResponseAssertions(responseAssertions.value),
        };
        for (const [key, rows] of [
          ["queryParams", q.rows],
          ["headerParams", h.rows],
          ["formParams", form?.rows],
        ] as const) {
          if (rows === undefined) delete root.request[key];
          else root.request[key] = rows;
        }
        if (restRows.length) root.request.restParams = restRows;
        else delete root.request.restParams;
        if (authType.value !== "NONE" || root.request.authConfig)
          root.request.authConfig = {
            authType: authType.value,
            basicAuth: {
              userName: basicUser.value,
              password: basicPassword.value,
            },
            digestAuth: {
              userName: digestUser.value,
              password: digestPassword.value,
            },
          };
        for (const [key, value] of [
          ["connectTimeoutMs", connectTimeout.value],
          ["responseTimeoutMs", responseTimeout.value],
        ] as const) {
          if (value === undefined || value === null) delete root.request[key];
          else if (!Number.isInteger(value) || value < 0 || value > 600000)
            throw new Error("超时须为0到600000毫秒的整数");
          else root.request[key] = value;
        }
      } else {
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
      responseAssertions,
      stop,
      steps,
      rest,
      authType,
      basicUser,
      basicPassword,
      digestUser,
      digestPassword,
      connectTimeout,
      responseTimeout,
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
  function changeBodyType(value: string) {
    if (value === "form") {
      try {
        readParams(body.value);
      } catch (exception) {
        console.info("切换表单正文，原内容不能转换为键值表", exception);
        body.value = "{}";
      }
    }
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
    responseAssertions,
    error,
    steps,
    methods,
    bodyTypes,
    toggle,
    move,
    changeBodyType,
    rest,
    authType,
    basicUser,
    basicPassword,
    digestUser,
    digestPassword,
    connectTimeout,
    responseTimeout,
  };
}
