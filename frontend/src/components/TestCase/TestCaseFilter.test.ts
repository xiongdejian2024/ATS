import { it, expect, vi, afterEach } from "vitest";
const mocks = vi.hoisted(() => ({ confirm: vi.fn() }));
vi.mock("ant-design-vue", () => ({ Modal: { confirm: mocks.confirm } }));
import Filter from "./TestCaseFilter.vue";
import { componentHost, flushComponent as flush } from "@/test/componentHost";
afterEach(() => { vi.clearAllMocks(); });
it("optional close guard preserves canceled conditions and acknowledges only successful view saves", async () => {
  const save = vi
    .fn()
    .mockRejectedValueOnce(Error("synthetic save failure"))
    .mockResolvedValue(undefined);
  const host = componentHost(Filter, {
    visible: false,
    guardClosing: true,
    availableFields: [{ key: "name", label: "Name", type: "text" }],
    conditions: [{ field: "name", operator: "contains", value: "base" }],
    initialFields: ["name"],
    view: {
      id: "v",
      name: "View",
      filters: {
        filterConditions: [
          { field: "name", operator: "contains", value: "base" },
        ],
        filterLogic: "and",
      },
    },
    saveView: save,
    viewNames: ["View"],
  });
  host.props.visible = true;
  await flush();
  const s = host.state;
  expect(s.hasDraft).toBe(false);
  s.draft[0].value = "edited";
  mocks.confirm.mockImplementationOnce((o: any) => o.onCancel());
  expect(await s.beforeClose()).toBe(false);
  expect(s.draft[0].value).toBe("edited");
  await s.save("update");
  expect(s.hasDraft).toBe(true);
  expect(s.error).toContain("草稿");
  await s.save("update");
  expect(s.hasDraft).toBe(false);
  s.draft[0].value = "discard";
  mocks.confirm.mockImplementationOnce((o: any) => o.onOk());
  expect(await s.beforeClose()).toBe(true);
  expect(s.draft[0].value).toBe("edited");
  host.stop();
});
