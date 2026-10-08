import { beforeEach, afterEach, it, expect, vi } from "vitest";
import { reactive } from "vue";
const mocks = vi.hoisted(() => ({
  report: vi.fn(),
  summary: vi.fn(),
  result: vi.fn(),
  comment: vi.fn(),
  attachment: vi.fn(),
  collaboration: vi.fn(),
  issues: vi.fn(),
  shares: vi.fn(),
  share: vi.fn(),
  revoke: vi.fn(),
  confirm: vi.fn(),
  success: vi.fn(),
  download: vi.fn(),
}));
const user = reactive({ user: { id: "first" } });
vi.mock("@/stores/user", () => ({ useUserStore: () => user }));
vi.mock("ant-design-vue", () => ({
  Modal: { confirm: mocks.confirm },
  message: { success: mocks.success, error: vi.fn(), warning: vi.fn() },
}));
vi.mock("vue-router", () => ({
  onBeforeRouteLeave: vi.fn(),
  onBeforeRouteUpdate: vi.fn(),
}));
vi.mock("@/api/planCollaboration", () => ({
  planCollaborationApi: mocks,
  downloadPlanFile: mocks.download,
}));
vi.mock("@/api/caseFeatures", () => ({
  caseFeaturesApi: { issues: mocks.issues },
}));
vi.mock("@/api/nativeHttpReport", () => ({
  nativeHttpReportApi: { detail: vi.fn() },
}));
vi.mock("./ReportDetailCards.vue", () => ({ default: { render: () => null } }));
vi.mock("@/components/TestCase/CaseRichText.vue", () => ({
  default: { render: () => null },
}));
vi.mock("@/components/TestCase/CaseMindMap.vue", () => ({
  default: { render: () => null },
}));
vi.mock("@/components/Report/NativeHttpReport.vue", () => ({
  default: { render: () => null },
}));
import Report from "./PlanRunReport.vue";
import { componentHost, flushComponent as flush } from "@/test/componentHost";
const row = {
  caseId: "master",
  associationId: "copy",
  caseName: "frozen",
  result: "pending",
  category: "functional",
  snapshot: { steps: [{ action: "a", expected: "b" }] },
};
const data = () => ({
  id: "run",
  status: "running",
  report: {
    total: 1,
    passRate: 0,
    counts: { pending: 1 },
    cases: [row],
    categories: {},
  },
  summary: { notes: "saved" },
});
beforeEach(() => {
  vi.clearAllMocks();
  user.user = { id: "first" };
  mocks.report.mockResolvedValue(data());
  mocks.collaboration.mockResolvedValue({ comments: [], attachments: [] });
  mocks.issues.mockResolvedValue([]);
  mocks.summary.mockResolvedValue({});
  mocks.comment.mockResolvedValue({});
  mocks.result.mockResolvedValue({});
  mocks.confirm.mockImplementation((o) => o.onCancel());
  vi.stubGlobal("window", {
    addEventListener: vi.fn(),
    removeEventListener: vi.fn(),
  });
});
afterEach(() => {
  vi.unstubAllGlobals();
});
it("old summary ACK across actor ABA cannot unlock a fresh write or acknowledge a new draft", async () => {
  const h = componentHost(Report, { runId: "run", projectId: "project" });
  await flush();
  const s = h.state;
  let oldFinish!: () => void, newFinish!: () => void;
  mocks.summary
    .mockReturnValueOnce(
      new Promise<void>((r) => {
        oldFinish = r;
      }),
    )
    .mockReturnValueOnce(
      new Promise<void>((r) => {
        newFinish = r;
      }),
    );
  s.summary.notes = "old";
  const old = s.saveSummary();
  user.user = { id: "other" };
  user.user = { id: "first" };
  await flush();
  s.summary.notes = "new";
  const newer = s.saveSummary();
  oldFinish();
  await old;
  expect(s.saveBusy).toBe(true);
  expect(s.savedSummary).not.toContain("old");
  expect(mocks.success).not.toHaveBeenCalled();
  newFinish();
  await newer;
  expect(s.saveBusy).toBe(false);
  expect(s.savedSummary).toContain("new");
  h.stop();
});
it("successful comment/result ACKs preserve newer input and independently acknowledge submitted fields", async () => {
  const h = componentHost(Report, { runId: "run", projectId: "project" });
  await flush();
  const s = h.state;
  await s.openCase(row);
  s.comment = "submitted";
  let finish!: () => void;
  mocks.comment.mockReturnValueOnce(
    new Promise<void>((r) => {
      finish = r;
    }),
  );
  const post = s.sendComment();
  s.comment = "newer";
  finish();
  await post;
  expect(s.comment).toBe("newer");
  expect(s.draft.dirty.value).toBe(true);
  s.comment = "";
  s.stepRows[0].actual = "submitted step";
  mocks.result.mockReturnValueOnce(
    new Promise<void>((r) => {
      finish = r;
    }),
  );
  const result = s.saveResult();
  s.stepRows[0].actual = "newer step";
  finish();
  await result;
  expect(s.stepRows[0].actual).toBe("newer step");
  expect(s.draft.dirty.value).toBe(true);
  h.stop();
});
it("late FileReader completion after scope change never submits an attachment under the new actor", async () => {
  let reader: any;
  class Reader {
    onload: () => void = () => {};
    onerror: () => void = () => {};
    result = "data:text/plain;base64,YQ==";
    error = null;
    constructor() {
      reader = this;
    }
    readAsDataURL() {}
  }
  vi.stubGlobal("FileReader", Reader);
  const h = componentHost(Report, { runId: "run", projectId: "project" });
  await flush();
  const s = h.state;
  await s.openCase(row);
  const pending = s.upload({
    size: 1,
    name: "synthetic.txt",
    type: "text/plain",
  } as File);
  user.user = { id: "other" };
  await flush();
  reader.onload();
  await pending;
  expect(mocks.attachment).not.toHaveBeenCalled();
  expect(s.saveBusy).toBe(false);
  h.stop();
});
it("old discard confirmation after actor or draft change cannot close or clear current content", async () => {
  const h = componentHost(Report, { runId: "run", projectId: "project" });
  await flush();
  const s = h.state;
  await s.openCase(row);
  s.comment = "draft";
  mocks.confirm.mockImplementation(() => {});
  const pending = s.closeCase();
  await flush();
  const confirmation = mocks.confirm.mock.calls[0][0];
  user.user = { id: "other" };
  await flush();
  await s.openCase(row);
  s.comment = "fresh";
  confirmation.onOk();
  await pending;
  expect(s.caseOpen).toBe(true);
  expect(s.comment).toBe("fresh");
  h.stop();
});
for (const n of [1, 2, 3, 4, 5])
  it(`refresh guard tail generation boundary n${n}`, async () => {
    const h = componentHost(Report, { runId: "run", projectId: "project" });
    await flush();
    const s = h.state,
      actors: string[] = [];
    mocks.report.mockImplementation(() => {
      actors.push(user.user.id);
      return Promise.resolve(data());
    });
    s.detailCards = {
      beforeClose: () =>
        Promise.resolve().then(() => {
          const step = (left: number): void =>
            queueMicrotask(() =>
              left > 1 ? step(left - 1) : (user.user = { id: "other" }),
            );
          step(n);
          return true;
        }),
    };
    await s.load();
    await flush();
    expect(actors.filter((a) => a === "other")).toHaveLength(1);
    h.stop();
  });

it("refresh ACK preserves newer summary input and cannot revert a successful save", async () => {
  const h = componentHost(Report, { runId: "run", projectId: "project" });
  await flush();
  const s = h.state;
  let finish!: (v: any) => void;
  mocks.report.mockReturnValueOnce(
    new Promise((r) => {
      finish = r;
    }),
  );
  const load = s.load();
  await flush();
  s.summary.notes = "new input";
  finish(data());
  await load;
  expect(s.summary.notes).toBe("new input");
  expect(s.savedSummary).toContain("saved");
  s.summary.notes = "saved";
  mocks.report.mockReturnValueOnce(
    new Promise((r) => {
      finish = r;
    }),
  );
  const old = s.load();
  await flush();
  s.summary.notes = "successfully submitted";
  await s.saveSummary();
  finish(data());
  await old;
  expect(s.summary.notes).toBe("successfully submitted");
  expect(s.savedSummary).toContain("successfully submitted");
  expect(s.loading).toBe(false);
  h.stop();
});
