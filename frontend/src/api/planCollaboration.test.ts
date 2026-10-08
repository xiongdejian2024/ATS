import { it, expect, vi, afterEach } from "vitest";
vi.mock("@/stores/user", () => ({
  useUserStore: () => ({ accessToken: "synthetic-test-token" }),
}));
vi.mock("@/utils/api", () => ({ apiClient: {} }));
import { downloadPlanFile } from "./planCollaboration";
afterEach(() => {
  vi.unstubAllGlobals();
});
it("download generation check runs after the delayed blob and preserves existing default caller behavior", async () => {
  const click = vi.fn(),
    create = vi.fn().mockReturnValue("blob:synthetic"),
    revoke = vi.fn(),
    timeout = vi.fn();
  vi.stubGlobal("URL", { createObjectURL: create, revokeObjectURL: revoke });
  vi.stubGlobal("document", { createElement: () => ({ click }) });
  vi.stubGlobal("setTimeout", timeout);
  let finish!: (v: Blob) => void;
  vi.stubGlobal(
    "fetch",
    vi.fn().mockResolvedValue({
      ok: true,
      blob: () => new Promise<Blob>((r) => (finish = r)),
    }),
  );
  let current = true;
  const old = downloadPlanFile(
    "runs/synthetic/pdf",
    "report.pdf",
    () => current,
  );
  for (let i = 0; i < 8; i++) await Promise.resolve();
  current = false;
  finish(new Blob(["synthetic-pdf"]));
  await old;
  expect(click).not.toHaveBeenCalled();
  expect(create).not.toHaveBeenCalled();
  vi.stubGlobal(
    "fetch",
    vi.fn().mockResolvedValue({
      ok: true,
      blob: async () => new Blob(["synthetic-pdf"]),
    }),
  );
  await downloadPlanFile("runs/synthetic/pdf", "report.pdf");
  expect(click).toHaveBeenCalledOnce();
  expect(timeout).toHaveBeenCalledOnce();
});
