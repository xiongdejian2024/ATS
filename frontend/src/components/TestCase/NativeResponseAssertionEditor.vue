<template>
  <div class="response-assertion-editor">
    <a-dropdown :trigger="['hover', 'click']" :disabled="disabled"
      ><a-button
        :disabled="disabled"
        class="assertion-add"
        aria-label="添加响应断言"
        ><PlusOutlined />断言</a-button
      ><template #overlay
        ><a-menu @click="add($event.key)"
          ><a-menu-item v-for="kind in responseKinds" :key="kind.value">{{
            kind.label
          }}</a-menu-item></a-menu
        ></template
      ></a-dropdown
    >
    <div v-if="groups.length" class="assertion-body">
      <VueDraggable
        v-model="groups"
        class="assertion-nav"
        handle=".assertion-drag"
        :disabled="disabled"
        :animation="150"
        @end="publish"
      >
        <div
          v-for="(group, index) in groups"
          :key="group.id"
          class="assertion-kind"
          :class="{ active: group.id === activeId }"
          role="button"
          tabindex="0"
          :aria-label="`选择${assertionLabel(group.name)}`"
          @click="activeId = group.id"
          @keydown.enter="activeId = group.id"
          @keydown.space.prevent="activeId = group.id"
        >
          <span class="assertion-kind-name"
            ><span>{{ index + 1 }}</span
            ><span :title="group.name">{{ group.name }}</span></span
          >
          <span class="assertion-kind-actions"
            ><HolderOutlined
              v-if="!disabled"
              class="assertion-drag"
              :aria-label="`拖动${assertionLabel(group.name)}`" /><a-dropdown
              v-if="!disabled"
              :trigger="['click']"
              ><a-button
                type="text"
                size="small"
                :aria-label="`${assertionLabel(group.name)}更多`"
                @click.stop
                ><MoreOutlined /></a-button
              ><template #overlay
                ><a-menu @click="remove(group)"
                  ><a-menu-item key="delete" danger>删除</a-menu-item></a-menu
                ></template
              ></a-dropdown
            ><a-switch
              v-model:checked="group.enable"
              :disabled="disabled"
              size="small"
              :aria-label="`启用${assertionLabel(group.name)}`"
              @click.stop
              @change="publish"
          /></span>
        </div>
      </VueDraggable>
      <div v-if="active" class="assertion-detail">
        <div
          v-if="active.assertionType === 'RESPONSE_CODE'"
          class="assertion-code"
        >
          <p>状态码</p>
          <a-space wrap
            ><a-select
              v-model:value="active.condition"
              :options="codeConditions"
              :disabled="disabled"
              aria-label="状态码匹配条件"
              style="width: 157px"
              @change="codeChange" /><a-input
              v-model:value="active.expectedValue"
              :maxlength="20000"
              :disabled="disabled || active.condition === 'UNCHECK'"
              aria-label="状态码匹配值"
              style="width: 157px"
              @change="publish"
          /></a-space>
        </div>
        <NativeAssertionRuleTable
          v-else-if="active.assertionType === 'RESPONSE_HEADER'"
          v-model="active.assertions!"
          mode="HEADER"
          :disabled="disabled"
          @update:modelValue="publish"
        />
        <NativeAssertionRuleTable
          v-else-if="active.assertionType === 'VARIABLE'"
          v-model="active.variableAssertionItems!"
          mode="VARIABLE"
          :disabled="disabled"
          @update:modelValue="publish"
        />
        <div v-else-if="active.assertionType === 'RESPONSE_TIME'">
          <p>响应时间 <span class="assertion-unit">(ms)</span></p>
          <a-space wrap
            ><span>小于或等于</span
            ><a-input-number
              v-model:value="active.expectedValue"
              :min="0"
              :max="2147483647"
              :precision="0"
              :step="100"
              :disabled="disabled"
              aria-label="响应时间断言毫秒"
              @change="publish"
          /></a-space>
        </div>
        <template v-else
          ><a-radio-group
            v-model:value="active.assertionBodyType"
            :disabled="disabled"
            aria-label="响应体断言方式"
            @change="publish"
            ><a-radio-button value="JSON_PATH">JSONPath</a-radio-button
            ><a-radio-button value="XPATH">XPath</a-radio-button
            ><a-radio-button value="REGEX">正则</a-radio-button></a-radio-group
          >
          <div class="assertion-body-table">
            <NativeAssertionRuleTable
              v-if="active.assertionBodyType === 'JSON_PATH'"
              v-model="active.jsonPathAssertion!.assertions"
              mode="JSON_PATH"
              :disabled="disabled"
              @update:modelValue="publish"
            />
            <template v-else-if="active.assertionBodyType === 'XPATH'"
              ><p>响应内容格式</p>
              <a-radio-group
                v-model:value="active.xpathAssertion!.responseFormat"
                :disabled="disabled"
                aria-label="XPath响应内容格式"
                @change="publish"
                ><a-radio-button value="XML">XML</a-radio-button
                ><a-radio-button value="HTML"
                  >HTML</a-radio-button
                ></a-radio-group
              ><NativeAssertionRuleTable
                v-model="active.xpathAssertion!.assertions"
                mode="XPATH"
                :disabled="disabled"
                class="xpath-table"
                @update:modelValue="publish"
            /></template>
            <NativeAssertionRuleTable
              v-else
              v-model="active.regexAssertion!.assertions"
              mode="REGEX"
              :disabled="disabled"
              @update:modelValue="publish"
            />
          </div>
        </template>
      </div>
    </div>
    <a-alert v-if="error" :message="error" type="error" show-icon />
  </div>
