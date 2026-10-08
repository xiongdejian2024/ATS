import { it, expect, vi, beforeEach } from "vitest";
import { reactive, effectScope } from "vue";
const m = vi.hoisted(() => ({
  catalog: vi.fn(),
  config: vi.fn(),
  saveConfig: vi.fn(),
  saveDefinition: vi.fn(),
  saveEnvironment: vi.fn(),
  confirm: vi.fn(),
  leave: vi.fn(),
  update: vi.fn(),
  success: vi.fn(),
}));
const user = reactive({ user: { id: "u" } });
vi.mock("@/stores/user", () => ({ useUserStore: () => user }));
vi.mock("@/api/nativeCase", () => ({
  nativeCaseApi: m,
  nativeStateOptions: () => [],
  nativeReportOptions: [],
}));
vi.mock("ant-design-vue", () => ({
  Modal: { confirm: m.confirm },
  message: {
    success: m.success,
    info: vi.fn(),
    warning: vi.fn(),
  },
}));
vi.mock("vue-router", () => ({
  onBeforeRouteLeave: m.leave,
  onBeforeRouteUpdate: m.update,
}));
import Config from "../NativeCaseConfig.vue";
import Variables from "../NativeVariableEditor.vue";
import Drawer from "../NativeCaseConfigDrawer.vue";
import { useNativeExecutionDraft } from "@/components/TestCase/nativeExecutionDraft";
import { componentHost, flushComponent as flush } from "@/test/componentHost";
const cfg = () => ({
  parameters: { request: {} },
  revision: 1,
  state: "DONE",
  apiDefinitionId: "d",
  environmentId: "e",
  apiChange: false,
  canEdit: true,
});
const cat = () => ({
  definitions: [
    {
      id: "d",
      name: "D",
      protocol: "HTTP",
      path: "/",
      parameters: { request: {} },
      revision: 1,
    },
  ],
  environments: [
    {
      id: "e",
      name: "E",
      address: "https://example.invalid",
      variables: [],
      revision: 1,
    },
  ],
  canCreate: true,
  canEdit: true,
  protocols: ["HTTP"],
  apiCases: [],
});
const props = { projectId: "p", caseId: "c", category: "api" };
beforeEach(() => {
  vi.resetAllMocks();
  user.user = { id: "u" };
  m.catalog.mockResolvedValue(cat());
  m.config.mockResolvedValue(cfg());
  m.saveConfig.mockResolvedValue({ ...cfg(), revision: 2 });
  m.saveEnvironment.mockResolvedValue(cat());
  vi.stubGlobal("window", {
    addEventListener: vi.fn(),
    removeEventListener: vi.fn(),
  });
  vi.spyOn(console, "error").mockImplementation(() => {});
});
it("definition incomplete variable draft requires confirmation", async () => {
  const h = componentHost(Config, props);
  await flush();
  const s = h.state;
  s.editEntity("definition", s.catalog.definitions[0]);
  const scope = effectScope();
  const editorProps = reactive({
    modelValue: s.definitionParameters,
    category: "api",
    apiCases: [],
  });
  const editor = scope.run(() =>
    useNativeExecutionDraft(editorProps, {
      update: (v) => {
        editorProps.modelValue = v;
        s.definitionParameters = v;
      },
      error: (v) => (s.entityEditorError = v),
      draft: (v) => (s.entityEditorDraft = v),
    }),
  )!;
  editor.initialVariables.value = '[{"name":""}]';
  expect(s.entityEditorError).toBeTruthy();
  const closing = s.closeEntity();
  expect(m.confirm).toHaveBeenCalled();
  m.confirm.mock.calls[0][0].onCancel();
  await closing;
  const remains = s.entityOpen;
  scope.stop();
  h.stop();
  expect(remains).true;
  expect(m.confirm).toHaveBeenCalled();
});
it("reload preserves unfinished main editor draft", async () => {
  const h = componentHost(Config, props);
  await flush();
  const s = h.state;
  s.editorDraft = "unfinished variable row";
  s.editorError = "invalid";
  await s.load(true);
  const draft = s.editorDraft;
  h.stop();
  expect(draft).toBe("unfinished variable row");
});
it("route confirmation cannot authorize a different case epoch", async () => {
  const h = componentHost(Config, props);
  await flush();
  h.state.state = "PROCESSING";
  const pending = m.leave.mock.calls[0][0]();
  const c = m.confirm.mock.calls[0][0];
  h.props.caseId = "new";
  await flush();
  c.onOk();
  const result = await pending;
  h.stop();
  expect(result).false;
});
it("confirmed environment save followed by failed config GET must not recreate on retry", async () => {
  const h = componentHost(Config, props);
  await flush();
  const s = h.state;
  s.editEntity("environment");
  s.entityName = "New";
  s.address = "https://example.invalid";
  m.config.mockRejectedValueOnce(Error("read offline"));
  await s.saveEntity();
  await s.saveEntity();
  const count = m.saveEnvironment.mock.calls.length;
  h.stop();
  expect(count).toBe(1);
});
it("main ACK preserves later local edit and old actor ABA never releases fresh save", async () => {
  const h = componentHost(Config, props);
  await flush();
  const s = h.state;
  let done!: (v: any) => void;
  m.saveConfig.mockReturnValueOnce(new Promise((r) => (done = r)));
  s.state = "PROCESSING";
  const p = s.save();
  s.state = "DEPRECATED";
  done({ ...cfg(), revision: 2, state: "PROCESSING" });
  await p;
  expect(s.state).toBe("DEPRECATED");
  expect(s.dirty).true;
  let old!: (v: any) => void, fresh!: (v: any) => void;
  m.saveConfig.mockReturnValueOnce(new Promise((r) => (old = r)));
  const a = s.save();
  user.user = { id: "v" };
  user.user = { id: "u" };
  await flush();
  m.saveConfig.mockReturnValueOnce(new Promise((r) => (fresh = r)));
  s.state = "PROCESSING";
  const b = s.save();
  old({ ...cfg(), revision: 99 });
  await a;
  expect(s.saving).true;
  expect(s.config.revision).toBe(1);
  fresh({ ...cfg(), revision: 2 });
  await b;
  h.stop();
});
it("variable echo retains incomplete row and disabled methods reject edits", async () => {
  const h = componentHost(Variables, {
    modelValue: "[]",
    onUpdateModelValue: vi.fn(),
  });
  const s = h.state;
  s.add();
  expect(s.rows[0].name).toBe("");
  h.props.modelValue = JSON.stringify(s.rows);
  await flush();
  expect(s.rows.length).toBe(1);
  h.props.disabled = true;
  await flush();
  s.change(0, "name", "x");
  s.remove(0);
  s.add();
  expect(s.rows.length).toBe(1);
  expect(s.rows[0].name).toBe("");
  h.stop();
});
it("unmounted entity write cannot emit saved", async () => {
  const saved = vi.fn();
  const h = componentHost(Config, { ...props, onSaved: saved });
  await flush();
  h.state.editEntity("environment", h.state.catalog.environments[0]);
  let done!: (v: any) => void;
  m.saveEnvironment.mockReturnValueOnce(new Promise((r) => (done = r)));
  const p = h.state.saveEntity();
  h.stop();
  done(cat());
  await p;
  expect(saved).not.toHaveBeenCalled();
});
it("outer drawer old confirmation cannot close new case", async () => {
  const change = vi.fn();
  const h = componentHost(Drawer, {
    ...props,
    open: true,
    "onUpdate:open": change,
  });
  h.state.dirty = true;
  h.state.close();
  const c = m.confirm.mock.calls[0][0];
  h.props.caseId = "new";
  await flush();
  c.onOk();
  h.stop();
  expect(change).not.toHaveBeenCalled();
});
it("variable editor must adopt external A-B-A values after prior local publish", async () => {
  const a = JSON.stringify([
    { name: "a", value: "", enable: true, description: "" },
  ]);
  const b = JSON.stringify([
    { name: "b", value: "", enable: true, description: "" },
  ]);
  const h = componentHost(Variables, { modelValue: a });
  h.state.change(0, "value", "new");
  const published = JSON.stringify(h.state.rows);
  h.props.modelValue = published;
  await flush();
  h.props.modelValue = b;
  await flush();
  expect(h.state.rows[0].name).toBe("b");
  h.props.modelValue = published;
  await flush();
  const name = h.state.rows[0].name;
  h.stop();
  expect(name).toBe("a");
});

