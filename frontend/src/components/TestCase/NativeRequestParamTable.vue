<template>
  <div class="request-param-editor">
    <div class="param-toolbar">
      <strong>{{ title }}</strong
      ><a-button :disabled="disabled" @click="batchOpen = true"
        >批量添加</a-button
      >
    </div>
    <div class="param-scroll">
      <table class="param-table" :class="{ typed }">
        <thead>
          <tr>
            <th aria-label="排序"></th>
            <th aria-label="启用"></th>
            <th>参数名</th>
            <th v-if="typed">类型</th>
            <th>参数值</th>
            <th v-if="typed">长度范围</th>
            <th v-if="typed">编码</th>
            <th>描述</th>
            <th></th>
          </tr>
        </thead>
        <VueDraggable
          v-model="rows"
          tag="tbody"
          handle=".param-drag"
          :disabled="disabled"
          :animation="150"
          @end="publish"
        >
          <tr
            v-for="(row, index) in rows"
            :key="row.uid"
            :data-param-row="index"
          >
            <td>
              <HolderOutlined
                v-if="index < rows.length - 1"
                class="param-drag"
                :aria-label="`${title}拖动参数${index + 1}`"
              />
            </td>
            <td>
              <a-checkbox
                v-model:checked="row.enable"
                :disabled="disabled"
                :aria-label="`${title}启用参数${index + 1}`"
                @change="publish"
              />
            </td>
            <td>
              <a-input
                v-model:value="row.key"
                :disabled="disabled"
                :maxlength="255"
                placeholder="参数名"
                :aria-label="`${title}参数名${index + 1}`"
                @change="publish"
              />
            </td>
            <td v-if="typed">
              <div class="param-type">
                <a-select
                  v-model:value="row.paramType"
                  :disabled="disabled"
                  :options="
                    paramTypes.map((value) => ({ value, label: value }))
                  "
                  :aria-label="`${title}类型${index + 1}`"
                  @change="publish"
                /><a-tooltip title="必填"
                  ><a-checkbox
                    v-model:checked="row.required"
                    :disabled="disabled"
                    :aria-label="`${title}必填${index + 1}`"
                    @change="publish"
                /></a-tooltip>
              </div>
            </td>
            <td>
              <a-input
                v-model:value="row.value"
                :disabled="disabled"
                :maxlength="20000"
                placeholder="参数值"
                :aria-label="`${title}参数值${index + 1}`"
                @change="publish"
              />
            </td>
            <td v-if="typed">
              <div class="param-range">
                <a-input-number
                  :value="row.lengthRange[0]"
                  :disabled="disabled"
                  :min="0"
                  :precision="0"
                  placeholder="最小值"
                  :aria-label="`${title}最小长度${index + 1}`"
                  @change="setRange(index, 0, $event)"
                /><span>~</span
                ><a-input-number
                  :value="row.lengthRange[1]"
                  :disabled="disabled"
                  :min="0"
                  :precision="0"
                  placeholder="最大值"
                  :aria-label="`${title}最大长度${index + 1}`"
                  @change="setRange(index, 1, $event)"
                />
              </div>
            </td>
            <td v-if="typed">
              <a-checkbox
                v-model:checked="row.encode"
                :disabled="disabled"
                :aria-label="`${title}编码${index + 1}`"
                @change="publish"
              />
            </td>
            <td>
              <a-input
                v-model:value="row.description"
                :disabled="disabled"
                :maxlength="1000"
                placeholder="描述"
                :aria-label="`${title}描述${index + 1}`"
                @change="publish"
              />
            </td>
            <td>
              <a-button
                v-if="index < rows.length - 1"
                type="text"
                :disabled="disabled"
                :aria-label="`${title}删除参数${index + 1}`"
                @click="remove(index)"
                ><DeleteOutlined
              /></a-button>
            </td>
          </tr>
        </VueDraggable>
      </table>
    </div>
    <a-alert v-if="error" :message="error" type="error" show-icon />
    <a-modal
      v-model:open="batchOpen"
      title="批量添加"
      :ok-button-props="{ disabled }"
      @ok="applyBatch"
    >
      <p>每行一个参数，使用参数名:参数值格式。</p>
      <a-textarea
        v-model:value="batch"
        :rows="8"
        :disabled="disabled"
        :aria-label="`${title}批量参数`"
      /><a-alert
        v-if="batchError"
        :message="batchError"
        type="error"
        show-icon
      />
    </a-modal>
  </div>
