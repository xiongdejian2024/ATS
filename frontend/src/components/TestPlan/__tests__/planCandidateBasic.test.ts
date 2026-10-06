import { describe, it, expect, vi } from "vitest";
import { ref } from "vue";
import {
  basicCondition,
  readProtocols,
  writeProtocols,
  protocolStorageKey,
  requestMethods,
  methodColor,
} from "../planCandidateBasic";
import { planCandidateColumns } from "../planCandidateColumns";
import {
  normalizeDisplay,
  displayStorageKey,
} from "@/components/Table/tableDisplay";
import { useCandidateModules } from "../planCandidateModules";

describe("关联接口基础交互", () => {
  it("协议排除偏好按用户隔离，新协议默认可见，空范围不会冒充全部", () => {
    const store = new Map<string, string>();
    const storage = {
      getItem: (k: string) => store.get(k) ?? null,
      setItem: (k: string, v: string) => {
        store.set(k, v);
      },
    };
    const key = protocolStorageKey("first");
    writeProtocols(storage, key, ["HTTP", "TCP"], []);
    expect(readProtocols(storage, key, ["HTTP", "TCP"])).toEqual([]);
    expect(readProtocols(storage, key, ["HTTP", "TCP", "DUBBO"])).toEqual([
      "DUBBO",
    ]);
    expect(
      readProtocols(storage, protocolStorageKey("second"), ["HTTP", "TCP"]),
    ).toBeUndefined();
    expect(
      basicCondition({
        protocols: [],
        methods: ["POST"],
        createdBy: ["person"],
      }),
    ).toEqual({ protocols: [], methods: ["POST"], createdBy: ["person"] });
    expect(basicCondition({ search: "ignored" })).toEqual({});
    store.set(key, "not-json");
    const error = vi.spyOn(console, "error").mockImplementation(() => {});
    expect(readProtocols(storage, key, ["HTTP"])).toBeUndefined();
    expect(error).toHaveBeenCalledWith(
      "读取关联协议偏好失败，使用全部协议",
      expect.any(Error),
    );
    error.mockRestore();
  });
  it("两种资源具有不同默认列，隐藏列可开启且ID名称保持必选", () => {
    const api = planCandidateColumns("API"),
      cases = planCandidateColumns("CASE");
    expect(
      normalizeDisplay(undefined, api)
        .columns.filter((c) => c.visible)
        .map((c) => c.key),
    ).toEqual([
      "id",
      "name",
      "method",
      "path",
      "tags",
      "caseTotal",
      "createdByName",
    ]);
    expect(
      normalizeDisplay(undefined, cases)
        .columns.filter((c) => c.visible)
        .map((c) => c.key),
    ).toEqual([
      "caseCode",
      "name",
      "priority",
      "path",
      "tags",
      "createdByName",
      "createdAt",
    ]);
    expect(
      displayStorageKey("person", "project", "associate-api-definition"),
    ).not.toBe(displayStorageKey("person", "project", "associate-api-case"));
    expect(requestMethods).toEqual([
      "GET",
      "POST",
      "PUT",
      "DELETE",
      "PATCH",
      "OPTIONS",
      "HEAD",
      "CONNECT",
    ]);
    expect(methodColor("GET")).not.toBe(methodColor("POST"));
    expect(methodColor("plugin")).toBe(methodColor("PUT"));
  });
  it("选择当前父模块只改变精确父模块，保留子模块排除与跨页选择", () => {
    const modules = useCandidateModules(
      {
        enabled: ref(true),
        modules: ref([
          { id: "parent", name: "父", count: 1 },
          { id: "child", parentId: "parent", name: "子", count: 2 },
        ]),
        rows: ref([
          { id: "one", moduleId: "parent" },
          { id: "two", moduleId: "child" },
        ]),
      },
      ref(undefined),
    );
    modules.check("parent", true);
    modules.keysChanged(["one"]);
    expect(modules.maps.value.child.excludeIds).toEqual(["two"]);
    modules.currentModule("parent", false);
    expect(modules.maps.value.child.excludeIds).toEqual(["two"]);
    expect(modules.pageSelected.value).toEqual([]);
    modules.currentModule("parent", true);
    expect(modules.pageSelected.value).toEqual(["one"]);
  });
});
