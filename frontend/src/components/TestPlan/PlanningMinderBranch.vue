<template>
  <div
    class="minder-branch"
    :class="{ 'laid-out': !!box }"
    :style="position"
    :data-node-id="node.id"
  >
    <div class="branch-label">
      <button
        v-if="editingId !== node.id"
        type="button"
        class="minder-node"
        :class="{
          selected: selectedIds.has(node.id),
          root: node.kind === 'root',
        }"
        :aria-label="node.name"
        :aria-pressed="selectedIds.has(node.id)"
        @pointerdown="
          ($event.ctrlKey || $event.metaKey) && $event.stopPropagation()
        "
        @click="emit('select', node.id, $event)"
        @dblclick="emit('edit', node.id)"
      >
        <span v-if="node.executionMode">{{
          node.executionMode === "parallel" ? "并行 · " : "串行 · "
        }}</span
        >{{ node.name }}
      </button>
      <input
        v-else
        v-focus-name
        class="minder-name-editor"
        aria-label="编辑测试集名称"
        :value="editName"
        maxlength="255"
        @input="emit('editName', ($event.target as HTMLInputElement).value)"
        @pointerdown.stop
        @keydown.stop
        @keydown.enter.prevent="emit('rename')"
        @keydown.esc.prevent="emit('cancelEdit')"
        @blur="emit('rename')"
      />
      <button
        v-if="hasChildren"
        type="button"
        class="fold-toggle"
        :aria-label="
          collapsed.has(node.id) ? `展开${node.name}` : `收起${node.name}`
        "
        @click="emit('toggle', node.id)"
      >
        {{ collapsed.has(node.id) ? "+" : "−" }}
      </button>
      <slot
        v-if="
          selectedIds.size === 1 &&
          selectedIds.has(node.id) &&
          editingId !== node.id
        "
        name="menu"
        :node="node"
      />
    </div>
    <div v-if="hasChildren && !collapsed.has(node.id)" class="branch-children">
      <PlanningMinderBranch
        v-for="child in fixedChildren"
        :key="child.id"
        :node="child"
        :geometry="geometry"
        :parent-origin="box"
        :points="points"
        :selected-ids="selectedIds"
        :collapsed="collapsed"
        :can-edit="canEdit"
        :editing-id="editingId"
        :edit-name="editName"
        @edit="(id) => emit('edit', id)"
        @edit-name="(name) => emit('editName', name)"
        @rename="emit('rename')"
        @cancel-edit="emit('cancelEdit')"
        @select="(id, event) => emit('select', id, event)"
        @toggle="(id) => emit('toggle', id)"
        @drag-choose="(event) => emit('dragChoose', event)"
        @drag-start="emit('dragStart')"
        @drag-end="emit('dragEnd')"
        @reorder="(parent, ordered) => emit('reorder', parent, ordered)"
        ><template #menu="scope"><slot name="menu" v-bind="scope" /></template
      ></PlanningMinderBranch>
      <VueDraggable
        v-if="collections.length"
        class="collection-children"
        :style="collectionPosition"
        :model-value="collections"
        :group="{ name: node.id, pull: false, put: false }"
        :disabled="!canEdit || collections.some((child) => !sortable(child))"
        draggable=".minder-branch"
        handle=".branch-label > .minder-node"
        direction="vertical"
        :animation="160"
        :force-fallback="true"
        :fallback-on-body="true"
        :fallback-tolerance="5"
        @choose="emit('dragChoose', $event)"
        @start="emit('dragStart')"
        @end="emit('dragEnd')"
        @update:model-value="(ordered) => emit('reorder', node, ordered)"
      >
        <PlanningMinderBranch
          v-for="child in collections"
          :key="child.id"
          class="sortable-collection"
          :node="child"
          :geometry="geometry"
          :parent-origin="collectionBox || box"
          :points="points"
          :selected-ids="selectedIds"
          :collapsed="collapsed"
          :can-edit="canEdit"
          :editing-id="editingId"
          :edit-name="editName"
          @edit="(id) => emit('edit', id)"
          @edit-name="(name) => emit('editName', name)"
          @rename="emit('rename')"
          @cancel-edit="emit('cancelEdit')"
          @select="(id, event) => emit('select', id, event)"
          @toggle="(id) => emit('toggle', id)"
          @drag-choose="(event) => emit('dragChoose', event)"
          @drag-start="emit('dragStart')"
          @drag-end="emit('dragEnd')"
          @reorder="(parent, ordered) => emit('reorder', parent, ordered)"
          ><template #menu="scope"><slot name="menu" v-bind="scope" /></template
        ></PlanningMinderBranch>
      </VueDraggable>
    </div>
  </div>