</template>
<script setup lang="ts">
import { computed, ref, watch } from "vue";
import { Modal } from "ant-design-vue";
import { VueDraggable } from "vue-draggable-plus";
import {
  PlusOutlined,
  HolderOutlined,
  MoreOutlined,
} from "@ant-design/icons-vue";
import NativeAssertionRuleTable from "./NativeAssertionRuleTable.vue";
import {
  responseKinds,
  newResponseGroup,
  readResponseAssertions,
  codeConditions,
  type Kind,
  type ResponseGroup,
} from "./nativeResponseAssertions";
const props = defineProps<{ modelValue: string; disabled?: boolean }>();
const emit = defineEmits<{ "update:modelValue": [value: string] }>();
const groups = ref<ResponseGroup[]>([]),
  activeId = ref(""),
  error = ref("");
const assertionLabel = (name: string) =>
  name.endsWith("断言") ? name : `${name}断言`;
let output = "";
const active = computed(
  () => groups.value.find((g) => g.id === activeId.value) || groups.value[0],
);
watch(
  () => props.modelValue,
  (raw) => {
    if (raw === output) return;
    try {
      groups.value = readResponseAssertions(raw);
      activeId.value =
        groups.value.find((g) => g.id === activeId.value)?.id ||
        groups.value[0]?.id ||
        "";
      error.value = "";
    } catch (exception) {
      console.error("响应断言加载失败，原编辑草稿保留", exception);
      error.value = "响应断言无法载入，请修正高级配置";
    }
  },
  { immediate: true },
);
function publish() {
  if (props.disabled) return;
  output = JSON.stringify(groups.value);
  emit("update:modelValue", output);
  try {
    readResponseAssertions(output);
    error.value = "";
  } catch (exception) {
    console.error("响应断言校验失败，草稿保留", exception);
    error.value =
      exception instanceof Error ? exception.message : "响应断言配置无效";
  }
}
function add(value: string | number) {
  if (props.disabled) return;
  const kind = value as Kind;
  if (!responseKinds.some((k) => k.value === kind)) return;
  const existing = groups.value.find((g) => g.assertionType === kind);
  if (existing) {
    activeId.value = existing.id;
    return;
  }
  const group = newResponseGroup(kind);
  groups.value.push(group);
  activeId.value = group.id;
  publish();
  console.info("响应断言已添加", { 类别: group.name });
}
function codeChange() {
  if (active.value?.condition === "UNCHECK") active.value.expectedValue = "";
  publish();
}
function remove(group: ResponseGroup) {
  if (props.disabled) return;
  Modal.confirm({
    title: `删除${group.name}`,
    content: "删除后将移除此断言配置，是否继续？",
    okText: "确认删除",
    cancelText: "取消",
    okButtonProps: { danger: true },
    onOk: () => {
      const index = groups.value.findIndex((g) => g.id === group.id);
      if (index < 0) return;
      groups.value.splice(index, 1);
      activeId.value = groups.value[Math.max(0, index - 1)]?.id || "";
      publish();
      console.info("响应断言已删除", { 类别: group.name });
    },
  });
}
</script>
<style scoped>
.response-assertion-editor {
  min-width: 0;
}
.assertion-add {
  width: 84px;
}
.assertion-body {
  display: flex;
  gap: 8px;
  margin-top: 8px;
  min-height: 264px;
  min-width: 0;
}
.assertion-nav {
  width: 216px;
  min-width: 216px;
  padding: 12px;
  background: #f7f8fa;
  overflow-y: auto;
  max-height: 420px;
  flex-shrink: 0;
}
.assertion-kind {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 4px;
  padding: 8px 4px;
  cursor: pointer;
  border: 1px solid transparent;
}
.assertion-kind.active {
  background: #fff;
  border-color: #e5e6eb;
  color: var(--ms-color-primary);
}
.assertion-kind-name {
  display: flex;
  gap: 8px;
  min-width: 0;
}
.assertion-kind-name > span:last-child {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  max-width: 80px;
}
.assertion-kind-actions {
  display: flex;
  align-items: center;
  gap: 3px;
}
.assertion-drag {
  cursor: grab;
  color: #86909c;
}
.assertion-detail {
  border: 1px solid #e5e6eb;
  padding: 16px;
  flex: 1;
  min-width: 0;
  overflow: hidden;
}
.assertion-body-table,
.xpath-table {
  margin-top: 16px;
}
.assertion-unit {
  color: #86909c;
}
@media (max-width: 600px) {
  .assertion-body {
    flex-direction: column;
  }
  .assertion-nav {
    width: 100%;
    min-width: 0;
    max-height: 220px;
  }
  .assertion-detail {
    padding: 12px;
  }
}
</style>
