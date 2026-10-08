import { describe, it, expect, vi } from "vitest";
vi.mock("ant-design-vue", () => ({ message: { warning: vi.fn() } }));
import CaseExportDialog from "./CaseExportDialog.vue";
import { componentHost, flushComponent as flush } from "@/test/componentHost";
describe("XMind 字段分组与导出请求", () => {
  it("首次打开遵循 XMind 格式，组间选择保留，名称必选且不输出不支持字段", () => {
    const exported = vi.fn(),
      { state: s, stop } = componentHost(CaseExportDialog, {
        open: true,
        initialFormat: "xmind",
        selectedCount: 1,
        busy: false,
        onExport: exported,
      });
    expect(s.format).toBe("xmind");
    s.fields = ["name", "caseCode", "description", "createdBy"];
    s.selectGroup(["name", "caseCode"], []);
    expect(s.fields).toContain("description");
    expect(s.fields).toContain("name");
    s.submit();
    expect(exported.mock.calls[0][0].fields.split(",")).toEqual([
      "description",
      "name",
    ]);
    expect(
      s.groups.flatMap((g: any) => g.options.map((o: any) => o.value)),
    ).not.toContain("createdBy");
    stop();
  });
  it("正在导出时不会产生第二个请求", async () => {
    const exported = vi.fn(),
      {
        state: s,
        props,
        stop,
      } = componentHost(CaseExportDialog, {
        open: true,
        initialFormat: "xlsx",
        selectedCount: 0,
        busy: true,
        onExport: exported,
      });
    s.submit();
    expect(exported).not.toHaveBeenCalled();
    props.busy = false;
    await flush();
    s.submit();
    expect(exported).toHaveBeenCalledTimes(1);
    stop();
  });
});
