import { beforeEach, expect, it, vi } from "vitest";
import { reactive } from "vue";
import { componentHost, flushComponent as flush } from "@/test/componentHost";
const api = vi.hoisted(() => ({
  list: vi.fn(),
  detail: vi.fn(),
  templates: vi.fn(),
  save: vi.fn(),
  comments: vi.fn(),
  history: vi.fn(),
  comment: vi.fn(),
  removeComment: vi.fn(),
  archive: vi.fn(),
  saveTemplate: vi.fn(),
  removeTemplate: vi.fn(),
  confirm: vi.fn(),
  download: vi.fn(),
}));
const user = reactive({ user: { id: "owner" } });
const project = reactive({ currentProject: { id: "project" }, projects: [] });
const route = reactive({ query: {} });
vi.mock("@/stores/user", () => ({ useUserStore: () => user }));
vi.mock("@/stores/project", () => ({ useProjectStore: () => project }));
vi.mock("@/api/defects", () => ({ defectsApi: api }));
vi.mock("@/api/fileLibrary", () => ({
  fileLibraryApi: { download: api.download },
}));
vi.mock("@/api/caseFeatures", () => ({ saveCaseBlob: vi.fn() }));
vi.mock("ant-design-vue", () => ({
  Modal: { confirm: api.confirm },
  message: { success: vi.fn(), error: vi.fn() },
}));
vi.mock("vue-router", () => ({
  useRoute: () => route,
  onBeforeRouteLeave: vi.fn(),
  onBeforeRouteUpdate: vi.fn(),
}));
vi.mock("./CaseRichText.vue", () => ({ default: { render: () => null } }));
vi.mock("./CaseCustomFields.vue", () => ({ default: { render: () => null } }));
vi.mock("./FileLibraryPicker.vue", () => ({ default: { render: () => null } }));
import Drawer from "./DefectDetailDrawer.vue";
import Manager from "./DefectTemplateManager.vue";
import Page from "@/views/Defects.vue";
const caps = {
  canRead: true,
  canCreate: true,
  canUpdate: true,
  canDelete: true,
};
const detail = () => ({
  id: "defect",
  title: "Original",
  description: "saved",
  descriptionFormat: "plain",
  status: "open",
  externalRef: null,
  templateId: null,
  customFields: {},
  files: [],
  revision: 1,
  archived: false,
  ...caps,
});
const props = {
  open: true,
  projectId: "project",
  defectId: "defect",
  initialCapabilities: caps,
};
function deferred<T = any>() {
  let resolve!: (v: T) => void;
  const promise = new Promise<T>((r) => {
    resolve = r;
  });
  return { promise, resolve };
}
beforeEach(() => {
  vi.resetAllMocks();
  user.user = { id: "owner" };
  project.currentProject = { id: "project" };
  route.query = {};
  api.list.mockResolvedValue({ items: [], total: 0, ...caps });
  api.detail.mockResolvedValue(detail());
  api.templates.mockResolvedValue({ items: [], ...caps });
  api.comments.mockResolvedValue({ items: [], total: 0 });
  api.history.mockResolvedValue({ items: [], total: 0 });
  api.comment.mockResolvedValue({ id: "comment", revision: 2 });
  api.save.mockResolvedValue({ id: "defect", revision: 2 });
  api.removeComment.mockResolvedValue({ revision: 2 });
  vi.stubGlobal("window", {
    addEventListener: vi.fn(),
    removeEventListener: vi.fn(),
  });
});
it("save ACK records the submitted baseline and preserves later changes", async () => {
  const pending = deferred();
  api.save.mockReturnValue(pending.promise);
  const closed = vi.fn(),
    h = componentHost(Drawer, { ...props, "onUpdate:open": closed });
  await flush();
  h.state.draft.title = "Submitted";
  const operation = h.state.save();
  h.state.draft.title = "Later";
  pending.resolve({ id: "defect", revision: 2 });
  await operation;
  expect(api.save.mock.calls[0][1].title).toBe("Submitted");
  expect(h.state.draft.title).toBe("Later");
  expect(h.state.dirty).toBe(true);
  expect(h.state.draft.expectedRevision).toBe(2);
  expect(closed).not.toHaveBeenCalled();
  h.stop();
});
it("failed create retries the same key and successful ACK adopts the identity", async () => {
  api.save
    .mockRejectedValueOnce(Error("response lost"))
    .mockResolvedValueOnce({ id: "created", revision: 1 });
  const h = componentHost(Drawer, { ...props, defectId: "" });
  await flush();
  h.state.draft.title = "New";
  await h.state.save();
  const key = api.save.mock.calls[0][1].requestId;
  await h.state.save();
  expect(key).toBeTruthy();
  expect(api.save.mock.calls[1][1].requestId).toBe(key);
  expect(api.save.mock.calls[1][2]).toBeUndefined();
  expect(h.state.id).toBe("created");
  h.stop();
});
it.each(["actor", "project", "unmount"])(
  "late save is ignored after %s changes",
  async (kind) => {
    const pending = deferred();
    api.save.mockReturnValue(pending.promise);
    const changed = vi.fn();
    const h = componentHost(Drawer, { ...props, onChanged: changed });
    await flush();
    h.state.draft.title = "Submitted";
    const operation = h.state.save();
    if (kind === "actor") user.user = { id: "other" };
    else if (kind === "project") h.props.projectId = "other";
    else h.stop();
    await flush();
    pending.resolve({ id: "defect", revision: 2 });
    await operation;
    expect(changed).not.toHaveBeenCalled();
    if (kind !== "unmount") h.stop();
  },
);
it("project ABA ignores the first detail receipt", async () => {
  const first = deferred();
  api.detail.mockReturnValueOnce(first.promise);
  const h = componentHost(Drawer, props);
  h.props.projectId = "other";
  await flush();
  h.props.projectId = "project";
  await flush();
  first.resolve({ ...detail(), title: "Stale" });
  await flush();
  expect(h.state.draft.title).toBe("Original");
  h.stop();
});
it("comment ACK preserves unsaved description and advances its baseline version", async () => {
  const h = componentHost(Drawer, props);
  await flush();
  h.state.draft.description = "Unsaved description";
  h.state.commentDraft.content = "Comment";
  await h.state.submitComment();
  expect(h.state.draft.description).toBe("Unsaved description");
  expect(h.state.dirty).toBe(true);
  expect(h.state.draft.expectedRevision).toBe(2);
  expect(h.state.commentDraft.content).toBe("");
  h.stop();
});
it("comment ACK retains text typed after submission and assigns a fresh key", async () => {
  const pending = deferred();
  api.comment.mockReturnValue(pending.promise);
  const h = componentHost(Drawer, props);
  await flush();
  h.state.commentDraft.content = "Submitted";
  const key = h.state.commentDraft.requestId,
    operation = h.state.submitComment();
  h.state.commentDraft.content = "Later";
  pending.resolve({ id: "comment", revision: 2 });
  await operation;
  expect(h.state.commentDraft.content).toBe("Later");
  expect(h.state.commentDraft.requestId).not.toBe(key);
  h.stop();
});
it("comment delete refresh cannot notify a changed actor", async () => {
  const changed = vi.fn(),
    h = componentHost(Drawer, { ...props, onChanged: changed });
  await flush();
  h.state.removeComment({ id: "comment", canDelete: true });
  const pending = deferred();
  api.comments.mockReturnValueOnce(pending.promise);
  const operation = api.confirm.mock.calls[0][0].onOk();
  await flush();
  user.user = { id: "other" };
  await flush();
  pending.resolve({ items: [], total: 0 });
  await operation;
  expect(changed).not.toHaveBeenCalled();
  h.stop();
});
it("discard confirmation refuses a draft changed while confirmation is open", async () => {
  const h = componentHost(Drawer, props);
  await flush();
  h.state.draft.description = "First";
  const operation = h.state.beforeClose();
  h.state.draft.description = "Later";
  api.confirm.mock.calls[0][0].onOk();
  expect(await operation).toBe(false);
  h.stop();
});
it("read-only capability prevents writes despite direct handler calls", async () => {
  api.detail.mockResolvedValue({
    ...detail(),
    canUpdate: false,
    canDelete: false,
  });
  const h = componentHost(Drawer, props);
  await flush();
  await h.state.save();
  h.state.archive();
  expect(api.save).not.toHaveBeenCalled();
  expect(api.archive).not.toHaveBeenCalled();
  expect(api.confirm).not.toHaveBeenCalled();
  h.stop();
});
it("legacy plain description is explicitly escaped before rich conversion", async () => {
  api.detail.mockResolvedValue({ ...detail(), description: "<script> & text" });
  const h = componentHost(Drawer, props);
  await flush();
  h.state.convertRich();
  expect(h.state.draft.description).toBe("<p>&lt;script&gt; &amp; text</p>");
  expect(h.state.draft.descriptionFormat).toBe("rich");
  h.stop();
});
it("template defaults clone reactive multiselect arrays", async () => {
  api.templates.mockResolvedValue({
    items: [
      {
        id: "template",
        name: "Template",
        revision: 1,
        isDefault: true,
        defaults: {},
        fields: [
          {
            key: "multi",
            name: "Choice",
            type: "multiselect",
            required: false,
            options: ["a", "b"],
            default: ["a"],
          },
        ],
      },
    ],
    ...caps,
  });
  const h = componentHost(Manager, { projectId: "project" });
  await flush();
  h.state.form.fields[0].default.push("b");
  expect(h.state.templates[0].fields[0].default).toEqual(["a"]);
  h.stop();
});
it("late template catalog cannot overwrite a later draft", async () => {
  const h = componentHost(Manager, { projectId: "project" });
  await flush();
  const pending = deferred();
  api.templates.mockReturnValueOnce(pending.promise);
  const operation = h.state.load();
  h.state.form.name = "Later draft";
  pending.resolve({ items: [], ...caps });
  await operation;
  expect(h.state.form.name).toBe("Later draft");
  h.stop();
});
it("parent route guard refuses actor changes between child guards", async () => {
  const h = componentHost(Page, {});
  await flush();
  h.state.drawer = {
    beforeClose: () =>
      Promise.resolve().then(() => {
        user.user = { id: "other" };
        return true;
      }),
  };
  expect(await h.state.beforeClose()).toBe(false);
  h.stop();
});
it("page catalog is paged with bounded size and literal search", async () => {
  const h = componentHost(Page, {});
  await flush();
  h.state.search = "%_literal";
  await h.state.applyFilters();
  expect(api.list.mock.lastCall?.[1]).toMatchObject({
    page: 1,
    size: 20,
    search: "%_literal",
  });
  h.stop();
});
