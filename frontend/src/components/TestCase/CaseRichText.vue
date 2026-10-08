<template>
  <div class="case-rich-text" :class="{ readonly }">
    <div
      v-if="editor && !readonly"
      class="rich-toolbar"
      role="toolbar"
      aria-label="富文本格式"
    >
      <a-button
        v-for="action in actions"
        :key="action.key"
        size="small"
        type="text"
        :title="action.label"
        :aria-label="action.label"
        :disabled="disabled"
        :class="{ active: action.active?.() }"
        @click="action.run"
        >{{ action.text }}</a-button
      >
      <a-upload
        v-if="uploadImage"
        :before-upload="insertImage"
        :show-upload-list="false"
        accept="image/png,image/jpeg,image/gif,image/webp"
        :disabled="disabled || uploading"
        ><a-button
          size="small"
          :disabled="disabled || uploading"
          :loading="uploading"
          aria-label="插入图片"
          >图片</a-button
        ></a-upload
      >
      <a-button v-if="selectImage" size="small" :disabled="disabled || uploading" @click="insertLibraryImage">文件库图片</a-button>
      <a-button v-if="projectId" size="small" :disabled="disabled || uploading" @click="insertMention">@ 提及</a-button>
    </div>
    <EditorContent :editor="editor" />
    <MentionMemberPicker v-if="projectId && !readonly" ref="mentionPicker" :project-id="projectId" :context="mentionContext || 'case'" />
  </div>
