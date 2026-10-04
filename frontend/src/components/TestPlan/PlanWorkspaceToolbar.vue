<template>
  <a-space wrap class="workspace-toolbar">
    <a-tree-select v-model:value="filter.module_id" :tree-data="tree" allow-clear tree-default-expand-all placeholder="全部计划模块" style="width:200px" @change="changed" />
    <a-button @click="editModule()">新建模块</a-button>
    <a-button v-if="filter.module_id" @click="editModule(modules.find(m => m.id === filter.module_id))">编辑模块</a-button>
    <a-popconfirm v-if="filter.module_id" title="删除模块？模块内计划保留。" @confirm="removeModule"><a-button danger>删除模块</a-button></a-popconfirm>
    <a-checkbox v-model:checked="filter.followed" @change="changed">我关注的</a-checkbox>
    <a-checkbox v-model:checked="filter.archived" @change="changed">已归档</a-checkbox>
    <a-input-search v-model:value="filter.tag" placeholder="按标签精确筛选" style="width:160px" @search="changed" />
    <a-button :disabled="!selectedIds.length" @click="batchOpen = true">批量管理（{{ selectedIds.length }}）</a-button>
  </a-space>
  <a-modal v-model:open="moduleOpen" title="计划模块" @ok="saveModule">
    <a-form layout="vertical">
      <a-form-item label="名称" required><a-input v-model:value="moduleForm.name" :maxlength="120" /></a-form-item>
      <a-form-item label="上级模块"><a-tree-select v-model:value="moduleForm.parentId" :tree-data="tree" allow-clear tree-default-expand-all style="width:100%" /></a-form-item>
    </a-form>
  </a-modal>
  <a-modal v-model:open="batchOpen" title="批量管理选中的计划" @ok="saveBatch">
    <a-form layout="vertical">
      <a-form-item label="操作"><a-select v-model:value="batchAction" :options="[{value:'moduleId',label:'移动模块'},{value:'tags',label:'设置标签'},{value:'archived',label:'归档状态'},{value:'groupId',label:'移入计划组'}]" /></a-form-item>
      <a-form-item v-if="batchAction === 'moduleId'" label="目标模块"><a-tree-select v-model:value="batchModule" :tree-data="tree" allow-clear style="width:100%" placeholder="清空则移至未分类" /></a-form-item>
      <a-form-item v-if="batchAction === 'tags'" label="标签（替换已选计划标签）"><a-select v-model:value="batchTags" mode="tags" /></a-form-item>
      <a-form-item v-if="batchAction === 'archived'" label="归档"><a-switch v-model:checked="batchArchived" /></a-form-item>
      <a-form-item v-if="batchAction === 'groupId'" label="计划组"><a-select v-model:value="batchGroup" allow-clear :options="groups.map(g => ({value:g.id,label:g.name}))" /></a-form-item>
    </a-form>
  </a-modal>
</template>
<script setup lang="ts">
import { computed, reactive, ref, watch } from 'vue'
import { message } from 'ant-design-vue'
import { planWorkspaceApi, type PlanModule } from '@/api/planWorkspace'
const props = defineProps<{projectId:string; selectedIds:string[]; groups:{id:string;name:string}[]}>()
const emit = defineEmits<{filter:[value:{module_id?:string;followed:boolean;archived:boolean;tag?:string}];saved:[]}>()
const modules = ref<PlanModule[]>([])
const filter = reactive({ module_id:undefined as string|undefined, followed:false, archived:false, tag:'' })
function changed() { emit('filter',{...filter}) }
const tree = computed(() => { const build = (parent?:string):any[] => modules.value.filter(m => (m.parentId || undefined) === parent).map(m => ({title:m.name,value:m.id,key:m.id,children:build(m.id)})); return build() })
async function load() { if (!props.projectId) return; try { modules.value = await planWorkspaceApi.modules(props.projectId) } catch(error) { console.error('读取计划模块失败',error); message.error('读取计划模块失败') } }
watch(() => props.projectId, () => { filter.module_id=undefined; void load() }, {immediate:true})
const moduleOpen=ref(false), moduleId=ref(''), moduleForm=reactive({name:'',parentId:undefined as string|undefined})
function editModule(module?:PlanModule) { moduleId.value=module?.id || ''; moduleForm.name=module?.name || ''; moduleForm.parentId=module?.parentId; moduleOpen.value=true }
async function saveModule() { try { if(moduleId.value) await planWorkspaceApi.updateModule(moduleId.value,moduleForm); else await planWorkspaceApi.createModule(props.projectId,moduleForm); moduleOpen.value=false; await load(); message.success('模块已保存') } catch(error) {console.error('保存计划模块失败',error);message.error('保存失败，请检查名称及父级')} }
async function removeModule() { try { await planWorkspaceApi.deleteModule(filter.module_id!); filter.module_id=undefined; await load(); changed() } catch(error) {console.error('删除计划模块失败',error);message.error('删除失败，请先处理子模块')} }
const batchOpen=ref(false),batchAction=ref('moduleId'),batchModule=ref<string>(),batchGroup=ref<string>(),batchTags=ref<string[]>([]),batchArchived=ref(true)
async function saveBatch() { const values:Record<string,unknown>={moduleId:batchModule.value || null,groupId:batchGroup.value || null,tags:batchTags.value,archived:batchArchived.value}; try { await planWorkspaceApi.batch(props.projectId,props.selectedIds,{[batchAction.value]:values[batchAction.value]}); batchOpen.value=false; emit('saved'); message.success('计划已批量更新') } catch(error) {console.error('批量更新计划失败',error);message.error('批量更新失败，执行中的计划不能归档')} }
</script>
<style scoped>.workspace-toolbar{padding:12px 0}</style>
