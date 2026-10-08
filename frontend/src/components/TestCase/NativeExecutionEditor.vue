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
      </a-space>
      <a-tabs>
        <a-tab-pane key="pre-processors" tab="前置处理器"><NativeProcessorEditor v-model="preProcessors" :project-id="projectId" :disabled="disabled" /></a-tab-pane>
        <a-tab-pane key="post-processors" tab="后置处理器"><NativeProcessorEditor v-model="postExecutionProcessors" :project-id="projectId" :disabled="disabled" /></a-tab-pane>
        <a-tab-pane key="mock" tab="Mock"><NativeMockEditor v-model="mockResponse" :disabled="disabled" /></a-tab-pane>
        <a-tab-pane key="variables" tab="初始变量"
          ><NativeVariableEditor
            v-model="initialVariables"
            :disabled="disabled"
        /></a-tab-pane>
        <a-tab-pane key="headers" :tab="tabTitle('Headers', headers)"
          ><NativeRequestParamTable
            v-model="headers"
            title="Headers"
            :disabled="disabled"
        /></a-tab-pane>
        <a-tab-pane key="body" :tab="bodyType === 'none' ? 'Body' : 'Body (1)'">
          <a-radio-group
            :value="bodyType"
            :disabled="disabled"
            :options="bodyTypes"
            aria-label="HTTP请求体类型"
            @change="changeBodyType($event.target.value)"
          />
          <NativeRequestParamTable
            v-if="bodyType === 'multipart'"
            v-model="body"
            title="form-data"
            typed
            multipart
            :project-id="projectId || ''"
            :disabled="disabled"
          />
          <NativeRequestParamTable
            v-else-if="bodyType === 'form'"
            v-model="body"
            title="x-www-form-urlencoded"
            typed
            :disabled="disabled"
          />
          <NativeBinaryBodyEditor
            v-else-if="bodyType === 'binary'"
            v-model="body"
            :project-id="projectId || ''"
            :disabled="disabled"
          />
          <NativeJsonBodyEditor
            v-else-if="bodyType === 'json'"
            v-model="body"
            v-model:schema="jsonSchema"
            v-model:schema-mode="jsonSchemaMode"
            :project-id="projectId || ''"
            :disabled="disabled"
          />
          <a-textarea
            v-else-if="bodyType !== 'none'"
            v-model:value="body"
            :disabled="disabled"
            :rows="8"
            :aria-label="
              bodyType === 'xml'
                ? 'HTTP请求体XML'
                : bodyType === 'text'
                  ? 'HTTP文本请求体'
                  : 'HTTP请求体JSON'
            "
          />
          <a-empty v-else description="该请求没有请求体" />
        </a-tab-pane>
        <a-tab-pane key="query" :tab="tabTitle('Query', query)"
          ><NativeRequestParamTable
            v-model="query"
            title="Query"
            typed
            :disabled="disabled"
        /></a-tab-pane>
        <a-tab-pane key="rest" :tab="tabTitle('REST', rest)"
          ><NativeRequestParamTable
            v-model="rest"
            title="REST"
            typed
            :disabled="disabled"
        /></a-tab-pane>
        <a-tab-pane
          key="auth"
          :tab="authType === 'NONE' ? '认证配置' : '认证配置 (1)'"
        >
          <div class="request-auth">
            <p>认证方式</p>
            <a-radio-group
              v-model:value="authType"
              :disabled="disabled"
              aria-label="HTTP认证方式"
              ><a-radio value="NONE">No Auth</a-radio
              ><a-radio value="BASIC">Basic Auth</a-radio
              ><a-radio value="DIGEST">Digest Auth</a-radio></a-radio-group
            >
            <template v-if="authType === 'BASIC'"
              ><a-form-item label="用户名"
                ><a-input
                  v-model:value="basicUser"
                  :maxlength="255"
                  :disabled="disabled"
                  aria-label="Basic认证用户名" /></a-form-item
              ><a-form-item label="密码"
                ><a-input-password
                  v-model:value="basicPassword"
                  :maxlength="20000"
                  autocomplete="new-password"
                  :disabled="disabled"
                  aria-label="Basic认证密码" /></a-form-item
            ></template>
            <template v-else-if="authType === 'DIGEST'"
              ><a-form-item label="用户名"
                ><a-input
                  v-model:value="digestUser"
                  :maxlength="255"
                  :disabled="disabled"
                  aria-label="Digest认证用户名" /></a-form-item
              ><a-form-item label="密码"
                ><a-input-password
                  v-model:value="digestPassword"
                  :maxlength="20000"
                  autocomplete="new-password"
                  :disabled="disabled"
                  aria-label="Digest认证密码" /></a-form-item
            ></template>
          </div>
        </a-tab-pane>
        <a-tab-pane key="setting" tab="其他设置"
          ><a-space wrap>
            <a-form-item label="记录阶段耗时"><a-checkbox v-model:checked="reportPhases" :disabled="disabled" aria-label="记录HTTP阶段耗时">记录</a-checkbox></a-form-item>
            <a-form-item label="连接超时（毫秒）"
              ><a-input-number
                v-model:value="connectTimeout"
                :min="0"
                :max="600000"
                :precision="0"
                :placeholder="String(timeout)"
                :disabled="disabled"
                aria-label="HTTP连接超时"
            /></a-form-item>
            <a-form-item label="响应超时（毫秒）"
              ><a-input-number
                v-model:value="responseTimeout"
                :min="0"
                :max="600000"
                :precision="0"
                :placeholder="String(timeout)"
                :disabled="disabled"
                aria-label="HTTP响应超时"
            /></a-form-item>
            <a-form-item label="跟随重定向"
              ><a-checkbox
                v-model:checked="redirects"
                :disabled="disabled"
                aria-label="跟随重定向"
                >跟随</a-checkbox
              ></a-form-item
            >
          </a-space></a-tab-pane
        >
        <a-tab-pane key="post" tab="后置操作"
          ><NativePostProcessorEditor
            v-model="postProcessors"
            :project-id="projectId"
            :case-id="caseId"
            :disabled="disabled"
        /></a-tab-pane>
        <a-tab-pane key="assertions" tab="断言">
          <NativeResponseAssertionEditor
            v-model="responseAssertions"
            :disabled="disabled"
          />
          <details class="assertion-advanced">
            <summary>高级断言配置</summary>
            <a-textarea
              v-model:value="assertions"
              :disabled="disabled"
              :rows="5"
              aria-label="HTTP断言JSON"
            />
          </details>
        </a-tab-pane>
      </a-tabs>
    </template>
    <template v-else-if="enabled">
      <a-form-item label="场景初始变量"
        ><NativeVariableEditor v-model="initialVariables" :disabled="disabled"
      /></a-form-item>
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
    <a-collapse v-if="enabled"><a-collapse-panel key="global" header="用例 / 场景全局前后置（各执行一次）"><p>全局处理器在当前用例或场景开始、结束时各执行一次；场景 API 步骤使用请求前后置配置。</p><a-form-item label="全局前置"><NativeProcessorEditor v-model="globalPreProcessors" :project-id="projectId" :disabled="disabled" /></a-form-item><a-form-item label="全局后置"><NativeProcessorEditor v-model="globalPostProcessors" :project-id="projectId" :disabled="disabled" /></a-form-item></a-collapse-panel></a-collapse>
  </div>
