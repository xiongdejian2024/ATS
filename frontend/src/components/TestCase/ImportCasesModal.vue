<template>
  <a-modal
    :open="visible"
    title="导入用例"
    width="min(760px,96vw)"
    :confirm-loading="importing"
    :ok-text="validateOnly ? '仅校验' : '确认导入'"
    :ok-button-props="{ disabled: !file || loading || !!preview?.errors }"
    @ok="submit"
    @cancel="close"
  >
    <a-alert
      message="支持 Excel、CSV、XMind。按编号识别已有用例；可选择覆盖或跳过。文件中未出现的既有用例不会删除。"
      type="info"
      show-icon
    />
    <a-upload-dragger
      :before-upload="selectFile"
      :show-upload-list="false"
      accept=".xlsx,.xls,.csv,.xmind"
      style="margin: 16px 0"
      ><p>{{ file ? file.name : "点击选择 Excel / CSV / XMind 文件" }}</p>
      <p>文件大小不超过 10 MiB</p></a-upload-dragger
    >
    <a-space wrap style="margin: 16px 0"
      ><a-checkbox v-model:checked="overwrite" @change="validate"
        >覆盖相同编号用例</a-checkbox
      ><a-checkbox v-model:checked="validateOnly">仅校验</a-checkbox
      ><a-button :disabled="loading || importing" @click="template"
        >下载 Excel 模板</a-button
      ></a-space
    >
    <a-spin :spinning="loading"
      ><template v-if="preview"
        ><a-alert
          :type="preview.errors ? 'error' : 'success'"
          :message="`校验 ${preview.total || 0} 条，通过 ${preview.validated || 0} 条，错误 ${preview.errors || 0} 条`"
          show-icon
        />
        <p v-if="preview.preview">
          预计新增 {{ preview.preview.to_create || 0 }} 条，更新
          {{ preview.preview.to_update || 0 }} 条；跳过或不变
          {{ preview.preview.no_change || preview.preview.to_skip || 0 }} 条。
        </p>
        <a-list
          v-if="preview.validation_errors?.length"
          :data-source="preview.validation_errors"
          ><template #renderItem="{ item }"
            ><a-list-item
              ><span
                >第 {{ item.row }} 行 · {{ item.name }}：{{
                  item.errors.join("；")
                }}</span
              ></a-list-item
            ></template
          ></a-list
        ><a-list
          v-else-if="preview.error_details?.length"
          :data-source="preview.error_details"
          ><template #renderItem="{ item }"
            ><a-list-item>{{ item }}</a-list-item></template
          ></a-list
        ></template
      ><a-empty
        v-else
        description="选择文件后自动校验，确认导入前不会写入用例库"
    /></a-spin>
  </a-modal>
</template>
<script setup lang="ts">
import { ref, watch } from "vue";
import { message } from "ant-design-vue";
import { apiClient } from "@/utils/api";
import { testCaseApi } from "@/api/testCase";
import { saveCaseBlob } from "@/api/caseFeatures";
const props = defineProps<{ visible: boolean; projectId: string }>(),
  emit = defineEmits<{
    "update:visible": [value: boolean];
    success: [result: any];
  }>();
const file = ref<File>(),
  overwrite = ref(false),
  validateOnly = ref(false),
  preview = ref<any>(),
  loading = ref(false),
  importing = ref(false);
let generation = 0;
async function request(only: boolean) {
  if (!file.value) return;
  const data = new FormData();
  data.append("file", file.value);
  const response = await apiClient
    .getInstance()
    .post(`/projects/${props.projectId}/cases/import`, data, {
      params: { validate_only: only, overwrite: overwrite.value },
      headers: { "Content-Type": "multipart/form-data" },
      timeout: 120000,
    });
  return response.data;
}
async function selectFile(selected: File) {
  if (!/\.(xlsx|xls|csv|xmind)$/i.test(selected.name)) {
    message.error("请选择 Excel、CSV 或 XMind 文件");
    return false;
  }
  if (selected.size > 10 * 1024 * 1024) {
    message.error("文件不能超过 10 MiB");
    return false;
  }
  file.value = selected;
  await validate();
  return false;
}
async function validate() {
  if (!file.value) return;
  const mine = ++generation;
  loading.value = true;
  preview.value = undefined;
  try {
    const result = await request(true);
    if (mine === generation) {
      preview.value = result.data;
      if (result.status === "error")
        message.warning(result.message || "文件包含校验错误");
    }
  } catch (error: any) {
    console.error("校验导入文件失败", error);
    if (mine === generation) preview.value = error.response?.data?.data;
  } finally {
    if (mine === generation) loading.value = false;
  }
}
async function submit() {
  if (!file.value) return;
  if (validateOnly.value) {
    await validate();
    return;
  }
  if (preview.value?.errors) return message.warning("请修正错误后重试");
  importing.value = true;
  try {
    const result = await request(false);
    if (result.status === "error") {
      preview.value = result.data;
      message.error(result.message || "导入失败");
      return;
    }
    emit("success", result.data);
    emit("update:visible", false);
  } catch (error) {
    console.error("导入用例失败", error);
  } finally {
    importing.value = false;
  }
}
async function template() {
  try {
    saveCaseBlob(
      await testCaseApi.getCaseTemplate(props.projectId),
      "用例导入模板.xlsx",
    );
  } catch (error) {
    console.error("下载用例模板失败", error);
  }
}
function close() {
  if (importing.value) return;
  generation++;
  emit("update:visible", false);
}
watch(
  () => props.visible,
  (open) => {
    if (open) {
      file.value = undefined;
      preview.value = undefined;
      overwrite.value = false;
      validateOnly.value = false;
      loading.value = false;
    }
  },
);
</script>