it("load and save actions cannot overlap or roll a receipt back", async () => {
  const h = componentHost(Config, props);
  await flush();
  let readDone!: (value: any) => void;
  m.config.mockReturnValueOnce(new Promise((resolve) => (readDone = resolve)));
  const read = h.state.load(true);
  h.state.state = "PROCESSING";
  await h.state.save();
  expect(m.saveConfig).not.toHaveBeenCalled();
  readDone(cfg());
  await read;
  await h.state.save();
  expect(h.state.config.revision).toBe(2);
  h.stop();
});
it("confirmation cannot permit departure after a write starts", async () => {
  const h = componentHost(Config, props);
  await flush();
  h.state.state = "PROCESSING";
  const pending = h.state.canLeave();
  h.state.saving = true;
  m.confirm.mock.calls.at(-1)![0].onOk();
  expect(await pending).toBe(false);
  h.stop();
});
it("outer drawer child guard is fenced across case ABA", async () => {
  const change = vi.fn();
  const h = componentHost(Drawer, {
    ...props,
    open: true,
    "onUpdate:open": change,
  });
  let allow!: (value: boolean) => void;
  h.state.configRef = {
    canLeave: () => new Promise((resolve) => (allow = resolve)),
  };
  const close = h.state.close();
  h.props.caseId = "other";
  await flush();
  h.props.caseId = "c";
  await flush();
  allow(true);
  await close;
  expect(change).not.toHaveBeenCalled();
  h.stop();
});
it("route confirmation is rechecked after the promise resumes", async () => {
  const h = componentHost(Config, props);
  await flush();
  h.state.state = "PROCESSING";
  const pending = h.state.canLeave();
  m.confirm.mock.calls.at(-1)![0].onOk();
  user.user = { id: "different" };
  expect(await pending).toBe(false);
  h.stop();
});

