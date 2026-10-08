<template>
  <div class="execution-configuration">
    <a-form-item v-if="!root" label="继承上级配置">
      <a-switch
        :checked="value.extended"
        :disabled="disabled"
        @change="changeInheritance"
      />
    </a-form-item>
    <a-form-item label="资源池">
      <a-select
        ref="resourceSelect"
        :value="executionPoolValue(value)"
        :disabled="controlsDisabled"
        :options="poolOptions"
        @change="selectPool"
      />
      <a-button
        v-if="!disabled"
        type="link"
        size="small"
        @click="emit('managePool')"
        >配置资源池</a-button
      >
    </a-form-item>
    <a-form-item label="接口请求环境">
      <a-select
        ref="environmentSelect"
        :value="executionEnvironmentValue(value)"
        :disabled="controlsDisabled"
        :options="environmentOptions"
        @change="selectEnvironment"
      />
    </a-form-item>
    <a-form-item label="执行方式">
      <a-radio-group
        :value="value.executionMode"
        :disabled="controlsDisabled"
        @change="set('executionMode', $event.target.value)"
        ><a-radio value="serial">串行</a-radio
        ><a-radio value="parallel">并行</a-radio></a-radio-group
      >
    </a-form-item>
    <a-form-item v-if="value.executionMode === 'serial'" label="失败停止"
      ><a-switch
        :checked="value.stopOnFailure"
        :disabled="controlsDisabled"
        @change="set('stopOnFailure', $event)"
    /></a-form-item>
    <a-form-item label="失败重试"
      ><a-switch
        :checked="value.retryOnFailure"
        :disabled="controlsDisabled"
        @change="set('retryOnFailure', $event)"
    /></a-form-item>
    <template v-if="value.retryOnFailure">
      <a-form-item label="重试次数"
        ><a-input-number
          :value="value.retryTimes"
          :min="1"
          :max="10"
          :step="1"
          :precision="0"
          :disabled="controlsDisabled"
          @change="set('retryTimes', $event ?? 1)"
        />
        次</a-form-item
      >
      <a-form-item label="重试间隔"
        ><a-input-number
          :value="value.retryInterval"
          :min="0"
          :step="100"
          :precision="0"
          :disabled="controlsDisabled"
          @change="set('retryInterval', $event ?? 0)"
        />
        毫秒</a-form-item
      >
    </template>
  </div>
</template>
<script setup lang="ts">
import { computed, ref } from "vue";
import {
  executionEnvironmentValue,
  selectExecutionEnvironment,
  executionPoolOptions,
  executionPoolValue,
  selectExecutionPool,
  executionEnvironmentOptions,
} from "./planMinderTag";
import type {
  ExecutionConfig,
  ExecutionCatalog,
} from "@/api/planExecutionConfig";
const props = defineProps<{
  value: ExecutionConfig;
  inherited?: ExecutionConfig;
  root: boolean;
  catalog: ExecutionCatalog;
  disabled: boolean;
  category?: string;
}>();
const emit = defineEmits<{
  "update:value": [value: ExecutionConfig];
  managePool: [];
}>();
const controlsDisabled = computed(
  () => props.disabled || (!props.root && props.value.extended),
);
const poolOptions = computed(() =>
  executionPoolOptions(props.catalog, props.category),
);
const environmentOptions = computed(() =>
  executionEnvironmentOptions(props.catalog),
);
const resourceSelect = ref<{ focus: () => void }>(),
  environmentSelect = ref<{ focus: () => void }>();
function set<K extends keyof ExecutionConfig>(
  key: K,
  value: ExecutionConfig[K],
) {
  emit("update:value", { ...props.value, [key]: value });
}
function selectEnvironment(value: string) {
  emit("update:value", selectExecutionEnvironment(props.value, value));
}
function selectPool(value: string) {
  emit("update:value", selectExecutionPool(props.value, value));
}
function changeInheritance(value: boolean) {
  emit("update:value", {
    ...(value && props.inherited ? props.inherited : props.value),
    extended: value,
  });
}
function focus(kind: "environment" | "resource") {
  if (!controlsDisabled.value)
    (kind === "environment"
      ? environmentSelect.value
      : resourceSelect.value
    )?.focus();
}
defineExpose({ focus });
</script>
<style scoped>
.execution-configuration :deep(.ant-select) {
  width: 100%;
}
</style>
