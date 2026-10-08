<template>
  <a-modal
    :open="visible"
    title="导入用例"
    width="min(760px,96vw)"
    :footer="null"
    :closable="!busy"
    :mask-closable="!busy"
    :keyboard="!busy"
    @cancel="close"
  >
    <a-steps
      :current="step"
      size="small"
      :items="[
        { title: '选择文件' },
        { title: '校验内容' },
        { title: '确认导入' },
      ]"
      style="margin-bottom: 20px"
    />
    <a-alert
      message="支持 Excel、CSV、XMind。按编号识别已有用例；覆盖或跳过相同编号。未出现在文件中的用例不会删除。"
      type="info"
      show-icon
    />
    <template v-if="step === 0">
      <a-space wrap style="margin: 16px 0"
        ><a-button @click="template('xlsx')">下载 Excel 模板</a-button
        ><a-button @click="template('xmind')"
          >下载 XMind 模板</a-button
        ></a-space
      >
      <a-upload-dragger
        :before-upload="selectFile"
        :show-upload-list="false"
        :disabled="busy"
        accept=".xlsx,.xls,.csv,.xmind"
        ><p>{{ file?.name || "选择 Excel / CSV / XMind 文件" }}</p>
        <p>文件大小不超过 10 MiB</p></a-upload-dragger
      >
      <a-checkbox
        v-model:checked="overwrite"
        :disabled="busy"
        style="margin-top: 16px"
        >覆盖相同编号用例</a-checkbox
      >
    </template>
    <template v-else>
      <p>{{ file?.name }} · {{ overwrite ? "覆盖" : "跳过" }}相同编号</p>
      <a-spin :spinning="loading">
        <template v-if="preview"
          ><a-alert
            :type="validated ? 'success' : 'error'"
            :message="
              '校验 ' +
              (preview.total || 0) +
              ' 条，通过 ' +
              (preview.validated || 0) +
              ' 条，错误 ' +
              (preview.errors || 0) +
              ' 条'
            "
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
                >第 {{ item.row }} 行 · {{ item.name }}：{{
                  item.errors.join("；")
                }}</a-list-item
              ></template
            ></a-list
          >
          <a-list
            v-else-if="preview.error_details?.length"
            :data-source="preview.error_details"
            ><template #renderItem="{ item }"
              ><a-list-item>{{ item }}</a-list-item></template
            ></a-list
          >
        </template>
      </a-spin>
      <a-alert
        v-if="step === 2"
        type="info"
        message="确认后在当前项目写入以上范围；服务端会再次校验权限和文件内容。"
      />
    </template>
    <a-alert
      v-if="error"
      type="error"
      :message="error"
      style="margin-top: 12px"
    />
    <a-space style="display: flex; justify-content: flex-end; margin-top: 20px"
      ><a-button :disabled="busy" @click="close">取消</a-button
      ><a-button v-if="step > 0" :disabled="busy" @click="back">上一步</a-button
      ><a-button v-if="step === 1" :disabled="busy" @click="validate"
        >重新校验</a-button
      ><a-button
        v-if="step === 0"
        type="primary"
        :disabled="!file || busy"
        @click="validate"
        >下一步：校验</a-button
      ><a-button
        v-if="step === 1"
        type="primary"
        :disabled="!validated || busy"
        @click="step = 2"
        >下一步：确认</a-button
      ><a-button
        v-if="step === 2"
        type="primary"
        :loading="importing"
        :disabled="!validated || busy"
        @click="submit"
        >确认导入</a-button
      ></a-space
    >
  </a-modal>
</template>
<script setup lang="ts">
import { ref, computed, watch, onMounted, onBeforeUnmount } from "vue";
import { message, Modal } from "ant-design-vue";
import { onBeforeRouteLeave, onBeforeRouteUpdate } from "vue-router";
import { apiClient } from "@/utils/api";
import { testCaseApi } from "@/api/testCase";
import { saveCaseBlob } from "@/api/caseFeatures";
import { useUserStore } from "@/stores/user";
const props = defineProps<{ visible: boolean; projectId: string }>(),
  emit = defineEmits<{
    "update:visible": [value: boolean];
    success: [result: any];
  }>(),
  user = useUserStore();
const file = ref<File>(),
  overwrite = ref(false),
  preview = ref<any>(),
  validated = ref(false),
  loading = ref(false),
  importing = ref(false),
  step = ref(0),
  error = ref("");