</template>
<script setup lang="ts">
import NativePostProcessorEditor from "./NativePostProcessorEditor.vue";
import NativeVariableEditor from "./NativeVariableEditor.vue";
import NativeMockEditor from "./NativeMockEditor.vue";
import NativeProcessorEditor from "./NativeProcessorEditor.vue";
import NativeRequestParamTable from "./NativeRequestParamTable.vue";
import NativeBinaryBodyEditor from "./NativeBinaryBodyEditor.vue";
import NativeJsonBodyEditor from "./NativeJsonBodyEditor.vue";
import NativeResponseAssertionEditor from "./NativeResponseAssertionEditor.vue";
import { paramCount } from "./nativeRequestParams";
const tabTitle = (title: string, raw: string) => {
  const count = paramCount(raw);
  return count ? `${title} (${count})` : title;
};
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
  jsonSchemaMode,
  jsonSchema,
  assertions,
  responseAssertions,
  postProcessors,
  initialVariables,
  mockResponse,
  reportPhases,
  preProcessors,
  postExecutionProcessors,
  globalPreProcessors,
  globalPostProcessors,
  error,
  steps,
  methods,
  bodyTypes,
  toggle,
  move,
  changeBodyType,
  rest,
  authType,
  basicUser,
  basicPassword,
  digestUser,
  digestPassword,
  connectTimeout,
  responseTimeout,
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
.request-auth {
  padding: 16px;
  border: 1px solid #e5e6eb;
  border-radius: 4px;
}
.request-auth :deep(.ant-form-item) {
  max-width: 450px;
  margin-top: 16px;
}
.scenario-step {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  align-items: center;
  margin-bottom: 12px;
}
</style>
