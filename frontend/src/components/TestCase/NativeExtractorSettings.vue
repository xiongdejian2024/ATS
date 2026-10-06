<template>
  <div class="extract-settings">
    <a-form-item
      v-if="modelValue.extractType === 'REGEX'"
      label="表达式匹配规则"
    >
      <a-radio-group
        :value="modelValue.expressionMatchingRule"
        :disabled="disabled"
        aria-label="表达式匹配规则"
        @change="set('expressionMatchingRule', $event.target.value)"
      >
        <a-radio value="EXPRESSION">匹配表达式</a-radio
        ><a-radio value="GROUP">匹配组</a-radio>
      </a-radio-group>
      <p class="hint">匹配表达式取完整匹配内容，匹配组取第一捕获组。</p>
    </a-form-item>
    <a-form-item label="结果匹配规则">
      <a-radio-group
        :value="modelValue.resultMatchingRule"
        :disabled="disabled"
        aria-label="结果匹配规则"
        @change="set('resultMatchingRule', $event.target.value)"
      >
        <a-radio value="RANDOM">随机匹配</a-radio
        ><a-radio value="SPECIFIC">指定匹配</a-radio
        ><a-radio value="ALL">全部匹配</a-radio>
      </a-radio-group>
    </a-form-item>
    <p v-if="modelValue.resultMatchingRule === 'ALL'" class="hint">
      全部匹配使用编号变量，例如
      {{ "${" + modelValue.variableName + "_1}" }}。JSONPath还提供
      {{ "${" + modelValue.variableName + "_ALL}" }}。
    </p>
    <a-form-item
      v-if="modelValue.resultMatchingRule === 'SPECIFIC'"
      label="指定匹配结果"
    >
      第
      <a-input-number
        :value="modelValue.resultMatchingRuleNum"
        :min="1"
        :max="2147483647"
        :precision="0"
        :disabled="disabled"
        aria-label="指定匹配序号"
        @change="set('resultMatchingRuleNum', $event || 1)"
      />
      条
    </a-form-item>
    <a-form-item v-if="modelValue.extractType === 'X_PATH'" label="内容类型">
      <a-radio-group
        :value="modelValue.responseFormat"
        :disabled="disabled"
        aria-label="提取响应文档类型"
        @change="set('responseFormat', $event.target.value)"
        ><a-radio value="XML">XML</a-radio
        ><a-radio value="HTML">HTML</a-radio></a-radio-group
      >
    </a-form-item>
  </div>
</template>
<script setup lang="ts">
import type { Extractor } from "./nativeExtractions";
const props = defineProps<{ modelValue: Extractor; disabled?: boolean }>();
const emit = defineEmits<{ "update:modelValue": [value: Extractor] }>();
function set(key: keyof Extractor, value: unknown) {
  if (!props.disabled)
    emit("update:modelValue", { ...props.modelValue, [key]: value });
}
</script>
<style scoped>
.hint {
  color: #86909c;
  font-size: 12px;
  margin: 6px 0;
}
.extract-settings :deep(.ant-radio-wrapper) {
  margin-bottom: 8px;
}
</style>