const busy = computed(() => loading.value || importing.value);
let generation = 0;
function reset() {
  ++generation;
  file.value = undefined;
  preview.value = undefined;
  validated.value = false;
  overwrite.value = false;
  loading.value = false;
  importing.value = false;
  step.value = 0;
  error.value = "";
}
async function request(
  project: string,
  selected: File,
  cover: boolean,
  only: boolean,
) {
  const data = new FormData();
  data.append("file", selected);
  const response = await apiClient
    .getInstance()
    .post("/projects/" + project + "/cases/import", data, {
      params: { validate_only: only, overwrite: cover },
      headers: { "Content-Type": "multipart/form-data" },
      timeout: 120000,
    });
  return response.data;
}
function selectFile(selected: File) {
  if (busy.value) return false;
  if (!/\.(xlsx|xls|csv|xmind)$/i.test(selected.name)) {
    message.error("请选择 Excel、CSV 或 XMind 文件");
    return false;
  }
  if (selected.size > 10 * 1024 * 1024) {
    message.error("文件不能超过 10 MiB");
    return false;
  }
  ++generation;
  file.value = selected;
  preview.value = undefined;
  validated.value = false;
  error.value = "";
  return false;
}
async function validate() {
  if (!file.value || busy.value || !props.visible) return;
  const mine = ++generation,
    project = props.projectId,
    selected = file.value,
    cover = overwrite.value;
  loading.value = true;
  validated.value = false;
  preview.value = undefined;
  error.value = "";
  step.value = 1;
  try {
    const result = await request(project, selected, cover, true);
    if (mine !== generation) return;
    preview.value = result.data;
    validated.value =
      result.status === "success" && !!result.data && !result.data.errors;
    if (!validated.value)
      error.value = result.message || "文件校验未通过，请修正后重试";
  } catch (failure: any) {
    if (mine === generation) {
      preview.value = failure.response?.data?.data;
      error.value = "校验请求失败，文件保留；请重新校验";
    }
  } finally {
    if (mine === generation) loading.value = false;
  }
}
function back() {
  if (busy.value) return;
  step.value = Math.max(0, step.value - 1);
}
async function submit() {
  if (
    !file.value ||
    busy.value ||
    !props.visible ||
    step.value !== 2 ||
    !validated.value
  )
    return;
  const mine = generation,
    project = props.projectId,
    selected = file.value,
    cover = overwrite.value;
  importing.value = true;
  error.value = "";
  try {
    const result = await request(project, selected, cover, false);
    if (mine !== generation) return;
    if (result.status !== "success") {
      preview.value = result.data;
      validated.value = false;
      step.value = 1;
      error.value = result.message || "导入未完成，请重新校验";
      return;
    }
    emit("success", result.data);
    emit("update:visible", false);
  } catch (failure) {
    if (mine === generation)
      error.value =
        "导入请求失败，可能已经写入；请先核对用例列表，再决定是否重试";
  } finally {
    if (mine === generation) importing.value = false;
  }
}
async function template(format: "xlsx" | "xmind") {
  try {
    saveCaseBlob(
      await testCaseApi.getCaseTemplate(props.projectId, format),
      "用例导入模板." + format,
    );
  } catch (failure) {
    message.error("模板下载失败，请重试");
  }
}
async function beforeClose() {
  if (!props.visible) return true;
  if (busy.value) {
    message.warning("请等待校验或导入完成");
    return false;
  }
  if (!file.value) return true;
  return new Promise<boolean>((resolve) =>
    Modal.confirm({
      title: "放弃当前导入文件和校验结果？",
      onOk: () => {
        reset();
        emit("update:visible", false);
        resolve(true);
      },
      onCancel: () => resolve(false),
    }),
  );
}
async function close() {
  if (await beforeClose()) {
    ++generation;
    emit("update:visible", false);
  }
}
onBeforeRouteLeave(beforeClose);
onBeforeRouteUpdate(beforeClose);
function beforeUnload(event: BeforeUnloadEvent) {
  if (props.visible && (busy.value || file.value)) {
    event.preventDefault();
    event.returnValue = "";
  }
}
watch(
  () => props.visible,
  (open) => {
    if (open) reset();
    else ++generation;
  },
);
watch(
  () => [props.projectId, user.user?.id],
  () => {
    reset();
    if (props.visible) emit("update:visible", false);
  },
);
watch(overwrite, () => {
  validated.value = false;
  preview.value = undefined;
  step.value = 0;
});
onMounted(() => window.addEventListener("beforeunload", beforeUnload));
onBeforeUnmount(() => {
  ++generation;
  window.removeEventListener("beforeunload", beforeUnload);
});
defineExpose({ beforeClose });
</script>
