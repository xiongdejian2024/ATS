<template>
  <div class="minder-branch" :style="position" :data-node-id="node.id">
    <div class="branch-label">
      <button
        class="minder-node"
        :class="{ selected: selected.has(node.id), root: node.kind === 'root' }"
        :aria-label="node.name"
        :aria-pressed="selected.has(node.id)"
        @click="emit('select', node, $event)"
      >
        <span v-if="node.caseCode" class="case-code">{{ node.caseCode }}</span>
        <span
          v-if="node.priority"
          class="case-priority"
          :class="node.priority"
          :aria-label="`优先级 ${node.priority}`"
          >{{ node.priority }}</span
        >
        <span v-if="node.result" class="status" :class="node.result">{{
          resultLabel(node)
        }}</span>
        <span v-if="functionalMinderTags[node.kind]" class="node-tag">{{
          functionalMinderTags[node.kind]
        }}</span>
        <span
          v-if="node.bugCount"
          class="case-defects"
          :aria-label="`${node.bugCount} 个关联缺陷`"
          :title="`${node.bugCount} 个关联缺陷`"
          >缺陷 {{ node.bugCount }}</span
        >
        <span class="node-text">{{ node.name }}</span
        ><span
          v-if="node.kind === 'folder' || node.kind === 'root'"
          class="node-count"
          >{{ node.count }}</span
        >
      </button>
      <button
        v-if="node.kind === 'folder' || node.children?.length"
        class="fold-toggle"
        :aria-label="`${collapsed.has(node.id) ? '展开' : '收起'}${node.name}`"
        @click="emit('toggle', node)"
      >
        {{ collapsed.has(node.id) ? "+" : "−" }}
      </button>
      <slot
        v-if="selected.size === 1 && selected.has(node.id)"
        name="menu"
        :node="node"
      />
    </div>
    <div v-if="!collapsed.has(node.id)">
      <FunctionalMinderBranch
        v-for="child in node.children || []"
        :key="child.id"
        :node="child"
        :geometry="geometry"
        :parent-origin="box"
        :selected="selected"
        :collapsed="collapsed"
        @select="(node, event) => emit('select', node, event)"
        @toggle="emit('toggle', $event)"
      >
        <template #menu="scope"><slot name="menu" v-bind="scope" /></template>
      </FunctionalMinderBranch>
    </div>
  </div>
</template>
<script setup lang="ts">
import { computed } from "vue";
import {
  functionalMinderTags,
  resultLabel,
  type FunctionalMinderNode,
} from "./functionalMinder";
import type { MinderGeometry, MinderBox } from "./planMinderView";
const props = defineProps<{
  node: FunctionalMinderNode;
  geometry?: MinderGeometry;
  parentOrigin?: MinderBox;
  selected: ReadonlySet<string>;
  collapsed: ReadonlySet<string>;
}>();
const emit = defineEmits<{
  select: [node: FunctionalMinderNode, event: MouseEvent];
  toggle: [node: FunctionalMinderNode];
}>();
defineSlots<{ menu(props: { node: FunctionalMinderNode }): unknown }>();
const box = computed(() => props.geometry?.nodes[props.node.id]);
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
</script>
<style scoped>
.minder-branch {
  position: absolute;
}
.branch-label {
  position: relative;
  display: flex;
  align-items: center;
  gap: 6px;
  white-space: nowrap;
  width: max-content;
}
.minder-node {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 7px;
  border: 1px solid #bfbfbf;
  border-radius: 4px;
  background: #fff;
  padding: 8px 12px;
  cursor: pointer;
  max-width: 360px;
  min-height: 36px;
  font-size: 13px;
  white-space: normal;
  text-align: left;
  overflow-wrap: anywhere;
}
.minder-node.root {
  background: #811fa3;
  color: #fff;
  border-color: #811fa3;
}
.minder-node.selected {
  outline: 2px solid #c689de;
  background: #f9f0ff;
  color: #1d2129;
}
.case-code {
  font-size: 11px;
  color: #86909c;
  overflow-wrap: anywhere;
}
.case-priority {
  font-size: 11px;
  padding: 1px 4px;
  border-radius: 3px;
  background: #f2f3f5;
  white-space: nowrap;
}
.case-priority.P0 {
  color: #f53f3f;
  background: #ffece8;
}
.case-priority.P1 {
  color: #ff7d00;
  background: #fff7e8;
}
.case-defects {
  color: #f53f3f;
  font-size: 11px;
  white-space: nowrap;
}
.node-text {
  max-width: 230px;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
.node-tag {
  font-size: 11px;
  color: #86909c;
  white-space: nowrap;
}
.node-count {
  color: #86909c;
}
.fold-toggle {
  border: 1px solid #bfbfbf;
  background: #fff;
  border-radius: 50%;
  width: 20px;
  height: 20px;
  line-height: 16px;
  cursor: pointer;
  position: absolute;
  right: -24px;
}
.status {
  font-size: 11px;
  padding: 1px 5px;
  border-radius: 3px;
  white-space: nowrap;
  background: #f2f3f5;
  color: #86909c;
}
.passed {
  background: #e8ffea;
  color: #00b42a;
}
.failed,
.error {
  background: #ffece8;
  color: #f53f3f;
}
.blocked {
  background: #fff7e8;
  color: #ff7d00;
}
</style>
