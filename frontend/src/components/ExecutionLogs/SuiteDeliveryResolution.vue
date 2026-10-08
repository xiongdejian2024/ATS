<template>
  <div v-if="delivery || error" class="suite-delivery">
    <a-alert v-if="error" type="error" :message="error"><template #action><a-button :disabled="busy" @click="refresh">刷新</a-button></template></a-alert>
    <template v-if="delivery">
    <a-alert v-if="delivery.closedBy" type="warning" show-icon message="未知结果已人工关闭，未重跑" :description="delivery.reason || ''" />
    <template v-else-if="delivery.deliveryState === 'unknown'">
      <a-alert type="warning" show-icon message="本次执行状态未知，运行槽仍保留" description="请在节点上核对本次执行。关闭记录不终止进程，不代表执行成功，也不会自动重跑。" />
      <template v-if="delivery.canResolve">
        <a-checkbox v-model:checked="confirmed" :disabled="busy">已核对本次执行未启动，或所有相关进程均已停止</a-checkbox>
        <a-textarea v-model:value="reason" :maxlength="2000" :rows="2" placeholder="填写核对方式和结果" :disabled="busy" />
        <a-button :disabled="!confirmed || !reason.trim()" :loading="busy" @click="close">核对后关闭未知执行</a-button>
      </template>
      <p v-else>本次执行属于计划或定时批次，请到对应批次入口核对。</p>
    </template>
    </template>
  </div>
</template>
<script setup lang="ts">
import { watch } from 'vue'
import { message } from 'ant-design-vue'
import { useSuiteDelivery } from './useSuiteDelivery'
import { useUserStore } from '@/stores/user'
const props = defineProps<{ suiteId: string; executionId: string }>()
const user = useUserStore()
const { delivery, confirmed, reason, busy, error, open, resolve, refresh } = useSuiteDelivery()
async function close() {
  if (await resolve()) message.success('未知结果已人工关闭，未重跑')
}
watch(() => [props.suiteId, props.executionId, user.user?.id], () => open(props.suiteId, props.executionId), { immediate: true })
</script>
<style scoped>.suite-delivery{display:flex;flex-direction:column;gap:8px;margin-bottom:12px;flex-shrink:0}</style>
