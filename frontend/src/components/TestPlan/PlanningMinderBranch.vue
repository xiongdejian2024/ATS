<template>
  <div class="minder-branch" :data-node-id="node.id">
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
        @reorder="(parent, ordered) => emit('reorder', parent, ordered)"
        ><template #menu="scope"><slot name="menu" v-bind="scope" /></template
      ></PlanningMinderBranch>
      <VueDraggable
        v-if="collections.length"
        class="collection-children"
        :model-value="collections"
        :group="{ name: node.id, pull: false, put: false }"
        :disabled="!canEdit || collections.some((child) => !sortable(child))"
        draggable=".minder-branch"
        handle=".branch-label > .minder-node"
        :animation="160"
        :force-fallback="true"
        :fallback-on-body="true"
        :fallback-tolerance="5"
        @update:model-value="(ordered) => emit('reorder', node, ordered)"
      >
        <PlanningMinderBranch
          v-for="child in collections"
          :key="child.id"
          class="sortable-collection"
          :node="child"
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
import type { PlanNode } from "@/api/planTree";
defineSlots<{ menu(props: { node: PlanMinderNode }): unknown }>();
const props = defineProps<{
  node: PlanMinderNode;
  points: PlanNode[];
  selectedIds: ReadonlySet<string>;
  collapsed: ReadonlySet<string>;
  canEdit: boolean;
  editingId?: string;
  editName?: string;
}>();
const emit = defineEmits<{
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
.branch-label {
  display: flex;
  align-items: center;
  position: relative;
  flex-shrink: 0;
}
.minder-node {
  border: 1px solid #d8c5e0;
  border-radius: 4px;
  background: #faf7fc;
  color: #333;
  padding: 8px 12px;
  font-size: 12px;
  max-width: 200px;
  overflow-wrap: anywhere;
  cursor: pointer;
  text-align: left;
}
.minder-node.selected {
  outline: 2px solid #811fa3;
}
.minder-name-editor {
  box-sizing: border-box;
  width: 200px;
  padding: 8px 12px;
  border: 2px solid #811fa3;
  border-radius: 4px;
  font-size: 12px;
}
.minder-node.root {
  color: white;
  background: #811fa3;
  font-weight: 600;
}
.fold-toggle {
  margin-left: 6px;
  border: 1px solid #d8c5e0;
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
  border-left: 1px solid #c5b1d0;
  position: relative;
  padding-left: 24px;
}
.branch-children::before {
  content: "";
  position: absolute;
  left: -48px;
  top: 50%;
  width: 48px;
  border-top: 1px solid #c5b1d0;
}
.branch-children > .minder-branch::before,
.collection-children > .minder-branch::before {
  content: "";
  position: absolute;
  left: -24px;
  top: 50%;
  width: 24px;
  border-top: 1px solid #c5b1d0;
}
.sortable-collection > .branch-label > .minder-node {
  cursor: grab;
}
.sortable-ghost {
  opacity: 0.35;
}
</style>
