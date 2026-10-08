<template>
  <a-drawer
    :open="open"
    title="缺陷详情"
    width="min(980px,100vw)"
    :mask-closable="!busy && !mediaBusy"
    :closable="!busy && !mediaBusy"
    @close="beforeClose"
  >
    <a-spin v-if="loading" />
    <a-alert v-if="error" type="error" :message="error" />
    <template v-if="ready">
      <a-space wrap
        ><a-tag v-if="archived">已归档</a-tag
        ><span>版本 {{ draft.expectedRevision }}</span
        ><a-button
          v-if="canWrite"
          type="primary"
          :disabled="busy || mediaBusy"
          :loading="busy"
          @click="save"
          >保存缺陷</a-button
        ><a-button
          v-if="id && capabilities.canDelete"
          :disabled="busy || mediaBusy"
          @click="archive"
          >{{ archived ? "恢复" : "归档" }}</a-button
        ><a-button :disabled="busy || mediaBusy" @click="beforeClose"
          >关闭</a-button
        ></a-space
      >
      <a-tabs :active-key="tab" @change="changeTab">
        <a-tab-pane key="details" tab="详情">
          <a-form layout="vertical" :disabled="!canWrite || busy || mediaBusy">
            <a-form-item label="标题" required
              ><a-input v-model:value="draft.title" :maxlength="300"
            /></a-form-item>
            <a-row :gutter="16"
              ><a-col :xs="24" :sm="12"
                ><a-form-item label="状态"
                  ><a-select
                    v-model:value="draft.status"
                    :options="statusOptions" /></a-form-item></a-col
              ><a-col :xs="24" :sm="12"
                ><a-form-item label="缺陷模板"
                  ><a-select
                    :value="draft.templateId || ''"
                    :options="templateOptions"
                    @change="selectTemplate" /></a-form-item></a-col
            ></a-row>
            <a-form-item label="描述"
              ><template v-if="draft.descriptionFormat === 'plain'"
                ><a-textarea
                  v-if="canWrite"
                  v-model:value="draft.description"
                  :maxlength="30000"
                  :rows="5"
                />
                <p v-else class="plain">{{ draft.description || "无描述" }}</p>
                <a-button
                  v-if="canWrite"
                  type="link"
                  :disabled="busy || mediaBusy"
                  @click="convertRich"
                  >转为富文本</a-button
                ></template
              ><CaseRichText
                v-else
                v-model="draft.description"
                :readonly="!canWrite"
                :disabled="busy || mediaBusy"
                :project-id="projectId"
                mention-context="defect"
                :upload-image="uploadImage"
                :select-image="selectImage"
                @uploading="richUploading = $event"
            /></a-form-item>
            <a-form-item label="外部引用"
              ><a-input v-model:value="draft.externalRef" :maxlength="500"
            /></a-form-item>
            <CaseCustomFields
              v-model="draft.customFields"
              :fields="fields"
              :readonly="!canWrite || busy || mediaBusy"
            />
            <dl v-if="!fields.length && Object.keys(draft.customFields).length">
              <template v-for="(value, key) in draft.customFields" :key="key">
                <dt>{{ key }}</dt>
                <dd>
                  {{
                    typeof value === "string" ? value : JSON.stringify(value)
                  }}
                </dd>
              </template>
            </dl>
          </a-form>
          <a-card title="文件" size="small"
            ><a-button
              v-if="canWrite"
              :disabled="busy || mediaBusy"
              @click="pickFiles('details')"
              >关联项目文件</a-button
            >
            <p class="hint">项目文件库共享已发布文件；归档保留证据和原字节。</p>
            <a-list :data-source="attachments"
              ><template #renderItem="{ item }"
                ><a-list-item
                  >{{ item.fileName
                  }}<a-tag v-if="item.archived">文件已归档</a-tag
                  ><template #actions
                    ><a-button type="link" @click="download(item)"
                      >下载</a-button
                    ><a-button
                      v-if="canWrite"
                      type="link"
                      :disabled="busy || mediaBusy"
                      @click="removeFile(item.id, 'details')"
                      >移除关联</a-button
                    ></template
                  ></a-list-item
                ></template
              ></a-list
            ></a-card
          >
          <p v-if="templateError" class="error">
            {{ templateError }}，已保存字段和值会保留。
          </p>
        </a-tab-pane>
        <a-tab-pane v-if="id" key="comments" tab="评论">
          <a-alert
            v-if="commentsError"
            type="error"
            :message="commentsError"
          /><a-button
            :loading="commentsLoading"
            :disabled="busy"
            @click="loadComments"
            >刷新评论</a-button
          >
          <a-card
            v-for="item in comments"
            :key="item.id"
            size="small"
            class="entry"
            ><p>{{ item.authorId }} · {{ formatDate(item.createdAt) }}</p>
            <CaseRichText :model-value="item.content" readonly /><a-space wrap
              ><a-button
                v-for="file in item.files"
                :key="file.id"
                type="link"
                @click="download(file)"
                >{{ file.fileName }}</a-button
              ><a-button
                v-if="item.canDelete && !archived"
                danger
                :disabled="busy || mediaBusy"
                @click="removeComment(item)"
                >删除评论</a-button
              ></a-space
            ></a-card
          >
          <a-pagination
            :current="commentPage"
            :total="commentTotal"
            :page-size="20"
            :show-size-changer="false"
            @change="paginateComments"
          />
          <template v-if="capabilities.canUpdate && !archived"
            ><CaseRichText
              v-model="commentDraft.content"
              :disabled="busy || mediaBusy"
              :project-id="projectId"
              mention-context="defect"
              :upload-image="uploadImage"
              :select-image="selectImage"
              @uploading="richUploading = $event"
            /><a-space wrap
              ><a-button
                :disabled="busy || mediaBusy"
                @click="pickFiles('comments')"
                >关联文件</a-button
              ><a-button
                type="primary"
                :loading="busy"
                :disabled="busy || mediaBusy"
                @click="submitComment"
                >提交评论</a-button
              ><a-tag
                v-for="file in commentFiles"
                :key="file.id"
                closable
                @close.prevent="removeFile(file.id, 'comments')"
                >{{ file.fileName }}</a-tag
              ></a-space
            ></template
          >
        </a-tab-pane>
        <a-tab-pane v-if="id" key="history" tab="变更历史">
          <a-alert
            v-if="historyError"
            type="error"
            :message="historyError" /><a-button
            :loading="historyLoading"
            :disabled="busy"
            @click="loadHistory"
            >刷新历史</a-button
          ><a-card
            v-for="item in history"
            :key="item.id"
            size="small"
            class="entry"
            ><p>
              版本 {{ item.revision }} ·
              {{ actions[item.action] || item.action }} ·
              {{ formatDate(item.createdAt) }} · {{ item.actorId }}
            </p>
            <p>
              {{ item.detail.snapshot.title }} ·
              {{
                statusLabels[item.detail.snapshot.status] ||
                item.detail.snapshot.status
              }}
            </p>
            <CaseRichText
              v-if="item.detail.content"
              :model-value="item.detail.content"
              readonly
            /><template v-else
              ><CaseRichText
                v-if="item.detail.snapshot.descriptionFormat === 'rich'"
                :model-value="item.detail.snapshot.description"
                readonly
              />
              <p v-else class="plain">
                {{ item.detail.snapshot.description }}
              </p></template
            ><a-space wrap
              ><a-button
                v-for="file in item.files"
                :key="file.id"
                type="link"
                @click="download(file)"
                >{{ file.fileName }}</a-button
              ></a-space
            ></a-card
          ><a-pagination
            :current="historyPage"
            :total="historyTotal"
            :page-size="20"
            :show-size-changer="false"
            @change="paginateHistory"
        /></a-tab-pane>
      </a-tabs>
    </template>
    <FileLibraryPicker ref="filePicker" :project-id="projectId" />
  </a-drawer>
