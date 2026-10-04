<template>
  <div class="ai-page">
    <div class="toolbar">
      <div><h2>AI 辅助</h2><p>分析测试需求，生成用例草稿，审阅后加入项目。</p></div>
      <a-select v-model:value="projectId" aria-label="AI 当前项目" placeholder="选择项目" style="min-width: 220px" :disabled="busy"
        :options="projects.map(p => ({ value: p.id, label: p.name }))" />
    </div>
    <a-alert v-if="!effectiveConfig?.enabled" type="info" show-icon message="尚未启用模型服务" description="请先在模型设置中填写服务地址和模型。未配置时不会生成测试结果或用例。" />
    <a-tabs v-model:activeKey="tab">
      <a-tab-pane key="chat" tab="测试助手">
        <div class="chat-layout">
          <a-card title="我的会话" class="sessions">
            <a-button block @click="newChat" :disabled="busy">新建会话</a-button>
            <a-empty v-if="!sessions.length" description="暂无会话" />
            <div v-for="item in sessions" :key="item.id" class="session-row">
              <a-button type="text" :class="{ active: conversation?.id === item.id }" @click="openChat(item.id)" :disabled="busy">{{ item.title }}</a-button>
              <a-popconfirm title="删除这段会话？" @confirm="removeChat(item.id)"><a-button type="text" danger size="small" :disabled="busy">删除</a-button></a-popconfirm>
            </div>
          </a-card>
          <a-card class="chat-main" title="测试需求与问题分析">
            <a-empty v-if="!conversation?.messages.length" description="输入测试需求、接口说明或错误信息开始对话" />
            <div class="messages" aria-live="polite">
              <div v-for="(item, index) in conversation?.messages" :key="index" class="chat-message" :class="item.role">
                <strong>{{ item.role === 'user' ? '我' : 'ATS 助手' }}</strong><p>{{ item.content }}</p>
              </div>
            </div>
            <a-textarea v-model:value="chatInput" aria-label="发送给 AI 的消息" placeholder="输入需求或问题；仅发送你填写的内容及当前会话上下文" :rows="4" :maxlength="16000" />
            <div class="actions"><a-button type="primary" :loading="busy" :disabled="!projectId || !chatInput.trim() || !effectiveConfig?.enabled" @click="sendChat">发送</a-button></div>
          </a-card>
        </div>
      </a-tab-pane>
      <a-tab-pane key="generate" tab="生成用例">
        <a-card title="从需求生成草稿">
          <a-form layout="vertical">
            <a-form-item label="需求或接口说明" required><a-textarea v-model:value="requirement" :rows="8" :maxlength="24000" placeholder="描述功能、输入约束、预期行为和需要覆盖的边界条件" /></a-form-item>
            <a-space wrap>
              <a-form-item label="用例类型"><a-select v-model:value="caseType" style="width: 150px" :options="caseTypes" /></a-form-item>
              <a-form-item label="生成数量"><a-input-number v-model:value="count" :min="1" :max="20" /></a-form-item>
            </a-space>
            <a-alert message="生成内容保存为待审阅草稿，不会自动执行或直接写入用例库。" type="info" />
            <div class="actions"><a-button type="primary" :loading="busy" :disabled="!projectId || requirement.trim().length < 5 || !effectiveConfig?.enabled" @click="generate">生成用例草稿</a-button></div>
          </a-form>
        </a-card>
      </a-tab-pane>
      <a-tab-pane key="drafts" :tab="`用例草稿（${drafts.filter(d => d.status === 'draft').length}）`">
        <a-card>
          <a-space class="draft-tools"><a-select v-model:value="draftFilter" :options="[{value:'all',label:'全部草稿'},{value:'draft',label:'待审阅'},{value:'imported',label:'已入库'},{value:'dismissed',label:'已放弃'}]" style="width:140px" /><a-button @click="loadProject" :disabled="busy">刷新</a-button></a-space>
          <a-table :data-source="filteredDrafts" row-key="id" :pagination="{ pageSize: 10 }" :scroll="{ x: 650 }">
            <a-table-column title="用例名称" key="name"><template #default="{ record }">{{ record.content.name }}</template></a-table-column>
            <a-table-column title="优先级" key="priority"><template #default="{ record }">{{ record.content.priority }}</template></a-table-column>
            <a-table-column title="状态" key="status"><template #default="{ record }"><a-tag :color="record.status === 'imported' ? 'green' : 'default'">{{ draftLabels[record.status as AIDraft['status']] }}</a-tag></template></a-table-column>
            <a-table-column title="操作" key="actions"><template #default="{ record }"><a-button type="link" @click="editDraft(record)">{{ record.status === 'draft' ? '审阅与编辑' : '查看' }}</a-button></template></a-table-column>
          </a-table>
        </a-card>
      </a-tab-pane>
      <a-tab-pane key="settings" tab="模型设置">
        <a-card title="模型服务">
          <a-alert message="支持 OpenAI 兼容接口，包括提供兼容接口的本地模型。API Key 加密保存，不会回显。" type="info" />
          <a-radio-group v-model:value="scope" class="scope"><a-radio-button value="personal">个人配置</a-radio-button><a-radio-button v-if="canManageSystem" value="system">系统默认配置</a-radio-button></a-radio-group>
          <a-form layout="vertical" class="config-form">
            <a-form-item label="API 基础地址" required><a-input v-model:value="modelForm.base_url" placeholder="例如 http://127.0.0.1:11434/v1" /></a-form-item>
            <a-form-item label="模型名称" required><a-input v-model:value="modelForm.model" placeholder="填写服务实际提供的模型名称" /></a-form-item>
            <a-form-item label="API Key"><a-input-password v-model:value="modelForm.api_key" autocomplete="new-password" :placeholder="modelForm.has_api_key ? '已保存；留空保留原密钥' : '本地无认证服务可留空'" /><a-checkbox v-model:checked="modelForm.clear_api_key">清除已保存的密钥</a-checkbox></a-form-item>
            <a-form-item label="响应超时（秒）"><a-input-number v-model:value="modelForm.timeout_seconds" :min="5" :max="180" /></a-form-item>
            <a-form-item label="启用服务"><a-switch v-model:checked="modelForm.enabled" /></a-form-item>
            <a-space wrap><a-button type="primary" :loading="busy" @click="saveConfig">保存配置</a-button><a-button :loading="busy" @click="testConfig">检测当前生效配置</a-button><a-popconfirm v-if="scope === 'personal'" title="删除个人配置并使用系统默认配置？" @confirm="resetConfig"><a-button :disabled="busy">使用系统默认</a-button></a-popconfirm></a-space>
          </a-form>
          <p class="hint">个人配置优先于系统默认配置。检测会向已保存的模型服务发送一条连接测试消息。</p>
        </a-card>
      </a-tab-pane>
    </a-tabs>
    <a-drawer :open="!!selectedDraft" title="审阅用例草稿" width="min(760px, 100vw)" @close="selectedDraft = null">
      <a-form v-if="selectedDraft" layout="vertical" :disabled="selectedDraft.status !== 'draft' || busy">
        <a-form-item label="名称" required><a-input v-model:value="selectedDraft.content.name" :maxlength="500" /></a-form-item>
        <a-space><a-form-item label="类型"><a-select v-model:value="selectedDraft.content.type" :options="caseTypes" style="width:140px" /></a-form-item><a-form-item label="优先级"><a-select v-model:value="selectedDraft.content.priority" :options="['P0','P1','P2','P3'].map(value => ({value}))" style="width:100px" /></a-form-item></a-space>
        <a-form-item label="前置条件"><a-textarea v-model:value="selectedDraft.content.precondition" :rows="3" /></a-form-item>
        <a-form-item label="关联需求"><a-input v-model:value="selectedDraft.content.requirement_ref" /></a-form-item>
        <a-form-item label="标签"><a-select v-model:value="selectedDraft.content.tags" mode="tags" /></a-form-item>
        <div v-for="(step, i) in selectedDraft.content.steps" :key="i" class="step">
          <strong>步骤 {{ i + 1 }}</strong><a-form-item label="操作" required><a-textarea v-model:value="step.action" :rows="2" /></a-form-item><a-form-item label="预期结果" required><a-textarea v-model:value="step.expected" :rows="2" /></a-form-item>
          <a-button danger size="small" @click="selectedDraft.content.steps.splice(i, 1)" :disabled="selectedDraft.content.steps.length < 2">删除步骤</a-button>
        </div>
        <a-button block @click="selectedDraft.content.steps.push({ action: '', expected: '' })">添加步骤</a-button>
      </a-form>
      <template #footer><a-space v-if="selectedDraft?.status === 'draft'" wrap><a-button :loading="busy" @click="saveDraft">保存草稿</a-button><a-popconfirm title="保存当前编辑并确认加入用例库？" @confirm="acceptDraft"><a-button type="primary" :loading="busy">确认入库</a-button></a-popconfirm><a-popconfirm title="放弃这条草稿？" @confirm="dismissDraft"><a-button danger :disabled="busy">放弃草稿</a-button></a-popconfirm></a-space><a-alert v-else-if="selectedDraft?.status === 'imported'" type="success" message="已加入项目用例库，不会重复导入。" /></template>
    </a-drawer>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, onMounted } from 'vue'