</template>
<script setup lang="ts">
import { computed } from "vue";
import { VueDraggable } from "vue-draggable-plus";
import type { PlanMinderNode } from "./planMinderTree";
import type { MinderDragEvent } from "./useMinderDragPreview";
import type { MinderBox, MinderGeometry } from "./planMinderView";
import type { PlanNode } from "@/api/planTree";
defineSlots<{ menu(props: { node: PlanMinderNode }): unknown }>();
const props = defineProps<{
  node: PlanMinderNode;
  geometry?: MinderGeometry;
  parentOrigin?: MinderBox;
  points: PlanNode[];
  selectedIds: ReadonlySet<string>;
  collapsed: ReadonlySet<string>;
  canEdit: boolean;
  editingId?: string;
  editName?: string;
}>();
const emit = defineEmits<{
  dragChoose: [event: MinderDragEvent];
  dragStart: [];
  dragEnd: [];
  select: [id: string, event: MouseEvent];
  toggle: [id: string];
  reorder: [parent: PlanMinderNode, ordered: PlanMinderNode[]];
  edit: [id: string];
  editName: [name: string];
  rename: [];
  cancelEdit: [];
}>();
const vFocusName = {
  mounted(element: HTMLInputElement) {
    element.focus();
    element.select();
  },
};
const fixedChildren = computed(() =>
  (props.node.children || []).filter((child) => child.kind !== "collection"),
);
const collections = computed(() =>
  (props.node.children || []).filter((child) => child.kind === "collection"),
);
const box = computed(() => props.geometry?.nodes[props.node.id]);
// Sortable需要真实容器盒；display:contents会使父容器为零尺寸，无法判断拖入。
const collectionBox = computed(() => {
  if (!props.geometry) return undefined;
  const boxes: MinderBox[] = [];
  function visit(node: PlanMinderNode) {
    const current = props.geometry?.nodes[node.id];
    if (current) boxes.push(current);
    if (!props.collapsed.has(node.id)) node.children?.forEach(visit);
  }
  collections.value.forEach(visit);
  if (!boxes.length) return undefined;
  const x = Math.min(...boxes.map((item) => item.x));
  const y = Math.min(...boxes.map((item) => item.y));
  return {
    x,
    y,
    width: Math.max(...boxes.map((item) => item.x + item.width)) - x,
    height: Math.max(...boxes.map((item) => item.y + item.height)) - y,
  };
});
const collectionPosition = computed(() =>
  collectionBox.value && box.value
    ? {
        left: `${collectionBox.value.x - box.value.x}px`,
        top: `${collectionBox.value.y - box.value.y}px`,
        width: `${collectionBox.value.width}px`,
        height: `${collectionBox.value.height}px`,
      }
    : undefined,
);
const position = computed(() =>
  box.value
    ? {
        left: `${box.value.x - (props.parentOrigin?.x || 0)}px`,
        top: `${box.value.y - (props.parentOrigin?.y || 0)}px`,
        width: `${box.value.width}px`,
        height: `${box.value.height}px`,
      }
    : undefined,
);
const hasChildren = computed(() => !!props.node.children?.length);
function sortable(node: PlanMinderNode) {
  if (node.kind !== "collection") return false;
  const point = props.points.find((p) => p.id === node.nodeId);
  return !point || point.category === node.category;
}
</script>
<style scoped>
.minder-branch {
  display: flex;
  align-items: center;
  width: max-content;
  position: relative;
  padding: 10px 0;
}
.laid-out {
  position: absolute;
  padding: 0;
  display: block;
}
.laid-out > .branch-children {
  display: contents;
}
.laid-out > .branch-children > .collection-children {
  display: block;
  position: absolute;
}
.laid-out > .branch-children::before,
.laid-out > .branch-children > .minder-branch::before,
.laid-out > .branch-children > .collection-children > .minder-branch::before {
  display: none;
}
.branch-label {
  display: flex;
  align-items: center;
  position: relative;
  flex-shrink: 0;
}
.minder-node {
  flex-shrink: 0;
  width: max-content;
  border: 1px solid var(--primary-border);
  border-radius: 4px;
  background: var(--ms-primary-soft);
  color: #333;
  padding: 8px 12px;
  font-size: 12px;
  max-width: 200px;
  overflow-wrap: anywhere;
  cursor: pointer;
  text-align: left;
}
.minder-node.selected {
  outline: 2px solid var(--primary-color);
}
.minder-name-editor {
  box-sizing: border-box;
  width: 200px;
  padding: 8px 12px;
  border: 2px solid var(--primary-color);
  border-radius: 4px;
  font-size: 12px;
}
.minder-node.root {
  color: white;
  background: var(--primary-color);
  font-weight: 600;
}
.fold-toggle {
  margin-left: 6px;
  border: 1px solid var(--primary-border);
  border-radius: 50%;
  width: 20px;
  height: 20px;
  line-height: 16px;
  background: white;
  cursor: pointer;
}
.branch-children {
  display: flex;
  flex-direction: column;
  margin-left: 48px;
  border-left: 1px solid var(--primary-border);
  position: relative;
  padding-left: 24px;
}
.branch-children::before {
  content: "";
  position: absolute;
  left: -48px;
  top: 50%;
  width: 48px;
  border-top: 1px solid var(--primary-border);
}
.branch-children > .minder-branch::before,
.collection-children > .minder-branch::before {
  content: "";
  position: absolute;
  left: -24px;
  top: 50%;
  width: 24px;
  border-top: 1px solid var(--primary-border);
}
.sortable-collection > .branch-label > .minder-node {
  cursor: grab;
}
.sortable-ghost {
  opacity: 0.35;
}
</style>
