<template>
  <a-card title="附件" size="small">
    <a-upload-dragger multiple :disabled="disabled || loading" :before-upload="selectFile" :show-upload-list="false">
      <p class="ant-upload-drag-icon"><InboxOutlined /></p>
      <p class="ant-upload-text">点击或将文件拖拽到这里上传</p>
      <p class="ant-upload-hint">支持选择多个文件，保存用例时上传</p>
    </a-upload-dragger>
    <a-alert v-if="loadFailed" type="error" message="附件加载失败，请重试后保存" show-icon>
      <template #action><a-button :disabled="disabled" @click="load">重试</a-button></template>
    </a-alert>
    <a-list :loading="loading" :data-source="displayFiles" size="small">
      <template #renderItem="{ item }">
        <a-list-item>
          <a-list-item-meta :title="item.name" :description="`${(item.size / 1024).toFixed(1)} KB · ${item.state}`" />
          <template #actions>
            <a-button v-if="item.persisted && !removed.includes(item.id)" type="link" :disabled="disabled" @click="download(item.id)">下载</a-button>
            <a-button type="link" :danger="!removed.includes(item.id)" :disabled="disabled" @click="toggleRemove(item.id, item.persisted)">{{ removed.includes(item.id) ? '撤销删除' : '删除' }}</a-button>
          </template>
        </a-list-item>
      </template>
    </a-list>
  </a-card>
</template>
<script setup lang="ts">
import { computed, ref, watch } from 'vue';
import { InboxOutlined } from '@ant-design/icons-vue';
import { caseFeaturesApi as api, saveCaseBlob, type CaseFile } from '@/api/caseFeatures';
import { flushAttachmentDraft } from './attachmentDraft';

const props = defineProps<{ projectId: string; caseId?: string; disabled?: boolean }>();
const emit = defineEmits<{ (e: 'change', signature: string): void }>();
const files = ref<CaseFile[]>([]);
const pending = ref<Array<{ id: string; file: File }>>([]);
const removed = ref<string[]>([]);
const loading = ref(false), loadFailed = ref(false);
const displayFiles = computed(() => [
  ...files.value.map(f => ({ id: f.id, name: f.fileName, size: f.fileSize, persisted: true, state: removed.value.includes(f.id) ? '保存时删除' : '已保存' })),
  ...pending.value.map(f => ({ id: f.id, name: f.file.name, size: f.file.size, persisted: false, state: '等待保存' })),
]);
function selectFile(file: File) {
  if (props.disabled || loading.value) return false;
  pending.value.push({ id: crypto.randomUUID(), file });
  console.info('已选择待保存附件', { name: file.name, size: file.size });
  return false;
}
function toggleRemove(id: string, persisted: boolean) {
  if (!persisted) pending.value = pending.value.filter(f => f.id !== id);
  else if (removed.value.includes(id)) removed.value = removed.value.filter(x => x !== id);
  else removed.value.push(id);
}
async function load() {
  files.value = [];
  if (!props.caseId) return;
  loading.value = true;
  loadFailed.value = false;
  try { files.value = await api.attachments(props.projectId, props.caseId); }
  catch (error) { loadFailed.value = true; console.error('加载编辑用例附件失败', error); }
  finally { loading.value = false; }
}
async function download(id: string) {
  const file = files.value.find(f => f.id === id);
  if (!file) return;
  try { saveCaseBlob(await api.download(props.projectId, id), file.fileName); }
  catch (error) { console.error('下载编辑用例附件失败', error); }
}
async function flush(caseId: string) {
  if (loading.value || loadFailed.value) throw new Error('请等待附件加载成功后再保存');
  try {
    await flushAttachmentDraft(pending.value, removed.value,
      async item => { files.value.push(await api.upload(props.projectId, caseId, item.file)); },
      async id => { await api.deleteAttachment(props.projectId, id); files.value = files.value.filter(f => f.id !== id); },
    );
    console.info('用例附件保存完成', { caseId });
  } catch (error) { console.error('用例附件保存失败，保留未完成附件等待重试', error); throw error; }
}
watch(() => pending.value.length || removed.value.length ? JSON.stringify({ pending: pending.value.map(f => f.id), removed: removed.value }) : '', signature => emit('change', signature));
watch(() => [props.projectId, props.caseId], load, { immediate: true });
defineExpose({ flush, canSave: () => !loading.value && !loadFailed.value });
</script>
