import { it, expect, vi, beforeEach } from "vitest";
const api = vi.hoisted(() => ({ get: vi.fn() }));
vi.mock("@/api/testPlan", () => ({ testPlanApi: { getTestPlans: api.get } }));
import Groups from "./PlanGroupTable.vue";
import { componentHost, flushComponent as flush } from "@/test/componentHost";
const props = () => ({
  projectId: "p",
  scopeKey: "p-u",
  groups: [{ id: "g", name: "Group", planCount: 100 }],
  query: { filters: '{"conditions":[],"logic":"or"}', group_id: "other" },
  revision: 1,
  busy: false,
});
beforeEach(() => {
  vi.clearAllMocks();
  api.get.mockResolvedValue({
    items: [{ id: "current", name: "Current" }],
    total: 100,
  });
});
it("loads only expanded members with group identity, current conditions and bounded pagination", async () => {
  const h = componentHost(Groups, props());
  await flush();
  expect(api.get).not.toHaveBeenCalled();
  h.state.expand(true, { id: "g" });
  await flush();
  expect(api.get).toHaveBeenCalledWith("p", {
    filters: '{"conditions":[],"logic":"or"}',
    group_id: "g",
    page: 1,
    size: 20,
  });
  await h.state.load("g", 2);
  expect(api.get.mock.calls.at(-1)![1].page).toBe(2);
  expect(h.state.state.g.page).toBe(2);
  h.stop();
});
it("same-query refresh invalidates cached and pending member responses", async () => {
  const h = componentHost(Groups, props());
  h.state.expand(true, { id: "g" });
  await flush();
  expect(h.state.state.g.items[0].id).toBe("current");
  let finish!: (v: any) => void;
  api.get.mockReturnValueOnce(new Promise((r) => (finish = r)));
  const old = h.state.load("g", 2);
  await flush();
  h.props.revision = 2;
  await flush();
  expect(h.state.expanded).toEqual([]);
  expect(h.state.state).toEqual({});
  finish({ items: [{ id: "stale" }], total: 1 });
  await old;
  expect(h.state.state).toEqual({});
  h.stop();
});
it("updated group metadata and returning scope cannot retain old members", async () => {
  const h = componentHost(Groups, props());
  h.state.expand(true, { id: "g" });
  await flush();
  h.props.groups = [{ id: "g", name: "Renamed", planCount: 100 }];
  await flush();
  expect(h.state.state).toEqual({});
  h.props.scopeKey = "q-u";
  await flush();
  h.props.scopeKey = "p-u";
  await flush();
  api.get.mockResolvedValue({ items: [{ id: "fresh" }], total: 1 });
  h.state.expand(true, { id: "g" });
  await flush();
  expect(h.state.state.g.items[0].id).toBe("fresh");
  h.stop();
});
it("failure preserves the prior page and successful retry updates its actual page", async () => {
  const h = componentHost(Groups, props());
  h.state.expand(true, { id: "g" });
  await flush();
  api.get.mockRejectedValueOnce(new Error("offline"));
  await h.state.load("g", 2);
  expect(h.state.state.g.page).toBe(1);
  expect(h.state.state.g.error).toBe(true);
  expect(h.state.state.g.items[0].id).toBe("current");
  await h.state.load("g", 2);
  expect(h.state.state.g.page).toBe(2);
  expect(h.state.state.g.error).toBe(false);
  h.stop();
});