</template>
<script setup lang="ts">
import { ref, watch } from "vue";
import { VueDraggable } from "vue-draggable-plus";
import { HolderOutlined, DeleteOutlined } from "@ant-design/icons-vue";
import {
  blankParam,
  readParams,
  filledParams,
  batchParams,
  paramTypes,
  type RequestParam,
} from "./nativeRequestParams";
const props = defineProps<{
  modelValue: string;
  title: string;
  typed?: boolean;
  disabled?: boolean;
}>();
const emit = defineEmits<{ "update:modelValue": [value: string] }>();
type Row = RequestParam & { uid: number };
const rows = ref<Row[]>([]),
  error = ref(""),
  batchOpen = ref(false),
  batch = ref(""),
  batchError = ref("");
let identity = 0,
  output = "";
const row = (param: RequestParam): Row => ({ ...param, uid: ++identity });
watch(
  () => props.modelValue,
  (raw) => {
    if (raw === output) return;
    try {
      rows.value = [...readParams(raw).map(row), row(blankParam())];
      error.value = "";
    } catch (exception) {
      console.error("参数表加载失败，原草稿保留", exception);
      error.value = "参数内容无法载入，请修正高级配置";
    }
  },
  { immediate: true },
);
function publish() {
  if (props.disabled) return;
  const last = rows.value.at(-1);
  if (!last || last.key || last.value || last.description)
    rows.value.push(row(blankParam()));
  const data = filledParams(rows.value).map(({ uid, ...param }) => param);
  output = JSON.stringify(data);
  emit("update:modelValue", output);
}
function remove(index: number) {
  rows.value.splice(index, 1);
  publish();
}
function setRange(index: number, key: number, value: number | string | null) {
  const next = [...rows.value[index].lengthRange];
  next[key] = value === null || value === "" ? NaN : Number(value);
  rows.value[index].lengthRange = next.every(Number.isNaN) ? [] : next;
  publish();
}
function applyBatch() {
  if (props.disabled) return;
  try {
    rows.value = [
      ...batchParams(batch.value, !props.typed).map(row),
      row(blankParam()),
    ];
    publish();
    batchOpen.value = false;
    batch.value = "";
    batchError.value = "";
    console.info("请求参数批量添加已应用", {
      类别: props.title,
      数量: rows.value.length - 1,
    });
  } catch (exception) {
    console.error("请求参数批量添加失败，原参数保留", exception);
    batchError.value =
      exception instanceof Error ? exception.message : "批量参数无效";
  }
}
</script>
<style scoped>
.param-toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}
.param-scroll {
  overflow-x: auto;
}
.param-table {
  width: 100%;
  min-width: 700px;
  border-collapse: collapse;
  table-layout: fixed;
}
.param-table.typed {
  min-width: 1160px;
}
.param-table th {
  text-align: left;
  background: #f7f8fa;
  font-weight: 500;
  padding: 10px 8px;
}
.param-table td {
  padding: 6px 8px;
  border-bottom: 1px solid #e5e6eb;
}
.param-table th:first-child {
  width: 28px;
}
.param-table th:nth-child(2) {
  width: 32px;
}
.param-table th:last-child {
  width: 48px;
}
.param-table.typed th:nth-child(4) {
  width: 145px;
}
.param-table.typed th:nth-child(6) {
  width: 200px;
}
.param-table.typed th:nth-child(7) {
  width: 70px;
}
.param-drag {
  cursor: grab;
  color: #86909c;
}
.param-type,
.param-range {
  display: flex;
  align-items: center;
  gap: 6px;
}
.param-type :deep(.ant-select) {
  width: 105px;
}
.param-range :deep(.ant-input-number) {
  width: 78px;
}
</style>