</template>
<script setup lang="ts">
import {
  computed,
  ref,
  reactive,
  watch,
  onBeforeUnmount,
  onMounted,
} from "vue";
import { onBeforeRouteLeave, onBeforeRouteUpdate } from "vue-router";
import { Modal, message } from "ant-design-vue";
import { useUserStore } from "@/stores/user";
import {
  defectsApi as api,
  type DefectInput,
  type DefectCapabilities,
  type DefectTemplate,
  type DefectComment,
  type DefectEvent,
} from "@/api/defects";
import { fileLibraryApi, type LibraryFile } from "@/api/fileLibrary";
import { createRequestId } from "@/utils/requestId";
import { saveCaseBlob } from "@/api/caseFeatures";
import CaseCustomFields from "./CaseCustomFields.vue";
import CaseRichText from "./CaseRichText.vue";
import FileLibraryPicker from "./FileLibraryPicker.vue";
const props = defineProps<{
  open: boolean;
  projectId: string;
  defectId?: string;
  initialCapabilities: DefectCapabilities;
}>();
const emit = defineEmits<{ "update:open": [boolean]; changed: [string] }>();
const user = useUserStore();
const blank = (): DefectInput => ({
  title: "",
  description: "",
  descriptionFormat: "plain",
  status: "open",
  externalRef: null,
  templateId: null,
  customFields: {},
  fileIds: [],
  expectedRevision: 0,
  requestId: createRequestId(),
});
const draft = reactive(blank()),
  commentDraft = reactive({
    content: "",
    fileIds: [] as string[],
    requestId: createRequestId(),
  });