import { message } from 'ant-design-vue'
import { useProjectStore } from '@/stores/project'
import { aiApi, type ModelConfiguration, type Conversation, type AIDraft } from '@/api/aiAssistance'
const projectStore = useProjectStore()
const projects = computed(() => projectStore.projects)
const projectId = ref(''), tab = ref('chat'), busy = ref(false), scope = ref('personal')
const sessions = ref<{id:string;title:string}[]>([]), conversation = ref<Conversation | null>(null), chatInput = ref('')
const requirement = ref(''), count = ref(5), caseType = ref('functional'), draftFilter = ref('all')
const drafts = ref<AIDraft[]>([]), selectedDraft = ref<AIDraft | null>(null)
const personal = ref<ModelConfiguration | null>(null), system = ref<ModelConfiguration | null>(null), canManageSystem = ref(false)
const blankConfig = (): ModelConfiguration => ({base_url:'',model:'',api_key:'',timeout_seconds:60,enabled:false,clear_api_key:false})
const modelForm = ref<ModelConfiguration>(blankConfig())
const effectiveConfig = computed(() => personal.value || system.value)
const filteredDrafts = computed(() => drafts.value.filter(d => draftFilter.value === 'all' || d.status === draftFilter.value))
const draftLabels = {draft:'待审阅',imported:'已入库',dismissed:'已放弃'}
const caseTypes = [{value:'functional',label:'功能测试'},{value:'interface',label:'接口测试'},{value:'ui',label:'UI 测试'},{value:'performance',label:'性能测试'},{value:'security',label:'安全测试'}]
async function action(fn: () => Promise<void>) {
  if(busy.value)return
  busy.value=true
  try { await fn() } catch(error:any) { console.error('AI 操作失败',error);const detail=error?.response?.data?.detail;message.error(typeof detail === 'string' ? detail : '操作失败，请检查输入或服务日志') }
  finally {busy.value=false}
}
function fillConfig(){modelForm.value={...blankConfig(),...(scope.value==='personal'?personal.value:system.value),api_key:'',clear_api_key:false}}
async function loadConfig(){const data=await aiApi.configuration();personal.value=data.personal;system.value=data.system;canManageSystem.value=data.can_manage_system;fillConfig()}
async function loadProject(){const id=projectId.value;if(!id)return;const [list,items]=await Promise.all([aiApi.conversations(id),aiApi.drafts(id)]);if(projectId.value===id){sessions.value=list;drafts.value=items}}
function newChat(){conversation.value=null;chatInput.value=''}
function openChat(id:string){return action(async()=>{conversation.value=await aiApi.conversation(id)})}
function removeChat(id:string){return action(async()=>{await aiApi.removeConversation(id);if(conversation.value?.id===id)newChat();await loadProject()})}
function sendChat(){return action(async()=>{conversation.value=await aiApi.chat({project_id:projectId.value,message:chatInput.value,conversation_id:conversation.value?.id});chatInput.value='';await loadProject()})}
function generate(){return action(async()=>{await aiApi.generate({project_id:projectId.value,requirement:requirement.value,count:count.value,case_type:caseType.value});await loadProject();tab.value='drafts';message.success('草稿已生成，请审阅')})}
function saveConfig(){return action(async()=>{await aiApi.saveConfiguration(scope.value,modelForm.value);await loadConfig();message.success('模型配置已保存')})}
function testConfig(){return action(async()=>{await aiApi.test();message.success('模型服务连接成功')})}
function resetConfig(){return action(async()=>{await aiApi.removePersonal();await loadConfig()})}
function editDraft(item:AIDraft){selectedDraft.value=JSON.parse(JSON.stringify(item))}
function saveDraft(){return action(async()=>{if(!selectedDraft.value)return;selectedDraft.value=await aiApi.updateDraft(selectedDraft.value);await loadProject();message.success('草稿已保存')})}
function acceptDraft(){return action(async()=>{if(!selectedDraft.value)return;selectedDraft.value=await aiApi.updateDraft(selectedDraft.value);selectedDraft.value=await aiApi.accept(selectedDraft.value);await loadProject();message.success('用例已加入当前项目')})}
function dismissDraft(){return action(async()=>{if(!selectedDraft.value)return;selectedDraft.value=await aiApi.dismiss(selectedDraft.value);await loadProject()})}
watch(scope,fillConfig)
watch(projectId,()=>{newChat();sessions.value=[];drafts.value=[];selectedDraft.value=null;action(loadProject)})
onMounted(()=>action(async()=>{await Promise.all([projectStore.fetchProjects(),loadConfig()]);projectId.value=projectStore.currentProject?.id || projects.value[0]?.id || '';await loadProject()}))
</script>

