import {
  nextTick,
  onScopeDispose,
  ref,
  shallowRef,
  watch,
  type Ref,
} from "vue";
export interface MinderLayoutNode {
  id: string;
  name: string;
  children?: MinderLayoutNode[];
}
import type { MinderBox, MinderGeometry, MinderMode } from "./planMinderView";

interface EngineNode {
  getData(key: string): string;
  getContentBox(): MinderBox;
  getLayoutBox(): MinderBox;
  getConnection(): { getPathData(): string } | undefined;
  traverse(visitor: (node: EngineNode) => void): void;
}
interface MinderEngine {
  importJson(value: unknown): void;
  getRoot(): EngineNode;
  layout(): void;
  destroy(): void;
}
interface EngineGlobal extends Window {
  kity: {
    Box: new (x: number, y: number, width: number, height: number) => MinderBox;
  };
  kityminder: {
    Minder: new (options: Record<string, unknown>) => MinderEngine;
  };
}
let loader: Promise<void> | undefined;
async function loadEngine() {
  if (!loader)
    loader = (async () => {
      await import("@7polo/kity/dist/kity.js");
      await import("@7polo/kityminder-core");
    })().catch((error) => {
      loader = undefined;
      throw error;
    });
  await loader;
}
/** 只借用MS固定版本的布局和连接线算法，编辑、选中和保存仍由现有组件负责。 */
export function useMinderLayout(
  stage: Ref<HTMLElement | undefined>,
  tree: Ref<MinderLayoutNode>,
  collapsed: Ref<ReadonlySet<string>>,
  mode: Ref<MinderMode>,
  editingId: Ref<string | undefined>,
) {
  const geometry = shallowRef<MinderGeometry>(),
    failed = ref(false);
  let engine: MinderEngine | undefined,
    host: HTMLElement | undefined,
    disposed = false,
    sequence = 0;
  async function refresh() {
    const request = ++sequence;
    try {
      await nextTick();
      if (!stage.value || disposed) return;
      await loadEngine();
      if (disposed || request !== sequence) return;
      const globals = window as unknown as EngineGlobal;
      if (!engine) {
        host = document.createElement("div");
        host.setAttribute("aria-hidden", "true");
        host.style.cssText =
          "position:fixed;left:-10000px;top:0;width:1000px;height:1000px;pointer-events:none;opacity:0";
        document.body.append(host);
        engine = new globals.kityminder.Minder({
          renderTo: host,
          enableKeyReceiver: false,
          enableAnimation: false,
          layoutAnimationDuration: 0,
          defaultTheme: "fresh-purple",
        });
      }
      const sizes = new Map<string, MinderBox>();
      for (const label of stage.value.querySelectorAll<HTMLElement>(
        ".branch-label",
      )) {
        const body = label.querySelector<HTMLElement>(
          ".minder-node, .minder-name-editor",
        );
        const id = label.closest<HTMLElement>("[data-node-id]")?.dataset.nodeId;
        if (id && body)
          sizes.set(id, {
            x: 0,
            y: 0,
            width: body.offsetWidth,
            height: body.offsetHeight,
          });
      }
      function serialize(node: MinderLayoutNode): unknown {
        return {
          data: { id: node.id, text: node.name },
          children: collapsed.value.has(node.id)
            ? []
            : node.children?.map(serialize) || [],
        };
      }
      engine.importJson({
        root: serialize(tree.value),
        template: mode.value,
        theme: "fresh-purple",
      });
      engine.getRoot().traverse((node) => {
        const size = sizes.get(node.getData("id"));
        // getContentBox是锁定引擎的公共测量入口，用DOM实际尺寸替代隐藏SVG字体测量。
        if (size)
          node.getContentBox = () =>
            new globals.kity.Box(
              -size.width / 2,
              -size.height / 2,
              size.width,
              size.height,
            );
      });
      engine.layout();
      const boxes: Record<string, MinderBox> = {},
        paths: string[] = [];
      engine.getRoot().traverse((node) => {
        boxes[node.getData("id")] = node.getLayoutBox();
        const path = node.getConnection()?.getPathData();
        if (path) paths.push(path);
      });
      const all = Object.values(boxes),
        minX = Math.min(...all.map((box) => box.x)),
        minY = Math.min(...all.map((box) => box.y));
      const offset = { x: 40 - minX, y: 40 - minY };
      geometry.value = {
        width: Math.max(...all.map((box) => box.x + box.width)) - minX + 80,
        height: Math.max(...all.map((box) => box.y + box.height)) - minY + 80,
        nodes: Object.fromEntries(
          Object.entries(boxes).map(([id, box]) => [
            id,
            {
              x: box.x + offset.x,
              y: box.y + offset.y,
              width: box.width,
              height: box.height,
            },
          ]),
        ),
        paths,
        offset,
      };
      failed.value = false;
    } catch (error) {
      console.error("计算测试规划脑图布局失败", error);
      failed.value = true;
    }
  }
  watch([stage, tree, collapsed, mode, editingId], refresh, {
    immediate: true,
    flush: "post",
  });
  onScopeDispose(() => {
    disposed = true;
    sequence++;
    try {
      engine?.destroy();
    } catch (error) {
      console.error("释放脑图布局引擎失败", error);
    }
    host?.remove();
  });
  return { geometry, failed, refresh };
}