const id = ref(""),
  ready = ref(false),
  loading = ref(false),
  busy = ref(false),
  error = ref(""),
  archived = ref(false),
  tab = ref("details"),
  baseline = ref("");
const capabilities = reactive<DefectCapabilities>({
  canRead: false,
  canCreate: false,
  canUpdate: false,
  canDelete: false,
});
const templates = ref<DefectTemplate[]>([]),
  templateError = ref(""),
  fileCache = reactive<Record<string, LibraryFile>>({}),
  filePicker = ref<InstanceType<typeof FileLibraryPicker>>();
const selectingFiles = ref(false),
  richUploading = ref(false),
  mediaBusy = computed(
    () =>
      selectingFiles.value ||
      richUploading.value ||
      !!filePicker.value?.isBusy(),
  );
const comments = ref<DefectComment[]>([]),
  commentPage = ref(1),
  commentTotal = ref(0),
  commentsLoading = ref(false),
  commentsError = ref("");
const history = ref<DefectEvent[]>([]),
  historyPage = ref(1),
  historyTotal = ref(0),
  historyLoading = ref(false),
  historyError = ref("");
let live = true,
  epoch = 0,
  commentSequence = 0,
  historySequence = 0,
  closing = false;
const current = (mine: number) => live && mine === epoch && props.open;
const body = (): DefectInput => ({
  ...draft,
  customFields: JSON.parse(JSON.stringify(draft.customFields)),
  fileIds: [...draft.fileIds],
});
const dirty = computed(
  () =>
    ready.value &&
    (JSON.stringify(body()) !== baseline.value ||
      !!commentDraft.content ||
      commentDraft.fileIds.length > 0),
);
const canWrite = computed(
  () =>
    !archived.value &&
    (id.value ? capabilities.canUpdate : capabilities.canCreate),
);
const statusLabels: Record<string, string> = {
  open: "待处理",
  in_progress: "处理中",
  resolved: "已解决",
  closed: "已关闭",
};
const statusOptions = Object.entries(statusLabels).map(([value, label]) => ({
  value,
  label,
}));
const actions: Record<string, string> = {
  created: "创建",
  updated: "更新",
  archived: "归档",
  restored: "恢复",
  commented: "评论",
  comment_removed: "删除评论",
};
const fields = computed(
  () => templates.value.find((t) => t.id === draft.templateId)?.fields || [],
);
const templateOptions = computed(() => [
  { value: "", label: "无模板" },
  ...templates.value.map((t) => ({
    value: t.id,
    label: t.name + (t.isDefault ? "（默认）" : ""),
  })),
  ...(draft.templateId &&
  !templates.value.some((t) => t.id === draft.templateId)
    ? [{ value: draft.templateId, label: "已记录模板" }]
    : []),
]);
const attachments = computed(() =>
  draft.fileIds.map(
    (key) =>
      fileCache[key] ||
      ({ id: key, fileName: "已记录文件 " + key } as LibraryFile),
  ),
);
const commentFiles = computed(() =>
  commentDraft.fileIds.map((key) => fileCache[key]),
);
const formatDate = (value: string) => new Date(value).toLocaleString("zh-CN");
function pruneFiles() {
  const keep = new Set([...draft.fileIds, ...commentDraft.fileIds]);
  for (const key of Object.keys(fileCache))
    if (!keep.has(key)) delete fileCache[key];
}
function adoptRevision(value: number) {
  draft.expectedRevision = value;
  if (baseline.value) {
    const saved = JSON.parse(baseline.value);
    saved.expectedRevision = value;
    baseline.value = JSON.stringify(saved);
  }
}
async function initialize() {
  const mine = ++epoch;
  closing = false;
  busy.value = false;
  loading.value = props.open;
  ready.value = false;
  error.value = "";
  tab.value = "details";
  id.value = props.defectId || "";
  archived.value = false;
  baseline.value = "";
  Object.assign(draft, blank());
  Object.assign(commentDraft, {
    content: "",
    fileIds: [],
    requestId: createRequestId(),
  });
  Object.assign(capabilities, {
    canRead: false,
    canCreate: false,
    canUpdate: false,
    canDelete: false,
  });
  templates.value = [];
  templateError.value = "";
  comments.value = [];
  history.value = [];
  commentPage.value = historyPage.value = 1;
  commentTotal.value = historyTotal.value = 0;
  ++commentSequence;
  ++historySequence;
  commentsLoading.value = historyLoading.value = false;
  commentsError.value = historyError.value = "";
  selectingFiles.value = richUploading.value = false;
  for (const key of Object.keys(fileCache)) delete fileCache[key];
  if (!props.open || !props.projectId) return;
  const project = props.projectId,
    identifier = props.defectId;
  try {
    if (identifier) {
      const data = await api.detail(project, identifier);
      if (!current(mine)) return;
      Object.assign(draft, {
        title: data.title,
        description: data.description,
        descriptionFormat: data.descriptionFormat,
        status: data.status,
        externalRef: data.externalRef,
        templateId: data.templateId,
        customFields: structuredClone(data.customFields),
        fileIds: data.files.map((f) => f.id),
        expectedRevision: data.revision,
      });
      for (const file of data.files) fileCache[file.id] = file;
      archived.value = data.archived;
      Object.assign(
        capabilities,
        Object.fromEntries(
          ["canRead", "canCreate", "canUpdate", "canDelete"].map((key) => [
            key,
            data[key as keyof DefectCapabilities],
          ]),
        ),
      );
    } else Object.assign(capabilities, props.initialCapabilities);
    if (!current(mine)) return;
    ready.value = true;
    baseline.value = JSON.stringify(body());
    try {
      const data = await api.templates(project);
      if (!current(mine)) return;
      templates.value = data.items;
      if (!identifier && JSON.stringify(body()) === baseline.value) {
        const template = data.items.find((t) => t.isDefault);
        if (template) {
          draft.templateId = template.id;
          Object.assign(draft, template.defaults);
          draft.customFields = Object.fromEntries(
            template.fields.map((f) => [
              f.key,
              JSON.parse(JSON.stringify(f.default)),
            ]),
          );
        }
        baseline.value = JSON.stringify(body());
      }
    } catch (failure) {
      if (current(mine)) {
        templateError.value = "模板读取失败";
        console.error("缺陷模板读取失败", failure);
      }
    }
  } catch (failure) {
    if (current(mine)) {
      error.value = "缺陷读取失败或当前无访问权限，请关闭后重试";
      console.error("缺陷读取失败", failure);
    }
  } finally {
    if (current(mine)) loading.value = false;
  }
}
watch(
  () => [props.open, props.projectId, props.defectId, user.user?.id],
  initialize,
  { immediate: true, flush: "sync" },
);
function selectTemplate(value: string) {
  if (!canWrite.value || busy.value || mediaBusy.value) return;
  const template = templates.value.find((t) => t.id === value);
  const mine = epoch,
    captured = JSON.stringify(body());
  const apply = () => {
    if (!current(mine) || busy.value || captured !== JSON.stringify(body()))
      return;
    draft.templateId = value || null;
    draft.customFields = Object.fromEntries(
      (template?.fields || []).map((f) => [
        f.key,
        JSON.parse(JSON.stringify(f.default)),
      ]),
    );
  };
  if (Object.keys(draft.customFields).length)
    Modal.confirm({
      title: "更换模板并重置自定义字段？",
      okText: "更换",
      onOk: apply,
    });
  else apply();
}
function convertRich() {
  if (!canWrite.value || busy.value || mediaBusy.value) return;
  draft.description = draft.description
    .split("\n")
    .map(
      (line) =>
        "<p>" +
        line
          .replace(/&/g, "&amp;")
          .replace(/</g, "&lt;")
          .replace(/>/g, "&gt;") +
        "</p>",
    )
    .join("");
  draft.descriptionFormat = "rich";
}
async function save() {
  if (
    !canWrite.value ||
    busy.value ||
    mediaBusy.value ||
    loading.value ||
    closing
  )
    return;
  const mine = epoch,
    project = props.projectId,
    input = body(),
    identifier = id.value;
  if (!input.title.trim()) {
    error.value = "请填写缺陷标题";
    return;
  }
  busy.value = true;
  error.value = "";
  try {
    const result = await api.save(project, input, identifier || undefined);
    if (!current(mine)) return;
    id.value = result.id;
    draft.expectedRevision = result.revision;
    baseline.value = JSON.stringify({
      ...input,
      expectedRevision: result.revision,
    });
    message.success("缺陷已保存");
    emit("changed", result.id);
    if (!dirty.value) emit("update:open", false);
  } catch (failure) {
    if (current(mine)) {
      error.value = "保存失败或版本冲突，草稿已保留；请核对后重试";
      console.error("缺陷保存失败", failure);
    }
  } finally {
    if (current(mine)) busy.value = false;
  }
}
async function beforeClose() {
  if (!live || busy.value || mediaBusy.value || closing) return false;
  if (!dirty.value) {
    emit("update:open", false);
    return true;
  }
  const mine = epoch,
    captured = JSON.stringify({ draft: body(), comment: commentDraft });
  closing = true;
  try {
    return await new Promise<boolean>((resolve) =>
      Modal.confirm({
        title: "放弃未保存的缺陷或评论？",
        okText: "丢弃草稿",
        cancelText: "继续编辑",
        onOk() {
          if (
            !current(mine) ||
            busy.value ||
            mediaBusy.value ||
            captured !==
              JSON.stringify({ draft: body(), comment: commentDraft })
          ) {
            resolve(false);
            return;
          }
          emit("update:open", false);
          resolve(true);
        },
        onCancel() {
          resolve(false);
        },
      }),
    );
  } finally {
    if (current(mine)) closing = false;
  }
}
function archive() {
  if (
    !id.value ||
    busy.value ||
    mediaBusy.value ||
    !capabilities.canDelete ||
    dirty.value
  ) {
    if (dirty.value) error.value = "请先保存或放弃草稿，再归档/恢复";
    return;
  }
  const mine = epoch,
    project = props.projectId,
    identifier = id.value,
    revision = draft.expectedRevision,
    target = !archived.value;
  Modal.confirm({
    title: target ? "归档此缺陷？" : "恢复此缺陷？",
    content: "归档保留身份、关系、文件和历史。",
    async onOk() {
      if (
        !current(mine) ||
        busy.value ||
        mediaBusy.value ||
        dirty.value ||
        !capabilities.canDelete
      )
        return;
      busy.value = true;
      try {
        const result = await api.archive(project, identifier, target, revision);
        if (!current(mine)) return;
        archived.value = target;
        adoptRevision(result.revision);
        emit("changed", identifier);
        message.success(target ? "缺陷已归档" : "缺陷已恢复");
        void loadHistory();
      } catch (failure) {
        if (current(mine))
          error.value = "归档/恢复失败或版本冲突，请核对后重试";
      } finally {
        if (current(mine)) busy.value = false;
      }
    },
  });
}
async function pickFiles(target: "details" | "comments") {
  if (
    busy.value ||
    mediaBusy.value ||
    archived.value ||
    (target === "details" ? !canWrite.value : !capabilities.canUpdate)
  )
    return;
  const mine = epoch;
  selectingFiles.value = true;
  try {
    const selected = await filePicker.value?.pick();
    if (!current(mine) || !selected?.length) return;
    const old = target === "details" ? draft.fileIds : commentDraft.fileIds;
    const ids = [...new Set([...old, ...selected.map((f) => f.id)])];
    if (ids.length > 50) {
      error.value = "每次最多关联50个文件，请先移除其他文件";
      return;
    }
    for (const file of selected) fileCache[file.id] = file;
    if (target === "details") draft.fileIds = ids;
    else commentDraft.fileIds = ids;
    pruneFiles();
  } finally {
    if (current(mine)) selectingFiles.value = false;
  }
}
function removeFile(key: string, target: "details" | "comments") {
  if (
    busy.value ||
    mediaBusy.value ||
    archived.value ||
    (target === "details" ? !canWrite.value : !capabilities.canUpdate)
  )
    return;
  if (target === "details")
    draft.fileIds = draft.fileIds.filter((id) => id !== key);
  else commentDraft.fileIds = commentDraft.fileIds.filter((id) => id !== key);
  pruneFiles();
}
async function uploadImage(file: File) {
  const mine = epoch,
    project = props.projectId;
  if (
    !current(mine) ||
    (!capabilities.canUpdate && !canWrite.value) ||
    busy.value ||
    archived.value
  )
    throw Error("当前不可上传");
  const data = await fileLibraryApi.upload(project, file, { image: true });
  if (!current(mine) || !data.src) throw Error("上传上下文已变化");
  return { src: data.src, fileName: data.fileName };
}
async function selectImage() {
  if (busy.value || mediaBusy.value || archived.value) return;
  const mine = epoch;
  selectingFiles.value = true;
  try {
    const rows = await filePicker.value?.pick({ imagesOnly: true, limit: 1 });
    if (!current(mine) || !rows?.[0]?.src) return;
    return { src: rows[0].src, fileName: rows[0].fileName };
  } finally {
    if (current(mine)) selectingFiles.value = false;
  }
}
async function download(file: LibraryFile) {
  const mine = epoch,
    project = props.projectId;
  try {
    const blob = await fileLibraryApi.download(project, file.id);
    if (current(mine)) saveCaseBlob(blob, file.fileName);
  } catch (failure) {
    if (current(mine)) message.error("文件下载失败");
  }
}
async function loadComments() {
  if (!id.value || !ready.value) return;
  const mine = epoch,
    ticket = ++commentSequence;
  commentsLoading.value = true;
  commentsError.value = "";
  try {
    const data = await api.comments(
      props.projectId,
      id.value,
      commentPage.value,
    );
    if (current(mine) && ticket === commentSequence) {
      comments.value = data.items;
      commentTotal.value = data.total;
    }
  } catch (failure) {
    if (current(mine) && ticket === commentSequence)
      commentsError.value = "评论读取失败，请重试";
  } finally {
    if (current(mine) && ticket === commentSequence)
      commentsLoading.value = false;
  }
}
async function loadHistory() {
  if (!id.value || !ready.value) return;
  const mine = epoch,
    ticket = ++historySequence;
  historyLoading.value = true;
  historyError.value = "";
  try {
    const data = await api.history(
      props.projectId,
      id.value,
      historyPage.value,
    );
    if (current(mine) && ticket === historySequence) {
      history.value = data.items;
      historyTotal.value = data.total;
    }
  } catch (failure) {
    if (current(mine) && ticket === historySequence)
      historyError.value = "历史读取失败，请重试";
  } finally {
    if (current(mine) && ticket === historySequence)
      historyLoading.value = false;
  }
}
function changeTab(value: string | number) {
  tab.value = String(value);
  if (tab.value === "comments") void loadComments();
  if (tab.value === "history") void loadHistory();
}
function paginateComments(value: number) {
  commentPage.value = value;
  void loadComments();
}
function paginateHistory(value: number) {
  historyPage.value = value;
  void loadHistory();
}
async function submitComment() {
  if (
    !id.value ||
    busy.value ||
    mediaBusy.value ||
    closing ||
    archived.value ||
    !capabilities.canUpdate
  )
    return;
  const mine = epoch,
    project = props.projectId,
    identifier = id.value,
    input = {
      content: commentDraft.content,
      fileIds: [...commentDraft.fileIds],
      requestId: commentDraft.requestId,
      expectedRevision: draft.expectedRevision,
    };
  if (!input.content.trim()) {
    error.value = "请填写评论内容";
    return;
  }
  busy.value = true;
  try {
    const result = await api.comment(project, identifier, input);
    if (!current(mine)) return;
    adoptRevision(result.revision);
    if (
      commentDraft.content === input.content &&
      JSON.stringify(commentDraft.fileIds) === JSON.stringify(input.fileIds)
    ) {
      commentDraft.content = "";
      commentDraft.fileIds = [];
      pruneFiles();
    }
    commentDraft.requestId = createRequestId();
    message.success("评论已提交");
    emit("changed", identifier);
    await loadComments();
    if (!current(mine)) return;
    void loadHistory();
  } catch (failure) {
    if (current(mine))
      error.value = "评论提交失败或版本冲突，草稿已保留；请核对后重试";
  } finally {
    if (current(mine)) busy.value = false;
  }
}
function removeComment(item: DefectComment) {
  if (busy.value || mediaBusy.value || archived.value || !item.canDelete)
    return;
  const mine = epoch,
    project = props.projectId,
    identifier = id.value,
    cid = item.id,
    revision = draft.expectedRevision;
  Modal.confirm({
    title: "删除此评论？",
    content: "变更历史与文件证据继续保留。",
    async onOk() {
      if (
        !current(mine) ||
        busy.value ||
        mediaBusy.value ||
        archived.value ||
        draft.expectedRevision !== revision
      )
        return;
      busy.value = true;
      try {
        const result = await api.removeComment(
          project,
          identifier,
          cid,
          revision,
        );
        if (!current(mine)) return;
        adoptRevision(result.revision);
        if (comments.value.length === 1 && commentPage.value > 1)
          --commentPage.value;
        await loadComments();
        if (!current(mine)) return;
        void loadHistory();
        emit("changed", identifier);
      } catch (failure) {
        if (current(mine)) error.value = "评论删除失败或版本冲突，请核对后重试";
      } finally {
        if (current(mine)) busy.value = false;
      }
    },
  });
}
function beforeUnload(event: BeforeUnloadEvent) {
  if (dirty.value || busy.value || mediaBusy.value) {
    event.preventDefault();
    event.returnValue = "";
  }
}
onMounted(() => window.addEventListener("beforeunload", beforeUnload));
onBeforeUnmount(() => {
  live = false;
  ++epoch;
  ++commentSequence;
  ++historySequence;
  window.removeEventListener("beforeunload", beforeUnload);
});
onBeforeRouteLeave(beforeClose);
onBeforeRouteUpdate(beforeClose);
defineExpose({ beforeClose });
</script>
<style scoped>
.plain {
  white-space: pre-wrap;
  overflow-wrap: anywhere;
}
.entry {
  margin: 12px 0;
}
.hint {
  font-size: 12px;
  color: #667085;
}
.error {
  color: #b42318;
}
.ant-select {
  width: 100%;
}
</style>
