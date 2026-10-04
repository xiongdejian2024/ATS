<template>
  <div>
    <template v-if="!plan.usesTestPointTree">
      <a-table :data-source="legacy" :columns="columns" row-key="id" size="small" :scroll="{x:650}"><template #bodyCell="{column,record}"><a v-if="column.key==='name'" @click="selected=record.id">{{record.name}}</a><a-tag v-else-if="column.key==='status'">{{statusNames[record.executionStatus||'pending']||record.executionStatus}}</a-tag></template></a-table>
    </template>
    <PlanTreeWorkspace :plan-id="plan.id" :project-id="plan.projectId" :category="category" :can-edit="canEdit" @changed="emit('changed')" />
    <a-drawer :open="!!selected" title="关联用例详情" width="min(860px,100vw)" @close="selected=''">
      <TestCaseDetail v-if="selected" :case-id="selected" :project-id="plan.projectId" read-only />
    </a-drawer>
  </div>
</template>
<script setup lang="ts">
import {computed,ref} from 'vue'
import type {TestPlan} from '@/types'
import type {PlanNode} from '@/api/planTree'
import PlanTreeWorkspace from './PlanTreeWorkspace.vue'
import TestCaseDetail from '@/components/TestCase/TestCaseDetail.vue'
const props=defineProps<{plan:TestPlan;category:PlanNode['category'];canEdit:boolean}>(),emit=defineEmits<{changed:[]}>(),selected=ref('')
const legacy=computed(()=>(props.plan.testCases||[]).filter(item=>(['api','scenario'].includes(item.type)?item.type:'functional')===props.category))
const columns=[{title:'用例编号',dataIndex:'caseCode',width:150},{title:'用例名称',key:'name',width:260},{title:'等级',dataIndex:'priority',width:90},{title:'执行结果',key:'status',width:110}]
const statusNames:Record<string,string>={pending:'未执行',pass:'通过',fail:'失败',broken:'阻塞',error:'错误',skip:'跳过'}
</script>
