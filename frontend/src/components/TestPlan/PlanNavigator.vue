<template>
  <aside class="plan-navigator">
    <div class="navigator-tools"><a-input-search v-model:value="keyword" placeholder="搜索模块 / 计划 / 计划组" allow-clear /><a-dropdown-button type="primary" :disabled="!projectId" @click="emit('create-plan')">新建<template #overlay><a-menu><a-menu-item @click="emit('create-group')">测试计划组</a-menu-item></a-menu></template></a-dropdown-button></div>
    <div class="all-plans" :class="{active:selectedKey==='all'}"><button @click="emit('select','all')"><FolderFilled /> 全部测试计划 <span>({{plans.length}})</span></button><a-button type="text" :title="expanded ? '收起全部模块' : '展开全部模块'" @click="toggleExpand"><FolderOpenOutlined /></a-button><a-button type="text" title="添加子模块" :disabled="!projectId" @click="emit('module-action','create')"><PlusOutlined /></a-button></div>
    <a-tree v-model:expanded-keys="expandedKeys" :selected-keys="selectedKey==='all'?[]:[selectedKey]" :tree-data="filtered" block-node @select="select">
      <template #title="node"><div class="navigation-node"><FolderOutlined v-if="node.kind==='module'" /><AppstoreOutlined v-else-if="node.kind==='group'" /><FileTextOutlined v-else /><span class="node-name" :title="node.title">{{node.title}}</span><small v-if="node.kind!=='plan'">({{node.count}})</small><a-dropdown v-if="node.kind!=='plan'" :trigger="['click']"><a-button size="small" type="text" :aria-label="`${node.title}更多操作`" @click.stop><MoreOutlined /></a-button><template #overlay><a-menu v-if="node.kind==='module'"><a-menu-item @click="emit('module-action','create',node.id)">添加子模块</a-menu-item><a-menu-item @click="emit('module-action','edit',node.id)">重命名</a-menu-item><a-menu-item danger @click="emit('module-action','delete',node.id)">删除</a-menu-item></a-menu><a-menu v-else><a-menu-item @click="emit('group-action','edit',node.id)">编辑</a-menu-item><a-menu-item @click="emit('group-action','copy',node.id)">复制</a-menu-item><a-menu-item danger @click="emit('group-action','delete',node.id)">删除</a-menu-item></a-menu></template></a-dropdown></div></template>
    </a-tree>
    <a-empty v-if="!filtered.length" :description="keyword?'没有匹配的模块或计划':'暂无模块或计划'" />
  </aside>
</template>
<script setup lang="ts">
import { computed,ref,watch } from 'vue';
import { FolderFilled,FolderOutlined,FolderOpenOutlined,PlusOutlined,AppstoreOutlined,FileTextOutlined,MoreOutlined } from '@ant-design/icons-vue';
import type { PlanModule } from '@/api/planWorkspace';
import type { PlanGroup } from '@/api/planOrchestration';
import { buildPlanNavigation,filterPlanNavigation,type NavigationPlan,type PlanNavigationNode } from './planNavigation';
const props=defineProps<{projectId?:string;modules:PlanModule[];groups:PlanGroup[];plans:NavigationPlan[];selectedKey:string}>();
const emit=defineEmits<{select:[key:string];'create-plan':[];'create-group':[];'module-action':[action:string,id?:string];'group-action':[action:string,id:string]}>();
const keyword=ref(''),expandedKeys=ref<string[]>([]),expanded=ref(true);
const tree=computed(()=>buildPlanNavigation(props.modules,props.groups,props.plans));
const filtered=computed(()=>filterPlanNavigation(tree.value,keyword.value));
function keys(nodes:PlanNavigationNode[]):string[]{return nodes.flatMap(n=>n.children.length?[n.key,...keys(n.children)]:[])}
function toggleExpand(){expanded.value=!expanded.value;expandedKeys.value=expanded.value?keys(tree.value):[]}
function select(values:any[]){if(values[0])emit('select',String(values[0]))}
watch(tree,()=>{if(expanded.value)expandedKeys.value=keys(tree.value)},{immediate:true});
watch(keyword,()=>{if(keyword.value.trim())expandedKeys.value=keys(filtered.value)});
watch(()=>props.projectId,()=>{keyword.value='';expandedKeys.value=[];expanded.value=true});
</script>
<style scoped>
.plan-navigator{width:300px;min-width:300px;padding:16px;overflow:auto;border-right:1px solid #f0f0f0;background:#fff}
.navigator-tools{display:flex;gap:8px;margin-bottom:16px}.navigator-tools .ant-input-search{min-width:0;flex:1}
.all-plans{display:flex;align-items:center;height:38px;padding-left:4px;margin-bottom:4px;border-radius:4px}.all-plans>button:first-child{flex:1;min-width:0;border:0;background:none;cursor:pointer;text-align:left;padding:0;white-space:nowrap}.all-plans.active{background:#f3e8f7;color:#811fa3}
.navigation-node{display:flex;align-items:center;gap:6px;min-width:0}.node-name{overflow:hidden;text-overflow:ellipsis;white-space:nowrap;flex:1}.navigation-node small{color:#86909c}.navigation-node .ant-btn{opacity:0}.navigation-node:hover .ant-btn,.navigation-node:focus-within .ant-btn{opacity:1}
:deep(.ant-tree-node-content-wrapper){min-width:0;flex:1}:deep(.ant-tree-title){display:block}
@media(max-width:768px){.plan-navigator{width:100%;min-width:0;border-right:0;border-bottom:1px solid #f0f0f0;max-height:250px;flex-shrink:0}}
</style>
