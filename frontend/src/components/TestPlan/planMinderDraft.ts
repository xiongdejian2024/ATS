import { cloneDeep } from "lodash-es";
import type { MinderDeletionTarget } from "./planMinderSelection";
import type {
  MinderCategory,
  MinderSave,
  MinderWorkspace,
} from "@/api/planMinder";
import type { PlanNode } from "@/api/planTree";
import type { ExecutionConfig } from "@/api/planExecutionConfig";
import type {
  PlanAssociation,
  CandidateSelectionPreview,
} from "@/api/planCaseWorkspace";

/** 整幅规划草稿与远程快照分离；保存失败不丢结构、关联计数或配置。 */
export class PlanMinderDraft {
  workspace?: MinderWorkspace;
  private original?: MinderWorkspace;
  private materialized: Partial<Record<MinderCategory, string>> = {};
  private deleteDefaults: MinderCategory[] = [];
  private configurations: MinderSave["configurations"] = {};
  private associations: {
    request: PlanAssociation;
    summary: CandidateSelectionPreview;
  }[] = [];
  load(value: MinderWorkspace) {
    this.original = cloneDeep(value);
    this.workspace = cloneDeep(value);
    this.materialized = {};
    this.deleteDefaults = [];
    this.configurations = {};
    this.associations = [];
  }
  clear() {
    this.workspace = undefined;
    this.original = undefined;
    this.materialized = {};
    this.deleteDefaults = [];
    this.configurations = {};
    this.associations = [];
  }
  reset() {
    if (this.original) this.load(this.original);
  }
  get payload(): MinderSave {
    return {
      expectedFingerprint: this.original?.fingerprint || "",
      ...(this.workspace?.policy.executionMode !==
      this.original?.policy.executionMode
        ? { executionMode: this.workspace?.policy.executionMode }
        : {}),
      points: (this.workspace?.nodes || [])
        .filter((n) => n.nodeType === "point")
        .map((n) => ({
          id: n.id,
          name: n.name,
          category: n.category,
          parentId: n.parentId || null,
          position: n.position,
          ...(this.materialized[n.category] === n.id
            ? { materializeDefault: n.category }
            : {}),
        })),
      deleteDefaults: [...this.deleteDefaults],
      configurations: cloneDeep(this.configurations),
      associations: this.associations.map((a) => cloneDeep(a.request)),
    };
  }
  get dirty() {
    if (!this.original) return false;
    const originalPoints = this.original.nodes
      .filter((n) => n.nodeType === "point")
      .map((n) => ({
        id: n.id,
        name: n.name,
        category: n.category,
        parentId: n.parentId || null,
        position: n.position,
      }));
    const ordered = (points: MinderSave["points"]) =>
      [...points].sort((a, b) => a.id.localeCompare(b.id));
    return (
      JSON.stringify(ordered(this.payload.points)) !==
        JSON.stringify(ordered(originalPoints)) ||
      this.deleteDefaults.length > 0 ||
      this.workspace?.policy.executionMode !==
        this.original.policy.executionMode ||
      Object.keys(this.configurations).length > 0 ||
      this.associations.length > 0
    );
  }
  association(category: MinderCategory, collectionId?: string | null) {
    return this.associations.find(
      (a) =>
        a.request.category === category &&
        (a.request.collectionId || null) === (collectionId || null),
    );
  }
  associationPreview(
    category: MinderCategory,
    collectionId?: string | null,
  ): MinderSave {
    const body = this.payload;
    body.associations = body.associations?.filter(
      (a) =>
        !(
          a.category === category &&
          (a.collectionId || null) === (collectionId || null)
        ),
    );
    return body;
  }
  associate(request: PlanAssociation, summary: CandidateSelectionPreview) {
    if (!this.workspace) throw new Error("测试规划尚未加载");
    if (
      request.collectionId &&
      !this.workspace.nodes.some(
        (n) =>
          n.id === request.collectionId &&
          n.nodeType === "point" &&
          n.category === request.category,
      )
    )
      throw new Error("关联测试集已变化，请重新选择");
    this.associations = this.associations.filter(
      (a) =>
        !(
          a.request.category === request.category &&
          (a.request.collectionId || null) === (request.collectionId || null)
        ),
    );
    this.associations.push({
      request: cloneDeep(request),
      summary: cloneDeep(summary),
    });
  }
  private remapAssociations(
    category: MinderCategory,
    from: string | null,
    to?: string,
  ) {
    this.associations = this.associations.filter((a) => {
      if (
        a.request.category === category &&
        (a.request.collectionId || null) === from
      ) {
        if (!to) return false;
        a.request.collectionId = to;
      }
      for (const [kind, field, suite] of [
        ["api", "apiCaseCollectionId", "syncApiSuiteId"],
        ["scenario", "apiScenarioCollectionId", "syncScenarioSuiteId"],
      ] as const) {
        if (kind !== category || a.request[field] !== (from || "default"))
          continue;
        a.request[field] = to;
        if (!to) {
          delete a.request[suite];
          if (a.summary.sync) a.summary.sync[kind].count = 0;
        }
      }
      return true;
    });
  }
  setExecutionMode(mode: "serial" | "parallel") {
    if (!this.workspace) return;
    this.workspace.policy.executionMode = mode;
    for (const category of ["api", "scenario"] as const) {
      const scope = `root:${category}`;
      const entry = this.workspace.executionCatalog.configurations[scope];
      if (entry && entry.revision === 0 && !this.configurations[scope]) {
        entry.config.executionMode = mode;
      }
    }
    this.recalculate();
  }
  private nameAvailable(
    name: string,
    category: MinderCategory,
    except?: string,
    materializing = false,
  ) {
    if (!name.trim() || name.trim().length > 255)
      throw new Error("测试集名称须为1到255字");
    if (
      !materializing &&
      name.trim() === "默认测试集" &&
      this.workspace?.entries[category].some((e) => !e.collectionId)
    )
      throw new Error("同一分类已存在默认测试集，请使用其他名称");
    if (
      this.workspace?.nodes.some(
        (n) =>
          n.nodeType === "point" &&
          n.category === category &&
          n.id !== except &&
          n.name === name.trim(),
      )
    )
      throw new Error("同一分类的测试集名称不能重复");
  }
  rename(id: string, name: string) {
    const node = this.workspace?.nodes.find(
      (n) => n.id === id && n.nodeType === "point",
    );
    if (!node) throw new Error("测试集不存在");
    this.nameAvailable(name, node.category, id);
    node.name = name.trim();
  }
  isNew(id: string) {
    return !this.original?.nodes.some((n) => n.id === id);
  }
  validate() {
    for (const node of this.workspace?.nodes.filter(
      (n) => n.nodeType === "point",
    ) || []) {
      const original = this.original?.nodes.find((n) => n.id === node.id);
      if (
        !original ||
        original.name !== node.name ||
        original.position !== node.position
      )
        this.nameAvailable(
          node.name,
          node.category,
          node.id,
          this.materialized[node.category] === node.id,
        );
    }
  }
  insert(category: MinderCategory, afterId?: string): PlanNode {
    // 默认临时文本可以与既有集同名，退出编辑及整体保存时再校验。
    const point = this.create(category, "默认测试集", afterId);
    if (category !== "functional") {
      const parent =
        this.workspace!.executionCatalog.configurations[`root:${category}`];
      if (parent)
        this.configure(`node:${category}:${point.id}`, {
          ...parent.effectiveConfig,
          extended: parent.config.extended,
        });
    }
    return point;
  }
  add(
    category: MinderCategory,
    name: string,
    afterId?: string,
    materializing = false,
  ): PlanNode {
    if (!this.workspace) throw new Error("测试规划尚未加载");
    this.nameAvailable(name, category, undefined, materializing);
    return this.create(category, name, afterId);
  }
  private create(
    category: MinderCategory,
    name: string,
    afterId?: string,
  ): PlanNode {
    if (!this.workspace) throw new Error("测试规划尚未加载");
    const siblings = this.workspace.nodes
      .filter(
        (n) => n.nodeType === "point" && n.category === category && !n.parentId,
      )
      .sort((a, b) => a.position - b.position);
    const after = afterId
      ? siblings.findIndex((n) => n.id === afterId)
      : siblings.length - 1;
    const point: PlanNode = {
      id: crypto.randomUUID(),
      planId: this.workspace.nodes[0]?.planId || "",
      parentId: null,
      name: name.trim(),
      nodeType: "point",
      category,
      position: 0,
      config: {},
      effectiveConfig: {},
    };
    siblings.splice(after + 1, 0, point);
    siblings.forEach((n, position) => {
      n.position = position;
    });
    this.workspace.nodes.push(point);
    this.recalculate();
    return point;
  }
  materializeDefault(category: MinderCategory, name = "默认测试集"): PlanNode {
    if (!this.workspace) throw new Error("测试规划尚未加载");
    const existing = this.materialized[category];
    if (existing) return this.workspace.nodes.find((n) => n.id === existing)!;
    const point = this.add(category, name, undefined, true);
    this.materialized[category] = point.id;
    this.remapAssociations(category, null, point.id);
    const siblings = this.workspace.nodes
      .filter(
        (n) => n.nodeType === "point" && n.category === category && !n.parentId,
      )
      .sort((a, b) => a.position - b.position);
    this.reorder(category, null, [
      point.id,
      ...siblings.filter((n) => n.id !== point.id).map((n) => n.id),
    ]);
    for (const entry of this.workspace.entries[category])
      if (!entry.collectionId) entry.collectionId = point.id;
    for (const node of this.workspace.nodes)
      if (
        node.nodeType !== "point" &&
        node.category === category &&
        !node.parentId
      )
        node.parentId = point.id;
    const catalog = this.workspace.executionCatalog.configurations,
      oldScope = `default:${category}`,
      newScope = `node:${category}:${point.id}`;
    if (category !== "functional" && catalog[oldScope])
      catalog[newScope] = { ...cloneDeep(catalog[oldScope]), scope: newScope };
    if (this.configurations[oldScope]) {
      this.configurations[newScope] = this.configurations[oldScope];
      delete this.configurations[oldScope];
    }
    this.recalculate();
    return point;
  }
  removeMany(targets: MinderDeletionTarget[]) {
    if (!this.workspace) throw new Error("测试规划尚未加载");
    // 先验证整个范围，任何过期或旧公共集投影都不部分删除。
    for (const target of targets) {
      if (target.nodeId) {
        const point = this.workspace.nodes.find((n) => n.id === target.nodeId);
        if (
          !point ||
          point.nodeType !== "point" ||
          point.category !== target.category
        )
          throw new Error("选中的测试集已变化，请重新选择");
      }
    }
    for (const target of targets) {
      if (
        target.nodeId &&
        this.workspace.nodes.some((n) => n.id === target.nodeId)
      )
        this.remove(target.nodeId);
      else if (!target.nodeId) this.removeDefault(target.category);
    }
    this.recalculate();
  }
  remove(id: string) {
    if (!this.workspace) return;
    const removed = new Set([id]);
    let size = 0;
    while (size !== removed.size) {
      size = removed.size;
      this.workspace.nodes.forEach((n) => {
        if (n.parentId && removed.has(n.parentId)) removed.add(n.id);
      });
    }
    for (const node of this.workspace.nodes.filter(
      (n) => removed.has(n.id) && n.nodeType === "point",
    ))
      this.remapAssociations(node.category, node.id);
    this.workspace.nodes = this.workspace.nodes.filter(
      (n) => !removed.has(n.id),
    );
    for (const category of ["functional", "api", "scenario"] as const) {
      this.workspace.entries[category] = this.workspace.entries[
        category
      ].filter((e) => !e.collectionId || !removed.has(e.collectionId));
      if (
        this.materialized[category] &&
        removed.has(this.materialized[category]!)
      ) {
        delete this.materialized[category];
        this.deleteDefaults.push(category);
      }
    }
    for (const scope of Object.keys(this.configurations))
      if (removed.has(scope.split(":")[2])) delete this.configurations[scope];
    this.recalculate();
  }
  removeDefault(category: MinderCategory) {
    if (!this.workspace) return;
    this.remapAssociations(category, null);
    this.workspace.entries[category] = this.workspace.entries[category].filter(
      (e) => !!e.collectionId,
    );
    this.workspace.nodes = this.workspace.nodes.filter(
      (n) =>
        !(n.nodeType !== "point" && n.category === category && !n.parentId),
    );
    if (!this.deleteDefaults.includes(category))
      this.deleteDefaults.push(category);
    delete this.configurations[`default:${category}`];
  }
  reorder(category: MinderCategory, parentId: string | null, ids: string[]) {
    if (!this.workspace) return;
    const siblings = this.workspace.nodes.filter(
      (n) =>
        n.nodeType === "point" &&
        n.category === category &&
        (n.parentId || null) === parentId,
    );
    if (
      new Set(ids).size !== ids.length ||
      ids.length !== siblings.length ||
      ids.some((id) => !siblings.some((n) => n.id === id))
    )
      throw new Error("只能排序当前分类中同一父级的测试集");
    ids.forEach((id, position) => {
      siblings.find((n) => n.id === id)!.position = position;
    });
  }
  configure(scope: string, config: ExecutionConfig) {
    if (!this.workspace) return;
    const entry = this.workspace.executionCatalog.configurations[scope];
    if (!entry) throw new Error("执行配置节点不存在");
    this.configurations[scope] = {
      config: cloneDeep(config),
      expectedRevision: entry.revision,
    };
    entry.config = cloneDeep(config);
    this.recalculate();
  }
  recalculate() {
    if (!this.workspace) return;
    const catalog = this.workspace.executionCatalog.configurations;
    for (const node of this.workspace.nodes.filter(
      (n) => n.nodeType === "point",
    ))
      for (const category of ["api", "scenario"] as const) {
        const scope = `node:${category}:${node.id}`,
          parent =
            catalog[
              node.parentId
                ? `node:${category}:${node.parentId}`
                : `root:${category}`
            ];
        if (!catalog[scope] && parent)
          catalog[scope] = {
            scope,
            revision: 0,
            config: { ...cloneDeep(parent.effectiveConfig), extended: true },
            effectiveConfig: {
              ...cloneDeep(parent.effectiveConfig),
              extended: true,
            },
          };
      }
    const resolve = (
      scope: string,
      seen = new Set<string>(),
    ): ExecutionConfig | undefined => {
      const entry = catalog[scope];
      if (!entry || seen.has(scope)) return entry?.effectiveConfig;
      seen.add(scope);
      if (!entry.config.extended || scope.startsWith("root:"))
        return cloneDeep(entry.config);
      const [, category, id] = scope.split(":"),
        node = this.workspace!.nodes.find((n) => n.id === id);
      const inherited = resolve(
        node?.parentId
          ? `node:${category}:${node.parentId}`
          : `root:${category}`,
        seen,
      );
      return inherited
        ? { ...inherited, extended: true }
        : cloneDeep(entry.config);
    };
    for (const scope of Object.keys(catalog))
      catalog[scope].effectiveConfig = resolve(scope)!;
  }
}