<style scoped>
.ai-page{padding:24px;max-width:1500px;margin:auto}.toolbar{display:flex;justify-content:space-between;align-items:center;gap:16px;margin-bottom:20px}.toolbar h2{margin:0}.toolbar p,.hint{color:#64748b}.chat-layout{display:grid;grid-template-columns:260px 1fr;gap:18px}.sessions{min-width:0}.session-row{display:flex;align-items:center;margin-top:8px}.session-row>:first-child{overflow:hidden;text-overflow:ellipsis;flex:1;text-align:left}.active{background:#e6f4ff}.chat-main{min-width:0}.messages{max-height:50vh;overflow-y:auto}.chat-message{padding:14px 16px;border-radius:8px;margin-bottom:12px;background:#f4f7fa}.chat-message.user{background:#eaf4ff}.chat-message p{white-space:pre-wrap;overflow-wrap:anywhere;margin:8px 0 0}.actions{display:flex;justify-content:flex-end;margin-top:16px}.scope{margin:20px 0}.config-form{max-width:680px}.step{border:1px solid #e2e8f0;padding:16px;border-radius:8px;margin-bottom:14px}.draft-tools{margin-bottom:16px}@media(max-width:850px){.chat-layout{grid-template-columns:1fr}.toolbar{align-items:stretch;flex-direction:column}.ai-page{padding:12px}.sessions{max-height:210px;overflow:auto}}
</style>
