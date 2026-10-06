import { describe, it, expect } from "vitest";
import { PlanMinderDraft } from "../planMinderDraft";
import type { MinderWorkspace } from "@/api/planMinder";
import type { ExecutionConfig } from "@/api/planExecutionConfig";
import type { PlanNode } from "@/api/planTree";
import type { PlanCaseEntry } from "@/api/planCaseWorkspace";
function fixture(): MinderWorkspace {
  const config: ExecutionConfig = {
    extended: false,
    executionMode: "serial",
    testResourcePoolId: "DEFAULT",
    requestEnvironmentId: "NONE",
    stopOnFailure: false,
    retryOnFailure: false,
    retryTimes: 1,
    retryInterval: 0,
  };
  return {
    fingerprint: "a".repeat(64),
    policy: {
      groupId: null,
      executionMode: "serial",
      stopOnFailure: false,
      passThreshold: 100,
      suiteOrder: [],
    },
    nodes: [],
    entries: {
      functional: [],
      api: [
        {
          associationId: "original",
          caseId: "master",
          collectionId: null,
        } as unknown as PlanCaseEntry,
      ],
      scenario: [],
    },
    usesTree: false,
    executionCatalog: {
      configurations: Object.fromEntries(
        ["root:api", "default:api", "root:scenario", "default:scenario"].map(
          (scope) => [
            scope,
            {
              scope,
              revision: scope.startsWith("default:") ? 2 : 1,
              config: { ...config, extended: scope.startsWith("default:") },
              effectiveConfig: {
                ...config,
                extended: scope.startsWith("default:"),
              },
            },
          ],
        ),
      ),
      pools: [],
      requestEnvironments: [],
      resources: [],
    },
  };
}
describe("规划整体草稿", () => {
  it("计划根方式只更新未持久化分类默认，保留显式配置与策略，取消可还原", () => {
    const source = fixture();
    source.executionCatalog.configurations["root:api"].revision = 0;
    source.policy.passThreshold = 88;
    const draft = new PlanMinderDraft();
    draft.load(source);
    draft.setExecutionMode("parallel");
    expect(draft.payload.executionMode).toBe("parallel");
    expect(draft.workspace!.policy.passThreshold).toBe(88);
    expect(
      draft.workspace!.executionCatalog.configurations["default:api"]
        .effectiveConfig.executionMode,
    ).toBe("parallel");
    expect(
      draft.workspace!.executionCatalog.configurations["root:scenario"]
        .effectiveConfig.executionMode,
    ).toBe("serial");
    expect(source.policy.executionMode).toBe("serial");
    draft.reset();
    expect(draft.dirty).toBe(false);
    expect(draft.payload.executionMode).toBeUndefined();
  });
  it("计划根切换不覆盖同一草稿显式编辑的分类执行方式", () => {
    const source = fixture();
    source.executionCatalog.configurations["root:api"].revision = 0;
    const draft = new PlanMinderDraft();
    draft.load(source);
    draft.configure("root:api", {
      ...source.executionCatalog.configurations["root:api"].config,
      executionMode: "serial",
    });
    draft.setExecutionMode("parallel");
    expect(
      draft.workspace!.executionCatalog.configurations["root:api"]
        .effectiveConfig.executionMode,
    ).toBe("serial");
    expect(draft.payload.configurations["root:api"].expectedRevision).toBe(0);
  });
  it("新增、改名和取消不修改原快照；保存失败仍保留完整待提交内容", () => {
    const source = fixture(),
      draft = new PlanMinderDraft();
    draft.load(source);
    const node = draft.add("api", "新集");
    draft.rename(node.id, "改名");
    const submitted = draft.payload;
    expect(draft.dirty).toBe(true);
    expect(source.nodes).toEqual([]);
    // 请求拒绝后不调用load，重试使用相同草稿和指纹。
    expect(draft.payload).toEqual(submitted);
    expect(draft.workspace!.nodes[0].name).toBe("改名");
    draft.reset();
    expect(draft.dirty).toBe(false);
    expect(draft.workspace!.nodes).toEqual([]);
  });
  it("同分类重复名称被拒绝，跨分类可同名，不允许复制虚拟默认集名", () => {
    const draft = new PlanMinderDraft();
    draft.load(fixture());
    draft.add("api", "名称");
    expect(() => draft.add("api", "名称")).toThrow("不能重复");
    expect(() => draft.add("scenario", "名称")).not.toThrow();
    expect(() => draft.add("api", "默认测试集")).toThrow("默认测试集");
  });
  it("默认集改名及排序按动作转换，关联身份和配置版本保持，取消恢复", () => {
    const draft = new PlanMinderDraft();
    draft.load(fixture());
    const other = draft.add("api", "另一个集"),
      node = draft.materializeDefault("api", "已命名默认集");
    expect(draft.workspace!.entries.api[0]).toMatchObject({
      associationId: "original",
      caseId: "master",
      collectionId: node.id,
    });
    expect(
      draft.payload.points.find((n) => n.id === node.id)!.materializeDefault,
    ).toBe("api");
    draft.reorder("api", null, [other.id, node.id]);
    expect(draft.payload.points.find((n) => n.id === node.id)!.position).toBe(
      1,
    );
    const scope = `node:api:${node.id}`,
      config = {
        ...draft.workspace!.executionCatalog.configurations[scope].config,
        extended: false,
        retryOnFailure: true,
        retryTimes: 3,
      };
    draft.configure(scope, config);
    expect(draft.payload.configurations[scope].expectedRevision).toBe(2);
    draft.reset();
    expect(draft.workspace!.entries.api[0].collectionId).toBeNull();
    expect(draft.dirty).toBe(false);
  });
  it("同级排序不能跨分类或父级，旧嵌套与混合分类仍保留", () => {
    const source = fixture();
    source.nodes = [
      {
        id: "parent",
        category: "functional",
        nodeType: "point",
        name: "公共",
        parentId: null,
        position: 0,
      },
      {
        id: "child",
        category: "api",
        nodeType: "point",
        name: "旧子集",
        parentId: "parent",
        position: 0,
      },
    ] as PlanNode[];
    const draft = new PlanMinderDraft();
    draft.load(source);
    const node = draft.add("api", "一级集");
    expect(() => draft.reorder("api", null, ["child", node.id])).toThrow(
      "同一父级",
    );
    expect(() => draft.reorder("api", null, ["parent", node.id])).toThrow(
      "同一父级",
    );
    expect(draft.payload.points.find((n) => n.id === "child")!.parentId).toBe(
      "parent",
    );
  });
  it("删除真实集和默认集只移除相应关联草稿，其他分类保留", () => {
    const source = fixture();
    source.nodes = [
      {
        id: "parent",
        category: "functional",
        nodeType: "point",
        name: "父",
        position: 0,
      },
      {
        id: "child",
        category: "functional",
        nodeType: "point",
        name: "子",
        parentId: "parent",
        position: 0,
      },
    ] as PlanNode[];
    source.entries.functional = [
      { collectionId: "child", caseId: "same-master" } as PlanCaseEntry,
    ];
    const draft = new PlanMinderDraft();
    draft.load(source);
    draft.remove("parent");
    expect(draft.workspace!.entries.functional).toEqual([]);
    expect(draft.workspace!.entries.api).toHaveLength(1);
    draft.removeDefault("api");
    expect(draft.payload.deleteDefaults).toEqual(["api"]);
    expect(draft.workspace!.entries.api).toEqual([]);
    draft.reset();
    expect(draft.workspace!.entries.functional).toHaveLength(1);
    expect(draft.workspace!.entries.api).toHaveLength(1);
  });
  it("草稿根配置动态传给继承节点，覆盖节点保持独立，重复编辑保留原版本", () => {
    const draft = new PlanMinderDraft();
    draft.load(fixture());
    const a = draft.add("api", "继承集"),
      b = draft.add("api", "覆盖集");
    const catalog = draft.workspace!.executionCatalog.configurations;
    draft.configure(`node:api:${b.id}`, {
      ...catalog[`node:api:${b.id}`].effectiveConfig,
      extended: false,
      retryTimes: 2,
    });
    draft.configure("root:api", {
      ...catalog["root:api"].config,
      retryTimes: 4,
    });
    draft.configure("root:api", {
      ...catalog["root:api"].config,
      retryTimes: 5,
    });
    expect(catalog[`node:api:${a.id}`].effectiveConfig.retryTimes).toBe(5);
    expect(catalog[`node:api:${b.id}`].effectiveConfig.retryTimes).toBe(2);
    expect(draft.payload.configurations["root:api"].expectedRevision).toBe(1);
  });
});
