<template>
  <a-space direction="vertical" style="width: 100%">
    <a-space v-if="!hideFollow"
      ><a-button :loading="busy" @click="toggleFollow">{{
        followed ? "取消关注" : "关注用例"
      }}</a-button
      ><span>{{ followCount }} 人关注</span></a-space
    >
    <a-textarea
      v-model:value="content"
      placeholder="添加讨论意见"
      :rows="3"
      :maxlength="10000"
    /><a-button
      type="primary"
      :loading="busy"
      :disabled="!content.trim()"
      @click="post"
      >发表评论</a-button
    >
    <a-list :data-source="comments"
      ><template #renderItem="{ item }"
        ><a-list-item
          ><a-list-item-meta
            :title="`${item.authorId === user.user?.id ? '我' : item.authorId} · ${item.createdAt}`"
            ><template #description
              ><p class="comment-text">{{ item.content }}</p></template
            ></a-list-item-meta
          ><template #actions
            ><a-popconfirm title="删除这条评论？" @confirm="remove(item.id)"
              ><a-button type="link" danger>删除</a-button></a-popconfirm
            ></template
          ></a-list-item
        ></template
      ></a-list
    >
  </a-space>
</template>
<script setup lang="ts">
import { ref, watch } from "vue";
import { caseFeaturesApi as api, type CaseComment } from "@/api/caseFeatures";
import { useUserStore } from "@/stores/user";
const props = defineProps<{ projectId: string; caseId: string; hideFollow?: boolean }>(),
  emit = defineEmits<{ changed: [] }>(),
  user = useUserStore();
const busy = ref(false),
  content = ref(""),
  comments = ref<CaseComment[]>([]),
  followed = ref(false),
  followCount = ref(0);
async function load() {
  try {
    const [rows, state] = await Promise.all([
      api.comments(props.projectId, props.caseId),
      api.followState(props.projectId, props.caseId),
    ]);
    comments.value = rows;
    followed.value = state.followed;
    followCount.value = state.count;
  } catch (error) {
    console.error("加载用例讨论失败", error);
  }
}
async function run(task: () => Promise<unknown>) {
  busy.value = true;
  try {
    await task();
    await load();
    emit("changed");
  } catch (error) {
    console.error("保存用例讨论失败", error);
  } finally {
    busy.value = false;
  }
}
async function toggleFollow() {
  await run(() => api.follow(props.projectId, props.caseId, !followed.value));
}
async function post() {
  if (content.value.trim())
    await run(async () => {
      await api.comment(props.projectId, props.caseId, content.value.trim());
      content.value = "";
    });
}
async function remove(id: string) {
  await run(() => api.deleteComment(props.projectId, props.caseId, id));
}
watch(
  () => [props.projectId, props.caseId],
  () => {
    content.value = "";
    load();
  },
  { immediate: true },
);
</script>
<style scoped>
.comment-text {
  white-space: pre-wrap;
  overflow-wrap: anywhere;
}
</style>
