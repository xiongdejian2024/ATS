<template>
  <a-drawer
    :open="open"
    title="表格设置"
    width="min(480px,100vw)"
    :footer="false"
    class="table-display-settings"
    @close="closeDrawer"
  >
    <a-alert
      v-if="error"
      :message="error"
      type="error"
      show-icon
      class="settings-error"
    />
    <template v-if="showMode">
      <div class="setting-title">模式设置</div>
      <a-radio-group value="drawer" class="detail-mode" button-style="solid">
        <a-radio-button value="drawer">抽屉</a-radio-button>
      </a-radio-group>
    </template>
    <div class="setting-title">每页显示数量</div>
    <a-radio-group
      :value="pageSize"
      class="page-size-options"
      button-style="solid"
      @change="emit('pageSizeChange', $event.target.value)"
    >
      <a-radio-button v-for="size in pageSizes" :key="size" :value="size">{{
        size
      }}</a-radio-button>
    </a-radio-group>
    <div v-if="showDescendants !== false" class="subdirectory-setting">
      <a-switch
        :checked="includeDescendants"
        size="small"
        aria-label="显示子模块资源"
        @change="
          (value: boolean | string | number) =>
            emit('descendantsChange', Boolean(value))
        "
      />
      <span>显示子模块资源</span>
      <a-tooltip
        placement="topRight"
        title="开启：显示模块及子模块下的资源；关闭：只显示所选模块下的资源。"
        ><QuestionCircleOutlined
      /></a-tooltip>
    </div>
    <a-divider />
    <div class="header-setting">
      <strong>表头设置</strong>
      <a-button :disabled="!changed" type="text" @click="resetDraft"
        >撤销修改</a-button
      >
    </div>
    <div
      v-for="column in fixed"
      :key="column.key"
      class="column-setting fixed-column"
    >
      <span>{{ title(column.key) }}</span
      ><a-switch
        :checked="true"
        size="small"
        disabled
        :aria-label="`显示${title(column.key)}`"
      />
    </div>
    <a-divider class="fixed-divider">以上属性不可排序</a-divider>
    <VueDraggable
      v-model="movable"
      handle=".sort-handle"
      ghost-class="column-ghost"
      :animation="150"
    >
      <div
        v-for="column in movable"
        :key="column.key"
        class="column-setting"
        :data-column-key="column.key"
      >
        <span class="column-label"
          ><HolderOutlined
            class="sort-handle"
            :aria-label="`拖动${title(column.key)}`"
          /><span>{{ title(column.key) }}</span></span
        >
        <a-switch
          v-model:checked="column.visible"
          size="small"
          :aria-label="`显示${title(column.key)}`"
        />
      </div>
    </VueDraggable>
  </a-drawer>
</template>
<script setup lang="ts">
import { ref, computed, watch } from "vue";
import { VueDraggable } from "vue-draggable-plus";
import { HolderOutlined, QuestionCircleOutlined } from "@ant-design/icons-vue";
import {
  pageSizes,
  normalizeDisplay,
  type DisplayColumn,
  type ColumnVisibility,
} from "./tableDisplay";
const props = defineProps<{
  open: boolean;
  definitions: DisplayColumn[];
  columns: ColumnVisibility[];
  pageSize: number;
  includeDescendants: boolean;
  error?: string;
  showMode?: boolean;
  showDescendants?: boolean;
}>();
const emit = defineEmits<{
  close: [columns: ColumnVisibility[]];
  pageSizeChange: [size: number];
  descendantsChange: [value: boolean];
}>();
const fixed = ref<ColumnVisibility[]>([]),
  movable = ref<ColumnVisibility[]>([]),
  original = ref("");
let draftCache: ColumnVisibility[] = [],
  baselineCache: ColumnVisibility[] = [];
const title = (key: string) =>
  props.definitions.find((column) => column.key === key)?.title || key;
const changed = computed(
  () => JSON.stringify([...fixed.value, ...movable.value]) !== original.value,
);
function resetDraft() {
  draftCache = props.columns.map((c) => ({ ...c }));
  baselineCache = props.columns.map((c) => ({ ...c }));
  const locked = new Set(
    props.definitions
      .filter((column) => column.required)
      .map((column) => column.key),
  );
  fixed.value = props.columns
    .filter((column) => locked.has(column.key))
    .map((column) => ({ ...column }));
  movable.value = props.columns
    .filter((column) => !locked.has(column.key))
    .map((column) => ({ ...column }));
  original.value = JSON.stringify([...fixed.value, ...movable.value]);
}
function updateDraftCache() {
  const live = [...fixed.value, ...movable.value].map((c) => ({ ...c }));
  const cachedKeys = new Set(draftCache.map((c) => c.key)),
    liveKeys = new Set(live.map((c) => c.key));
  const reordered = live.filter((c) => cachedKeys.has(c.key));
  draftCache = draftCache.map((c) =>
    liveKeys.has(c.key) ? reordered.shift()! : c,
  );
  for (const c of [...live, ...props.columns])
    if (!cachedKeys.has(c.key)) {
      draftCache.push({ ...c });
      cachedKeys.add(c.key);
      baselineCache.push({ ...c });
    }
}
function closeDrawer() {
  updateDraftCache();
  emit(
    "close",
    draftCache.map((c) => ({ ...c })),
  );
}
watch(
  () => props.open,
  (open) => {
    if (open) resetDraft();
  },
  { immediate: true },
);
watch(
  () => props.definitions,
  () => {
    if (!props.open) return;
    // 同一次打开中保留暂时消失字段的草稿、顺序和基线；重开从新作用域重置。
    updateDraftCache();
    const draft = normalizeDisplay(
      { columns: draftCache },
      props.definitions,
    ).columns;
    original.value = JSON.stringify(
      normalizeDisplay({ columns: baselineCache }, props.definitions).columns,
    );
    const locked = new Set(
      props.definitions.filter((c) => c.required).map((c) => c.key),
    );
    fixed.value = draft.filter((c) => locked.has(c.key));
    movable.value = draft.filter((c) => !locked.has(c.key));
  },
);
</script>
<style scoped>
.setting-title,
.header-setting {
  font-weight: 500;
  color: #555;
}
.page-size-options {
  display: flex;
  width: 289px;
  max-width: 100%;
  margin-top: 8px;
}
.detail-mode {
  margin: 8px 0 16px;
}
.page-size-options :deep(.ant-radio-button-wrapper) {
  flex: 1;
  text-align: center;
  padding: 0;
}
.subdirectory-setting {
  display: flex;
  align-items: center;
  gap: 6px;
  margin-top: 24px;
  color: #555;
}
.header-setting,
.column-setting {
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.column-setting {
  padding: 8px 12px;
  margin: 4px 0;
  min-height: 38px;
}
.fixed-column {
  padding-left: 36px;
}
.column-setting:hover {
  background: #f5f5f5;
  border-radius: 6px;
}
.column-label {
  display: flex;
  align-items: center;
  gap: 8px;
  min-width: 0;
}
.sort-handle {
  cursor: move;
  color: #999;
  font-size: 16px;
}
.fixed-divider :deep(.ant-divider-inner-text) {
  font-size: 12px;
  font-weight: 400;
  color: #888;
}
.column-ghost {
  border: 1px dashed var(--primary-color);
  background: var(--ms-primary-soft);
}
.settings-error {
  margin-bottom: 12px;
}
</style>