</template>
<script setup lang="ts">
import { watch, ref, onBeforeUnmount } from "vue";
import { message } from "ant-design-vue";
import Image from "@tiptap/extension-image";
import RichTextImage from "./RichTextImage.vue";
import { useEditor, EditorContent, VueNodeViewRenderer } from "@tiptap/vue-3";
import StarterKit from "@tiptap/starter-kit";
import MentionMemberPicker from './MentionMemberPicker.vue';
import {StructuredMention} from './structuredMention';
const props = defineProps<{
  modelValue?: string;
  readonly?: boolean;
  disabled?: boolean;
  label?: string;
  projectId?: string;
  mentionContext?: 'case'|'plan';
  selectImage?: () => Promise<{src:string;fileName:string} | undefined>;
  uploadImage?: (file: File) => Promise<{ src: string; fileName: string }>;
}>();
const emit = defineEmits<{
  (e: "update:modelValue", value: string): void;
  (e: "uploading", value: boolean): void;
}>();
// 兼容已有纯文本。通过编辑器 schema 解析HTML，不直接向页面注入HTML。
function content(value = "") {
  if (/<\/?[a-z][\s\S]*>/i.test(value)) return value;
  return value
    .split("\n")
    .map(
      (line) =>
        `<p>${line.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")}</p>`,
    )
    .join("");
}
const editor = useEditor({
  extensions: [
    StarterKit.configure({ link: { openOnClick: false } }),
    StructuredMention,
    Image.extend({
      addNodeView() {
        return VueNodeViewRenderer(RichTextImage);
      },
    }),
  ],
  content: content(props.modelValue),
  editable: !props.readonly && !props.disabled,
  editorProps: {
    attributes: {
      role: "textbox",
      "aria-label": props.label || "富文本内容",
      "aria-multiline": "true",
    },
  },
  onUpdate: ({ editor: current }) =>
    emit("update:modelValue", current.isEmpty ? "" : current.getHTML()),
});
defineExpose({ focus: () => editor.value?.commands.focus("end") });
const uploading = ref(false);
const mentionPicker=ref<InstanceType<typeof MentionMemberPicker>>();
let closed = false;
onBeforeUnmount(() => {
  closed = true;
  if(uploading.value)emit('uploading',false);
});
async function insertImage(file: File) {
  if (!props.uploadImage || props.disabled || uploading.value) return false;
  uploading.value = true;
  emit("uploading", true);
  try {
    const image = await props.uploadImage(file);
    if (!closed && editor.value && !editor.value.isDestroyed)
      editor.value
        .chain()
        .focus()
        .setImage({ src: image.src, alt: image.fileName })
        .run();
  } catch (error) {
    console.error("插入富文本图片失败", error);
    message.error("图片上传失败，请重试");
  } finally {
    uploading.value = false;
    if (!closed) emit("uploading", false);
  }
  return false;
}
async function insertLibraryImage() {
  if (!props.selectImage || props.disabled || uploading.value) return;
  uploading.value=true;emit('uploading',true);
  try { const image=await props.selectImage();if(image&&!closed&&editor.value&&!editor.value.isDestroyed)editor.value.chain().focus().setImage({src:image.src,alt:image.fileName}).run() }
  catch(error){message.error('选择文件库图片失败，请重试')}
  finally{uploading.value=false;if(!closed)emit('uploading',false)}
}
async function insertMention(){
  if(!props.projectId||props.disabled||uploading.value)return;
  uploading.value=true;emit('uploading',true);
  const project=props.projectId;
  try{const member=await mentionPicker.value?.pick();if(member&&!closed&&project===props.projectId&&editor.value&&!editor.value.isDestroyed)editor.value.chain().focus().insertContent([{type:'structuredMention',attrs:{id:member.id,label:member.label}},{type:'text',text:' '}]).run()}
  finally{uploading.value=false;if(!closed)emit('uploading',false)}
}
const actions = [
  {
    key: "bold",
    label: "加粗",
    text: "B",
    active: () => editor.value?.isActive("bold"),
    run: () => editor.value?.chain().focus().toggleBold().run(),
  },
  {
    key: "italic",
    label: "斜体",
    text: "I",
    active: () => editor.value?.isActive("italic"),
    run: () => editor.value?.chain().focus().toggleItalic().run(),
  },
  {
    key: "underline",
    label: "下划线",
    text: "U",
    active: () => editor.value?.isActive("underline"),
    run: () => editor.value?.chain().focus().toggleUnderline().run(),
  },
  {
    key: "strike",
    label: "删除线",
    text: "S",
    active: () => editor.value?.isActive("strike"),
    run: () => editor.value?.chain().focus().toggleStrike().run(),
  },
  {
    key: "bullet",
    label: "无序列表",
    text: "• 列表",
    active: () => editor.value?.isActive("bulletList"),
    run: () => editor.value?.chain().focus().toggleBulletList().run(),
  },
  {
    key: "ordered",
    label: "有序列表",
    text: "1. 列表",
    active: () => editor.value?.isActive("orderedList"),
    run: () => editor.value?.chain().focus().toggleOrderedList().run(),
  },
  {
    key: "quote",
    label: "引用",
    text: "引用",
    active: () => editor.value?.isActive("blockquote"),
    run: () => editor.value?.chain().focus().toggleBlockquote().run(),
  },
  {
    key: "code",
    label: "代码块",
    text: "</>",
    active: () => editor.value?.isActive("codeBlock"),
    run: () => editor.value?.chain().focus().toggleCodeBlock().run(),
  },
  {
    key: "undo",
    label: "撤销",
    text: "↶",
    run: () => editor.value?.chain().focus().undo().run(),
  },
  {
    key: "redo",
    label: "重做",
    text: "↷",
    run: () => editor.value?.chain().focus().redo().run(),
  },
];
watch(
  () => props.modelValue,
  (value) => {
    if (editor.value && editor.value.getHTML() !== content(value))
      editor.value.commands.setContent(content(value), { emitUpdate: false });
  },
);
watch(
  () => [props.readonly, props.disabled],
  () => editor.value?.setEditable(!props.readonly && !props.disabled),
);
</script>
<style scoped>
.case-rich-text {
  border: 1px solid #d9d9d9;
  border-radius: 4px;
  background: #fff;
  overflow: hidden;
}
.rich-toolbar {
  display: flex;
  flex-wrap: wrap;
  padding: 4px;
  border-bottom: 1px solid #f0f0f0;
  background: #fafafa;
  gap: 2px;
}
.rich-toolbar .active {
  color: var(--primary-color);
  background: var(--ms-primary-soft);
}
.case-rich-text :deep(.tiptap) {
  min-height: 100px;
  padding: 12px;
  outline: none;
  white-space: pre-wrap;
  overflow-wrap: anywhere;
}
.case-rich-text :deep(.tiptap p) {
  margin: 0 0 8px;
}
.case-rich-text :deep(.structured-mention){color:var(--primary-color);background:var(--ms-primary-soft);border-radius:3px;padding:1px 3px;white-space:nowrap}
.case-rich-text :deep(.tiptap p:last-child) {
  margin-bottom: 0;
}
.case-rich-text :deep(.tiptap pre) {
  background: #f5f5f5;
  padding: 8px;
  white-space: pre-wrap;
}
.case-rich-text :deep(.tiptap blockquote) {
  border-left: 3px solid #d9d9d9;
  padding-left: 12px;
  color: #666;
}
.readonly {
  border: 0;
}
.readonly :deep(.tiptap) {
  min-height: 0;
  padding: 0;
}
</style>