it("environment creation receipt binds ID and revision while preserving later variable draft", async () => {
  const h = componentHost(Config, props);
  await flush();
  const s = h.state;
  s.editEntity("environment");
  s.entityName = "Created";
  s.address = "https://example.invalid";
  s.environmentVariables = '[{"name":"a","value":"submitted"}]';
  let done!: (v: any) => void;
  m.saveEnvironment.mockReturnValueOnce(new Promise((r) => (done = r)));
  const save = s.saveEntity();
  s.environmentVariables = '[{"name":"a","value":"later"}]';
  const receipt = cat();
  receipt.environments.push({
    id: "created",
    name: "Created",
    address: "https://example.invalid",
    variables: [],
    revision: 1,
  });
  done(receipt);
  await save;
  expect(s.entityId).toBe("created");
  expect(s.entityRevision).toBe(1);
  expect(s.environmentVariables).toContain("later");
  expect(s.entityOpen).true;
  expect(s.dirty).true;
  m.saveEnvironment.mockResolvedValue(receipt);
  await s.saveEntity();
  expect(m.saveEnvironment.mock.calls[1][2]).toBe("created");
  expect(m.saveEnvironment.mock.calls[1][1].expectedRevision).toBe(1);
  h.stop();
});
it("readonly config actions reject writes and modal creation", async () => {
  const h = componentHost(Config, { ...props, readonly: true });
  await flush();
  h.state.state = "PROCESSING";
  await h.state.save();
  h.state.editEntity("environment");
  await h.state.saveEntity();
  expect(h.state.entityOpen).false;
  expect(m.saveConfig).not.toHaveBeenCalled();
  expect(m.saveEnvironment).not.toHaveBeenCalled();
  h.stop();
});
