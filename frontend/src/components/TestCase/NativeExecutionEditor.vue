<template>
  <div class="native-execution-editor">
    <a-form-item :label="category === 'api' ? 'HTTP请求执行' : '场景请求执行'">
      <a-switch
        :checked="enabled"
        :disabled="disabled"
        aria-label="启用原生请求执行"
        @change="toggle"
      />
    </a-form-item>
    <template v-if="enabled && category === 'api'">
      <a-space wrap>
        <a-form-item label="请求方法"
          ><a-select
            v-model:value="method"
            :options="methods"
            :disabled="disabled"
            aria-label="HTTP请求方法"
            style="width: 130px"
        /></a-form-item>
        <a-form-item label="超时（毫秒）"
          ><a-input-number
            v-model:value="timeout"
            :min="1"
            :max="300000"
            :precision="0"
            :disabled="disabled"
            aria-label="HTTP请求超时"
        /></a-form-item>
        <a-form-item label="跟随重定向"
          ><a-switch
            v-model:checked="redirects"
            :disabled="disabled"
            aria-label="跟随重定向"
        /></a-form-item>
      </a-space>
      <a-tabs>
        <a-tab-pane key="query" tab="Query参数"
          ><a-textarea
            v-model:value="query"
            :disabled="disabled"
            :rows="4"
            aria-label="HTTP查询参数JSON"
        /></a-tab-pane>
        <a-tab-pane key="headers" tab="Headers"
          ><a-textarea
            v-model:value="headers"
            :disabled="disabled"
            :rows="4"
            aria-label="HTTP请求头JSON"
        /></a-tab-pane>
        <a-tab-pane key="body" tab="Body">
          <a-select
            v-model:value="bodyType"
            :disabled="disabled"
            :options="bodyTypes"
            aria-label="HTTP请求体类型"
            style="width: 160px"
          />
          <a-textarea
            v-if="bodyType !== 'none'"
            v-model:value="body"
            :disabled="disabled"
            :rows="5"
            :aria-label="
              bodyType === 'text' ? 'HTTP文本请求体' : 'HTTP请求体JSON'
            "
          />
        </a-tab-pane>
        <a-tab-pane key="assertions" tab="断言"
          ><a-textarea
            v-model:value="assertions"
            :disabled="disabled"
            :rows="5"
            aria-label="HTTP断言JSON"
          />
          <p>
            状态、JSON路径、响应头或文本断言；JSON路径使用键名和数组下标列表。
          </p></a-tab-pane
        >
      </a-tabs>
    </template>
    <template v-else-if="enabled">
      <a-form-item label="步骤失败时停止"
        ><a-switch
          v-model:checked="stop"
          :disabled="disabled"
          aria-label="场景步骤失败时停止"
      /></a-form-item>
      <div v-for="(step, index) in steps" :key="index" class="scenario-step">
        <span>{{ index + 1 }}</span>
        <a-select
          v-model:value="step.apiCaseId"
          :disabled="disabled"
          :options="apiCases.map((c) => ({ value: c.id, label: c.name }))"
          show-search
          option-filter-prop="label"
          aria-label="场景步骤API用例"
          placeholder="选择API用例"
          style="width: 280px; max-width: 100%"
        />
        <a-switch
          v-model:checked="step.enabled"
          :disabled="disabled"
          aria-label="启用场景步骤"
        />
        <a-button :disabled="disabled || index === 0" @click="move(index, -1)"
          >上移</a-button
        >
        <a-button
          :disabled="disabled || index === steps.length - 1"
          @click="move(index, 1)"
          >下移</a-button
        >
        <a-button :disabled="disabled" danger @click="steps.splice(index, 1)"
          >移除</a-button
        >
      </div>
      <a-button
        :disabled="disabled || steps.length >= 1000"
        @click="steps.push({ apiCaseId: '', enabled: true })"
        >添加API步骤</a-button
      >
    </template>
    <a-alert v-if="error" :message="error" type="error" show-icon />
  </div>
</template>
<script setup lang="ts">
import {
  useNativeExecutionDraft,
  type ExecutionEditorProps,
} from "./nativeExecutionDraft";
const props = defineProps<ExecutionEditorProps>();
const emit = defineEmits<{
  "update:modelValue": [value: string];
  error: [value: string];
  draft: [value: string];
}>();
const {
  enabled,
  method,
  timeout,
  redirects,
  stop,
  query,
  headers,
  bodyType,
  body,
  assertions,
  error,
  steps,
  methods,
  bodyTypes,
  toggle,
  move,
} = useNativeExecutionDraft(props, {
  update: (value) => emit("update:modelValue", value),
  error: (value) => emit("error", value),
  draft: (value) => emit("draft", value),
});
</script>
<style scoped>
.native-execution-editor {
  margin: 16px 0;
}
.scenario-step {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  align-items: center;
  margin-bottom: 12px;
}
</style>
