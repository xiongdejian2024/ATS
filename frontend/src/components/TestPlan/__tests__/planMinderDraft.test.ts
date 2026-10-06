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
  it("整批删除默认与父子集保留其他关联，取消完整还原配置、顺序和指纹", () => {
    const source = fixture();
    source.nodes = [
      {
        id: "parent",
        name: "父集",
        nodeType: "point",
        category: "api",
        parentId: null,
        position: 0,
      },
      {
        id: "child",
        name: "子集",
        nodeType: "point",
        category: "api",
        parentId: "parent",
        position: 0,
      },
      {
        id: "keep",
        name: "保留集",
        nodeType: "point",
        category: "scenario",
        parentId: null,
        position: 0,
      },
    ] as PlanNode[];
    source.entries.api.push({
      associationId: "child-original",
      caseId: "master-child",
      collectionId: "child",
    } as PlanCaseEntry);
    source.entries.scenario.push({
      associationId: "keep-original",
      caseId: "master-keep",
      collectionId: "keep",
    } as PlanCaseEntry);
    const draft = new PlanMinderDraft();
    draft.load(source);
    draft.configure("default:api", {
      ...source.executionCatalog.configurations["default:api"].config,
      extended: false,
    });
    draft.removeMany([
      { category: "api" },
      { nodeId: "parent", category: "api" },
      { nodeId: "child", category: "api" },
    ]);
    expect(draft.payload.points.map((n) => n.id)).toEqual(["keep"]);
    expect(draft.payload.deleteDefaults).toEqual(["api"]);
    expect(draft.workspace!.entries.api).toEqual([]);
    expect(draft.workspace!.entries.scenario[0].associationId).toBe(
      "keep-original",
    );
    expect(draft.payload.configurations).toEqual({});
    expect(draft.payload.expectedFingerprint).toBe(source.fingerprint);
    draft.reset();
    expect(draft.workspace).toEqual(source);
    expect(draft.dirty).toBe(false);
  });
  it("范围中一个节点过期或分类不符时，不部分删除前面合法集", () => {
    const draft = new PlanMinderDraft();
    draft.load(fixture());
    expect(() =>
      draft.removeMany([
        { category: "api" },
        { category: "api", nodeId: "missing" },
      ]),
    ).toThrow("重新选择");
    expect(draft.workspace!.entries.api).toHaveLength(1);
    expect(draft.dirty).toBe(false);
  });
  it("直接插入可暂存默认重名文本，退出编辑及保存前须改名，原关联保留", () => {
    const draft = new PlanMinderDraft();
    draft.load(fixture());
    const point = draft.insert("api");
    expect(point.name).toBe("默认测试集");
    expect(draft.isNew(point.id)).toBe(true);
    expect(() => draft.validate()).toThrow("默认测试集");
    draft.rename(point.id, "直接改名集");
    expect(() => draft.validate()).not.toThrow();
    expect(draft.workspace!.entries.api[0].collectionId).toBeNull();
    draft.reset();
    expect(draft.dirty).toBe(false);
    expect(draft.workspace!.nodes).toEqual([]);
  });
  it("新集复制分类当前配置为独立初始值，同级插入顺序正确，父配置以后变化不覆盖", () => {
    const draft = new PlanMinderDraft();
    draft.load(fixture());
    const a = draft.insert("api");
    draft.rename(a.id, "第一集");
    const b = draft.insert("api", a.id);
    draft.rename(b.id, "第二集");
    expect(draft.workspace!.nodes.map((n) => n.position)).toEqual([0, 1]);
    const scope = `node:api:${b.id}`;
    expect(draft.payload.configurations[scope].config.extended).toBe(false);
    draft.configure("root:api", {
      ...draft.workspace!.executionCatalog.configurations["root:api"].config,
      executionMode: "parallel",
    });
    expect(
      draft.workspace!.executionCatalog.configurations[scope].effectiveConfig
        .executionMode,
    ).toBe("serial");
  });
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
  it("临时集关联保持原关联计数，重复打开替换选择，取消完整还原", () => {
    const source = fixture(),
      draft = new PlanMinderDraft();
    draft.load(source);
    const target = draft.add("api", "关联临时集");
    const summary = {
      count: 2,
      excludedCount: 0,
      automatedCount: 2,
      usesTree: false,
      compatibleSuiteIds: [],
      canAssociate: true,
    };
    draft.associate(
      { category: "api", collectionId: target.id, caseIds: ["a", "b"] },
      summary,
    );
    expect(draft.workspace!.entries.api).toEqual(source.entries.api);
    expect(draft.association("api", target.id)?.summary.count).toBe(2);
    expect(draft.associationPreview("api", target.id).associations).toEqual([]);
    draft.associate(
      { category: "api", collectionId: target.id, caseIds: ["c"] },
      { ...summary, count: 1 },
    );
    expect(draft.payload.associations).toHaveLength(1);
    expect(draft.payload.associations![0].caseIds).toEqual(["c"]);
    expect(draft.dirty).toBe(true);
    draft.reset();
    expect(draft.payload.associations).toEqual([]);
    expect(draft.workspace).toEqual(source);
    expect(draft.dirty).toBe(false);
  });
  it("待关联默认集实体化时目标迁移，删除同步目标仅撤销该分类，父集删除撤销本集关联", () => {
    const draft = new PlanMinderDraft();
    draft.load(fixture());
    const functional = draft.add("functional", "功能临时集"),
      scene = draft.add("scenario", "场景临时集");
    const summary = {
      count: 1,
      excludedCount: 0,
      automatedCount: 0,
      usesTree: false,
      compatibleSuiteIds: [],
      canAssociate: true,
      sync: {
        api: { count: 2, compatibleSuiteIds: [] },
        scenario: { count: 1, compatibleSuiteIds: [] },
      },
    };
    draft.associate(
      {
        category: "functional",
        collectionId: functional.id,
        caseIds: ["a"],
        syncCase: true,
        apiCaseCollectionId: "default",
        apiScenarioCollectionId: scene.id,
      },
      summary,
    );
    const api = draft.materializeDefault("api", "实体化默认集");
    expect(draft.payload.associations![0].apiCaseCollectionId).toBe(api.id);
    draft.remove(api.id);
    expect(draft.payload.associations![0].apiCaseCollectionId).toBeUndefined();
    expect(draft.payload.associations![0].apiScenarioCollectionId).toBe(
      scene.id,
    );
    expect(
      draft.association("functional", functional.id)?.summary.sync?.api.count,
    ).toBe(0);
    draft.remove(functional.id);
    expect(draft.payload.associations).toEqual([]);
    expect(draft.payload.points.map((p) => p.id)).toEqual([scene.id]);
  });
});
