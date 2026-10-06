<template>
  <div class="test-case-edit">
    <!-- 固定顶部区域 -->
    <div v-if="!embedded" class="edit-header">
      <div class="header-title">
        <span class="title-text">{{ initialDraft ? '复制用例' : isNewCase ? '新建用例' : '编辑用例' }}</span>
        <span v-if="testCase.caseCode" class="sub-title">{{ testCase.caseCode }}</span>
        <span v-else class="sub-title">自动生成编号</span>
      </div>
      <div class="header-actions">
        <a-space>
          <a-button :disabled="loading" @click="handleCancel">取消</a-button>
          <a-button v-if="allowContinue && isNewCase" :loading="saving" :disabled="loading || loadError" @click="handleSave(true)">保存并继续</a-button>
          <a-button type="primary" :loading="saving" :disabled="loading || loadError" @click="handleSave()">
            <template #icon><SaveOutlined /></template>
            保存
          </a-button>
        </a-space>
      </div>
    </div>

    <!-- 可滚动内容区域 -->
    <div class="edit-scroll-content">
      <a-alert v-if="loadError" message="用例加载失败，请重试后编辑" type="error" show-icon><template #action><a-button @click="loadTestCase">重试</a-button></template></a-alert>
      <a-alert v-if="attachmentSaveError" type="warning" show-icon message="用例内容已保存，附件尚未全部保存。再次保存将重试剩余附件，不会重复创建用例。" />
      <a-spin :spinning="loading">
        <a-form
          ref="formRef"
          :model="formData"
          :disabled="loading || saving || loadError"
          :rules="formRules"
          layout="vertical"
        >
        <div class="case-form-columns">
          <section class="case-content-column">
            <a-form-item label="用例名称" name="name"><a-input v-model:value="formData.name" placeholder="请输入用例名称" :maxlength="255" show-count /></a-form-item>
            <a-form-item label="前置条件"><CaseRichText v-model="formData.precondition" label="前置条件" :disabled="loading || saving || loadError" /></a-form-item>
            <div class="description-heading"><span>{{ formData.caseEditType === 'STEP' ? '步骤描述' : '文本描述' }}</span><a-select v-model:value="formData.caseEditType" aria-label="描述方式" :options="[{label:'步骤描述',value:'STEP'},{label:'文本描述',value:'TEXT'}]" style="width:120px" /></div>
            <div v-if="formData.caseEditType === 'STEP'">
          <div class="steps-container">
              <div v-if="formData.steps.length > 0" class="steps-table-wrapper">
              <div class="steps-table-header">
                <div class="sequence-col">序号</div>
                <div class="action-col">用例步骤</div>
                <div class="expected-col">预期结果</div>
                <div class="operations-col">操作</div>
              </div>
              <div class="steps-list">
                <template v-for="(element, index) in formData.steps" :key="element.id || index">
                  <div class="step-row">
                    <div class="sequence-col">
                      <div class="step-sequence">{{ index + 1 }}</div>
                    </div>
                    <div class="action-col">
                      <a-textarea
                        v-model:value="element.action"
                        placeholder="请输入用例步骤"
                        :rows="2"
                        :auto-size="{ minRows: 2, maxRows: 4 }"
                        @blur="updateStepNumber"
                      />
                    </div>
                    <div class="expected-col">
                      <a-textarea
                        v-model:value="element.expected"
                        placeholder="请输入预期结果"
                        :rows="2"
                        :auto-size="{ minRows: 2, maxRows: 4 }"
                        @blur="updateStepNumber"
                      />
                    </div>
                    <div class="operations-col">
                      <a-dropdown :trigger="['click']">
                        <a-button type="text" size="small">
                          <template #icon><MoreOutlined /></template>
                        </a-button>
                        <template #overlay>
                          <a-menu @click="handleStepMenuClick($event, index)">
                            <a-menu-item key="copy">
                              <CopyOutlined />
                              复制
                            </a-menu-item>
                            <a-menu-item key="insertAbove">
                              <ArrowUpOutlined />
                              在上方插入
                            </a-menu-item>
                            <a-menu-item key="insertBelow">
                              <ArrowDownOutlined />
                              在下方插入
                            </a-menu-item>
                            <a-menu-divider />
                            <a-menu-item key="delete" danger>
                              <DeleteOutlined />
                              删除
                            </a-menu-item>
                          </a-menu>
                        </template>
                      </a-dropdown>
                    </div>
                  </div>
                </template>
              </div>
            </div>
            <a-empty
              v-else
              description="暂无测试步骤，请添加"
              :image="false"
            />
            <div class="steps-footer">
              <a-button @click="importSteps">导入步骤</a-button>
              <a-button type="dashed" block @click="addStep">
                <template #icon><PlusOutlined /></template>
                添加步骤
              </a-button>
            </div>
          </div>

            </div>
            <template v-else>
              <a-form-item><CaseRichText v-model="formData.textDescription" label="文本描述" :disabled="loading || saving || loadError" /></a-form-item>
              <a-form-item label="预期结果"><CaseRichText v-model="formData.expectedResult" label="预期结果" :disabled="loading || saving || loadError" /></a-form-item>
            </template>
            <a-form-item label="备注"><CaseRichText v-model="formData.description" label="备注" :disabled="loading || saving || loadError" /></a-form-item>
            <CaseAttachmentDraft ref="attachmentRef" :project-id="projectId" :case-id="caseId" :disabled="loading || saving || loadError" @change="attachmentSignature = $event" />
          </section>
          <aside class="case-fields-column">
            <a-form-item label="内容模板"><a-select v-model:value="templateId" allow-clear placeholder="选择模板" :options="templates.map(t=>({label:t.name+(t.isDefault?'（默认）':''),value:t.id}))" @change="applyTemplate" /></a-form-item>
            <a-form-item label="所属模块" name="moduleId"><a-tree-select v-model:value="formData.moduleId" :tree-data="moduleTreeData" placeholder="请选择模块" :field-names="{label:'title',value:'id',children:'children'}" tree-default-expand-all allow-clear :tree-node-label-prop="'title'" show-search tree-node-filter-prop="title" /></a-form-item>
            <a-form-item label="等级" name="priority"><a-select v-model:value="formData.priority" :options="['P0','P1','P2','P3'].map(p=>({label:p,value:p}))" /></a-form-item>
            <a-form-item label="执行人"><a-select v-model:value="formData.executorId" allow-clear show-search option-filter-prop="label" placeholder="请选择执行人" :options="members" /></a-form-item>
            <CaseCustomFields v-model="customFields" :fields="activeTemplate?.fields || []" />
            <a-form-item label="标签"><a-select v-model:value="formData.tags" mode="tags" placeholder="请输入标签" :token-separators="[',']"><a-select-option v-for="tag in commonTags" :key="tag" :value="tag">{{tag}}</a-select-option></a-select></a-form-item>
            <a-form-item label="用例类型" name="type"><a-select v-model:value="formData.type" @change="nativeTypeChanged" :options="[{label:'功能测试',value:'functional'},{label:'接口测试',value:'interface'},{label:'API用例',value:'api'},{label:'API场景',value:'scenario'},{label:'UI测试',value:'ui'},{label:'性能测试',value:'performance'},{label:'安全测试',value:'security'}]" /></a-form-item>
            <a-form-item label="是否自动化"><a-switch v-model:checked="formData.isAutomated" checked-children="是" un-checked-children="否" /></a-form-item>
            <a-form-item label="需求关联"><a-input v-model:value="formData.requirementRef" placeholder="请输入需求编号或描述" /></a-form-item>
          </aside>
        </div>
        </a-form>
      </a-spin>
    </div>

    <!-- 固定底部区域 -->
    <div v-if="!embedded" class="edit-footer">
      <a-space>
        <a-button :disabled="loading" @click="handleCancel">取消</a-button>
        <a-button v-if="allowContinue && isNewCase" :loading="saving" :disabled="loading || loadError" @click="handleSave(true)">保存并继续</a-button>
          <a-button type="primary" :loading="saving" :disabled="loading || loadError" @click="handleSave()">
          保存
        </a-button>
      </a-space>
    </div>

    <!-- 批量导入步骤对话框 -->
    <a-modal
      v-model:visible="importModalVisible"
      title="批量导入步骤"
      width="800px"
      @ok="handleImportSteps"
      @cancel="importModalVisible = false"
    >
      <a-form layout="vertical">
        <a-form-item label="导入格式">
          <a-radio-group v-model:value="importFormat">
            <a-radio value="text">文本格式</a-radio>
            <a-radio value="table">表格格式</a-radio>
          </a-radio-group>
        </a-form-item>

        <a-form-item label="导入内容">
          <a-textarea
            v-if="importFormat === 'text'"
            v-model:value="importContent"
            placeholder="请输入步骤内容，每行一个步骤，格式：操作描述|预期结果"
            :rows="10"
          />
          <a-table
            v-else
            :data-source="importTableData"
            :columns="importTableColumns"
            :pagination="false"
            size="small"
            bordered
          >
            <template #bodyCell="{ column, record, index }">
              <template v-if="column.key === 'action'">
                <a-input
                  v-model:value="record.action"
                  placeholder="操作描述"
                  @change="handleImportTableChange"
                />
              </template>
              <template v-else-if="column.key === 'expected'">
                <a-input
                  v-model:value="record.expected"
                  placeholder="预期结果"
                  @change="handleImportTableChange"
                />
              </template>
              <template v-else-if="column.key === 'operations'">
                <a-button
                  type="text"
                  size="small"
                  danger
                  @click="removeImportTableRow(index)"
                >
                  <template #icon><DeleteOutlined /></template>
                </a-button>
              </template>
            </template>
          </a-table>
          <a-button
            v-if="importFormat === 'table'"
            type="dashed"
            block
            @click="addImportTableRow"
            style="margin-top: 8px"
          >
            <template #icon><PlusOutlined /></template>
            添加行
          </a-button>
        </a-form-item>
      </a-form>
    </a-modal>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, watch, onMounted, nextTick } from 'vue';
import { SaveOutlined, PlusOutlined, DeleteOutlined, ArrowUpOutlined, ArrowDownOutlined, MoreOutlined, CopyOutlined } from '@ant-design/icons-vue';
import { message } from 'ant-design-vue';
import type { FormInstance, Rule } from 'ant-design-vue/es/form';
import type { TestCase, TestCaseStep } from '@/types';
import { testCaseApi } from '@/api/testCase';
import { projectApi } from '@/api/project';
import CaseAttachmentDraft from './CaseAttachmentDraft.vue'
import CaseRichText from './CaseRichText.vue'
import CaseCustomFields from './CaseCustomFields.vue'
import {caseFeaturesApi,type CaseTemplate} from '@/api/caseFeatures'
import { caseGovernanceApi } from '@/api/caseGovernance'

interface Props {
  embedded?: boolean
  caseId?: string
  copySourceId?: string
  projectId: string
  defaultModuleId?: string  // 默认模块ID（右键创建用例时使用）
  allowContinue?: boolean
  initialDraft?: Partial<TestCase>  // 复制只加载可编辑内容，创建确认前不写库
}

interface Emits {
  (e: 'save', testCase: TestCase, continueCreation?: boolean): void
  (e: 'dirty', value: boolean): void
  (e: 'cancel'): void
}

const props = withDefaults(defineProps<Props>(), {
  caseId: '',
  defaultModuleId: ''
})

const emit = defineEmits<Emits>()

// 响应式数据
const loading = ref(false)
const saving = ref(false)
const loadError = ref(false)
const savedCaseId = ref('')
const attachmentSaveError = ref(false)
const attachmentRef = ref<InstanceType<typeof CaseAttachmentDraft>>()
const attachmentSignature = ref('')
const formRef = ref<FormInstance>()
const testCase = reactive<Partial<TestCase>>({
  id: '',
  name: '',
  type: 'functional',
  priority: 'P2',
  status: 'not_executed',
  tags: [],
  steps: []
})

const formData = reactive({
  name: '',
  type: 'functional' as TestCase['type'],
  priority: 'P2' as TestCase['priority'],
  moduleId: '',
  precondition: '',
  caseEditType: 'STEP' as 'STEP' | 'TEXT',
  textDescription: '',
  expectedResult: '',
  description: '',
  executorId: undefined as string | undefined,
  requirementRef: '',
  tags: [] as string[],
  steps: [] as TestCaseStep[],
  isAutomated: false
})

const templates=ref<CaseTemplate[]>([]),templateId=ref<string>(),customFields=ref<Record<string,unknown>>({})
const activeTemplate=computed(()=>templates.value.find(t=>t.id===templateId.value))
function applyTemplate(){
  const template=activeTemplate.value
  customFields.value=Object.fromEntries((template?.fields||[]).map(f=>[f.key,f.default ?? null]))
  if(template){const defaults=template.defaults; for(const key of ['type','priority','precondition','steps','tags','description'] as const){if(defaults[key]!==undefined)(formData as any)[key]=JSON.parse(JSON.stringify(defaults[key]))}formData.caseEditType=defaults.case_edit_type??defaults.caseEditType??'STEP';formData.textDescription=defaults.text_description??defaults.textDescription??'';formData.expectedResult=defaults.expected_result??defaults.expectedResult??'';formData.isAutomated=defaults.is_automated??defaults.isAutomated??false;updateStepNumber()}
}
async function loadTemplates(){try{templates.value=await caseFeaturesApi.templates(props.projectId);if(!props.caseId){templateId.value=templates.value.find(t=>t.isDefault)?.id;applyTemplate()}}catch(error){console.error('加载编辑模板失败',error)}}

function nativeTypeChanged(value: string) { if (['api', 'scenario'].includes(value)) formData.isAutomated = true }

// 通用标签
const commonTags = ['登录', '注册', '搜索', '支付', '订单', '用户管理', '权限', 'API']

// 模块树数据
const moduleTreeData = ref<any[]>([])
const members = ref<Array<{label:string;value:string}>>([])
async function loadMembers() {
  try {
    const rows = await caseGovernanceApi.reviewers(props.projectId)
    members.value = rows.map(m => ({label: m.name, value: m.id}))
  } catch(error) {console.error('加载用例执行人失败',error)}
}


// 导入步骤相关
const importModalVisible = ref(false)
const importFormat = ref<'text' | 'table'>('text')
const importContent = ref('')
const importTableData = ref<Array<{ action: string; expected: string }>>([
  { action: '', expected: '' }
])

const importTableColumns = [
  { title: '操作描述', dataIndex: 'action', key: 'action' },
  { title: '预期结果', dataIndex: 'expected', key: 'expected' },
  { title: '操作', key: 'operations', width: 80 }
]

// 步骤表格列定义（已移除，改用自定义表格）

// 计算属性
const isNewCase = computed(() => !props.caseId)

// 表单验证规则
const formRules: Record<string, Rule[]> = {
  name: [
    { required: true, message: '请输入用例名称', trigger: 'blur' },
    { min: 1, max: 255, message: '用例名称长度应在1-255个字符之间', trigger: 'blur' }
  ],
  type: [{ required: true, message: '请选择用例类型', trigger: 'change' }],
  priority: [{ required: true, message: '请选择优先级', trigger: 'change' }]
}
const loadTestCase = async () => {
  if (!props.caseId) {
    console.log('新建用例，不需要加载数据')
    loading.value = false
    return
  }

  loading.value = true
  console.log('开始加载用例数据，loading 已设置为 true')

  try {
    loadError.value=false
    console.info('加载测试用例：', { caseId: props.caseId, projectId: props.projectId })
    const data = await testCaseApi.getTestCase(props.projectId, props.caseId)
    console.info('测试用例内容已加载', { caseId: data.id })

    if (!data) {
      throw new Error('用例数据为空')
    }

    Object.assign(testCase, data)
    templateId.value=(data as any).templateId || undefined
    customFields.value=(data as any).customFields || {}

    // 填充表单数据（处理字段名映射：后端可能返回下划线格式）
    formData.name = data.name || ''
    formData.type = data.type || 'functional'
    formData.priority = data.priority || 'P2'
    formData.moduleId = (data.moduleId || '') as string
    formData.precondition = data.precondition || ''
    formData.caseEditType = data.caseEditType || 'STEP'
    formData.textDescription = data.textDescription || ''
    formData.expectedResult = data.expectedResult || ''
    formData.description = data.description || ''
    formData.executorId = data.executorId || undefined
    formData.requirementRef = data.requirementRef || ''
    formData.tags = data.tags || []
    // 为步骤添加唯一ID（如果还没有）
    formData.steps = (data.steps || []).map((step: any, index: number) => ({
      ...step,
      id: step.id || `step-${Date.now()}-${index}-${Math.random().toString(36).substr(2, 9)}`
    }))
    formData.isAutomated = data.isAutomated ?? false

    // 更新步骤编号
    updateStepNumber()

    console.log('用例数据加载完成')
  } catch (error: any) {
    loadError.value=true
    console.error('加载测试用例失败：', error)
    const errorMessage = error?.response?.data?.message || error?.message || '加载用例失败'
    message.error(errorMessage)
  } finally {
    console.info('结束测试用例加载')
    loading.value = false
  }
}

const loadModuleTree = async () => {
  if (!props.projectId) {
    console.warn('缺少项目ID，无法加载模块树')
    return
  }

  try {
    const response = await projectApi.getModules(props.projectId)
    // API 返回格式可能是 { modules: [...], totalCaseCount: ... } 或直接是数组
    const moduleList = response.modules || response || []
    // 转换为树形结构
    moduleTreeData.value = buildTreeData(Array.isArray(moduleList) ? moduleList : [])
  } catch (error) {
    console.error('Failed to load modules:', error)
    // 模块加载失败不影响用例编辑，只记录错误
  }
}

const buildTreeData = (modules: any[]): any[] => {
  const treeMap = new Map()
  const treeData: any[] = []

  // 构建映射（包含原始模块数据）
  modules.forEach(module => {
    treeMap.set(module.id, {
      id: module.id,
      name: module.name,
      title: module.name, // 添加 title 字段用于显示
      parentId: module.parentId || module.parent_id, // 兼容两种字段名
      children: [],
      raw: module
    })
  })

  // 构建模块路径的函数
  const getModulePath = (moduleId: string): string => {
    if (!moduleId || !treeMap.has(moduleId)) {
      return ''
    }

    const pathParts: string[] = []
    let currentId: string | null = moduleId

    // 递归向上查找父模块，构建路径
    const visited = new Set<string>() // 防止循环引用
    while (currentId && treeMap.has(currentId) && !visited.has(currentId)) {
      visited.add(currentId)
      const moduleNode = treeMap.get(currentId)
      pathParts.unshift(moduleNode.name) // 从前面插入，保持顺序
      currentId = moduleNode.parentId || null
    }

    return pathParts.join('/')
  }

  // 为每个模块节点添加路径显示名称
  modules.forEach(module => {
    const node = treeMap.get(module.id)
    const path = getModulePath(module.id)
    // 使用路径作为显示名称，如果路径为空则使用模块名称
    const displayName = path || module.name
    node.name = displayName
    node.title = displayName // 同时设置 title 字段
  })

  // 构建树形结构
  modules.forEach(module => {
    const node = treeMap.get(module.id)
    const parentId = module.parentId || module.parent_id
    if (parentId && treeMap.has(parentId)) {
      treeMap.get(parentId).children.push(node)
    } else {
      treeData.push(node)
    }
  })

  return treeData
}

const handleCancel = () => {
  console.log('取消按钮被点击，当前 loading 状态:', loading.value)
  if (loading.value) {
    console.warn('正在加载中，强制关闭 loading')
    loading.value = false
  }
  emit('cancel')
}

const handleSave = async (continueCreation = false) => {
  if (!formRef.value || saving.value || loading.value || loadError.value) return

  try {
    await formRef.value.validateFields()
    if (!attachmentRef.value?.canSave()) { message.warning('请等待附件加载成功后再保存'); return }
    const missing=(activeTemplate.value?.fields || []).find(f=>f.required && (customFields.value[f.key]===null || customFields.value[f.key]===undefined || customFields.value[f.key]==='' || (Array.isArray(customFields.value[f.key]) && !(customFields.value[f.key] as unknown[]).length)))
    if(missing){message.warning(`请填写自定义字段：${missing.name}`);return}

    saving.value = true

    // 转换字段名：前端使用驼峰，后端使用下划线
    // 确保 module_id 如果是空字符串或无效值，转换为 null
    let moduleIdValue: string | null = null
    if (formData.moduleId && formData.moduleId.trim() !== '') {
      moduleIdValue = formData.moduleId.trim()
    }

    // 处理steps，确保始终是数组格式
    const processedSteps = (formData.steps && Array.isArray(formData.steps) && formData.steps.length > 0)
      ? formData.steps
          .filter(step => step && (step.action || step.expected)) // 过滤掉空的步骤
          .map((step, index) => ({
            step: index + 1, // 重新编号
            action: (step.action || '').trim(),
            expected: (step.expected || '').trim()
          }))
      : []

    const submitData: any = {
      template_id: templateId.value || null,
      custom_fields: customFields.value,
      name: formData.name.trim(),
      type: formData.type || 'functional',
      priority: formData.priority || 'P2',
      module_id: moduleIdValue,  // 保留 null 值
      precondition: formData.precondition && formData.precondition.trim() !== '' ? formData.precondition.trim() : null,
      requirement_ref: formData.requirementRef && formData.requirementRef.trim() !== '' ? formData.requirementRef.trim() : null,
      tags: Array.isArray(formData.tags) ? formData.tags : [],
      case_edit_type: formData.caseEditType,
      text_description: formData.textDescription || null,
      expected_result: formData.expectedResult || null,
      description: formData.description || null,
      executor_id: formData.executorId || null,
      steps: processedSteps,  // 确保始终是数组
      is_automated: formData.isAutomated ?? false
    }

    // 移除 undefined 值，但保留 null 值（因为 module_id 等字段需要 null）
    Object.keys(submitData).forEach(key => {
      if (submitData[key] === undefined) {
        delete submitData[key]
      }
    })

    let result: TestCase
    if (isNewCase.value && !savedCaseId.value) {
      // 调试：打印发送的数据
      console.log('创建测试用例 - projectId:', props.projectId)
      console.info('提交测试用例创建请求', { projectId: props.projectId })
      try {
      result = await testCaseApi.createTestCase(props.projectId, { ...submitData, copy_source_id: props.copySourceId })
      savedCaseId.value = result.id
      } catch (error: any) {
        console.error('创建测试用例失败:', error)
        console.error('错误详情:', error.response?.data)
        if (error.response?.data?.errors) {
          const errorMessages = error.response.data.errors.map((e: any) => `${e.field}: ${e.message}`).join('\n')
          message.error(`创建失败: ${errorMessages}`)
        } else {
          message.error(error.response?.data?.message || '创建失败')
        }
        throw error
      }
    } else {
      result = await testCaseApi.updateTestCase(props.projectId, props.caseId || savedCaseId.value, submitData)
    }

    try {
      await attachmentRef.value.flush(result.id)
      attachmentSaveError.value = false
    } catch (error) {
      attachmentSaveError.value = true
      throw error
    }
    await nextTick()
    message.success(isNewCase.value ? '用例创建成功' : '用例更新成功')
    setDraftBaseline()
    emit('save', result, continueCreation)
  } catch (error) {
    console.error('保存测试用例失败：', error)
    if (error instanceof Error) {
      message.error(error.message || '保存失败')
    }
  } finally {
    saving.value = false
  }
}

const addStep = () => {
  const newStep: TestCaseStep = {
    step: formData.steps.length + 1,
    action: '',
    expected: '',
    id: `step-${Date.now()}-${Math.random().toString(36).substr(2, 9)}` // 添加唯一ID
  } as any
  formData.steps.push(newStep)
  updateStepNumber()
}

// 更新步骤编号
const updateStepNumber = () => {
  formData.steps.forEach((step, index) => {
    step.step = index + 1
  })
}

// 处理步骤操作
const handleStepOperation = (operation: string, index: number) => {
  switch (operation) {
    case 'copy':
      copyStep(index)
      break
    case 'insertAbove':
      insertStepAbove(index)
      break
    case 'insertBelow':
      insertStepBelow(index)
      break
    case 'delete':
      removeStep(index)
      break
  }
}

// 复制步骤
const copyStep = (index: number) => {
  const step = formData.steps[index]
  const newStep: TestCaseStep = {
    step: index + 2,
    action: step.action,
    expected: step.expected
  }
  formData.steps.splice(index + 1, 0, newStep)
  updateStepNumber()
}

// 在上方插入步骤
const insertStepAbove = (index: number) => {
  const newStep: TestCaseStep = {
    step: index + 1,
    action: '',
    expected: ''
  }
  formData.steps.splice(index, 0, newStep)
  updateStepNumber()
}

// 在下方插入步骤
const insertStepBelow = (index: number) => {
  const newStep: TestCaseStep = {
    step: index + 2,
    action: '',
    expected: ''
  }
  formData.steps.splice(index + 1, 0, newStep)
  updateStepNumber()
}

const removeStep = (index: number) => {
  formData.steps.splice(index, 1)
  updateStepNumber()
}

const importSteps = () => {
  importModalVisible.value = true
  importFormat.value = 'text'
  importContent.value = ''
  importTableData.value = [{ action: '', expected: '' }]
}

const handleImportSteps = () => {
  if (importFormat.value === 'text') {
    const lines = importContent.value.split('\n').filter(line => line.trim())
    const steps: TestCaseStep[] = []

    lines.forEach((line, index) => {
      const parts = line.split('|')
      steps.push({
        step: index + 1,
        action: parts[0]?.trim() || '',
        expected: parts[1]?.trim() || ''
      })
    })

    formData.steps = steps
  } else {
    const steps = importTableData.value
      .filter(row => row.action.trim() || row.expected.trim())
      .map((row, index) => ({
        step: index + 1,
        action: row.action,
        expected: row.expected
      }))

    formData.steps = steps
  }

  importModalVisible.value = false
  message.success('步骤导入成功')
}

const addImportTableRow = () => {
  importTableData.value.push({ action: '', expected: '' })
}

const removeImportTableRow = (index: number) => {
  importTableData.value.splice(index, 1)
}

const handleImportTableChange = () => {
  // 过滤空行
  importTableData.value = importTableData.value.filter(
    row => row.action.trim() || row.expected.trim()
  )

  // 如果最后一行不是空行，添加新行
  const lastRow = importTableData.value[importTableData.value.length - 1]
  if (lastRow && (lastRow.action.trim() || lastRow.expected.trim())) {
    importTableData.value.push({ action: '', expected: '' })
  }
}

const draftBaseline = ref('')
const draftSnapshot = () => JSON.stringify({ formData, templateId:templateId.value, customFields:customFields.value, attachmentSignature: attachmentSignature.value })
function setDraftBaseline() { draftBaseline.value=draftSnapshot();emit('dirty',false) }
watch(draftSnapshot, value => { if(draftBaseline.value)emit('dirty',value!==draftBaseline.value) })

// 生命周期
onMounted(async () => {
  // 如果是新建用例，不需要加载数据，直接设置默认值
  if (!props.caseId) {
    loading.value = true
    if (props.defaultModuleId) {
      formData.moduleId = props.defaultModuleId
    }
    // 只加载模块树（用于选择模块）
    await Promise.allSettled([loadModuleTree(), loadTemplates(), loadMembers()])
    if (props.initialDraft) {
      const draft = JSON.parse(JSON.stringify(props.initialDraft))
      Object.assign(formData, { name: draft.name || '', type: draft.type || 'functional', priority: draft.priority || 'P2', moduleId: draft.moduleId || '', precondition: draft.precondition || '', caseEditType: draft.caseEditType || 'STEP', textDescription: draft.textDescription || '', expectedResult: draft.expectedResult || '', description: draft.description || '', executorId: draft.executorId || undefined, requirementRef: draft.requirementRef || '', tags: draft.tags || [], steps: draft.steps || [], isAutomated: draft.isAutomated || false })
      templateId.value = draft.templateId || undefined
      customFields.value = draft.customFields || {}
      updateStepNumber()
      console.info('已加载复制用例草稿，等待用户确认创建')
    }
    setDraftBaseline()
    loading.value=false
    return
  }

  // 编辑用例：并行加载用例数据和模块树，提高加载速度
  // 使用 Promise.allSettled 确保即使一个失败，另一个也能完成
  await Promise.allSettled([
    loadTestCase(),
    loadTemplates(),
    loadModuleTree(),
    loadMembers()
  ])
  setDraftBaseline()
})

// 监听 props 变化
watch(
  () => props.caseId,
  (newCaseId, oldCaseId) => {
    // 只有当 caseId 真正变化时才重新加载
    if (newCaseId && newCaseId !== oldCaseId) {
      loadTestCase()
    } else if (!newCaseId) {
      // 如果变为新建用例，重置表单
      loading.value = false
      Object.assign(formData, {
        name: '',
        type: 'functional',
        priority: 'P2',
        moduleId: props.defaultModuleId || '',
        precondition: '',
        caseEditType: 'STEP', textDescription: '', expectedResult: '', description: '', executorId: undefined,
        requirementRef: '',
        tags: [],
        steps: [],
        isAutomated: false
      })
      templateId.value=templates.value.find(t=>t.isDefault)?.id;applyTemplate()
      updateStepNumber()
    }
  }
)

// 监听 projectId 变化
watch(
  () => props.projectId,
  (newProjectId, oldProjectId) => {
    if (newProjectId && newProjectId !== oldProjectId) {
      // 项目变化时重新加载模块树
      loadModuleTree()
      // 如果有 caseId，重新加载用例
      if (props.caseId) {
        loadTestCase()
      }
    }
  }
)

// 暴露方法给父组件
defineExpose({
  save: handleSave,
  isSaving: () => saving.value,
  canSave: () => !loading.value && !loadError.value,
  resetForm: () => {
    if (formRef.value) {
      formRef.value.resetFields()
    }
    Object.assign(formData, {
      name: '',
      type: 'functional',
      priority: 'P2',
      moduleId: '',
      precondition: '',
      caseEditType: 'STEP', textDescription: '', expectedResult: '', description: '', executorId: undefined,
      requirementRef: '',
      tags: [],
      steps: [],
      isAutomated: false
    })
  }
})
const handleStepMenuClick = (info: { key: string | number }, index: number) => handleStepOperation(String(info.key), index)
</script>

<style scoped>
.case-form-columns{display:grid;grid-template-columns:minmax(0,1fr) 428px;gap:0}
.case-content-column{min-width:0;padding-right:16px;border-right:1px solid #f0f0f0}
.case-fields-column{padding-left:16px;min-width:0}
.description-heading{display:flex;align-items:center;gap:12px;margin-bottom:12px;font-weight:500}
@media(max-width:1000px){.case-form-columns{grid-template-columns:minmax(0,1fr) 300px}}
@media(max-width:768px){.case-form-columns{display:flex;flex-direction:column}.case-content-column{padding-right:0;border-right:0}.case-fields-column{padding-left:0;margin-top:24px}}

.test-case-edit {
  padding: 0;
  background: #fff;
  height: 100%;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.edit-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 24px;
  border-bottom: 1px solid #f0f0f0;
  background: #fff;
  position: sticky;
  top: 0;
  z-index: 10;
  flex-shrink: 0;
}

.header-title {
  display: flex;
  align-items: center;
  gap: 12px;
}

.title-text {
  font-size: 16px;
  font-weight: 500;
  color: rgba(0, 0, 0, 0.85);
}

.sub-title {
  font-size: 14px;
  color: rgba(0, 0, 0, 0.45);
}

.header-actions {
  display: flex;
  align-items: center;
}

/* 可滚动内容区域 */
.edit-scroll-content {
  flex: 1;
  overflow-y: auto;
  overflow-x: hidden;
  padding: 24px;
}

/* 固定底部区域 */
.edit-footer {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  padding: 16px 24px;
  border-top: 1px solid #f0f0f0;
  background: #fff;
  position: sticky;
  bottom: 0;
  z-index: 10;
  flex-shrink: 0;
}

.info-card {
  margin-bottom: 16px;
}

.steps-header {
  margin-bottom: 16px;
  padding-bottom: 16px;
  border-bottom: 1px solid #f0f0f0;
}

.steps-container {
  margin-top: 16px;
}

.steps-footer {
  margin-top: 16px;
}

.steps-table-wrapper {
  margin-bottom: 16px;
  border: 1px solid #f0f0f0;
  border-radius: 4px;
  background: #fff;
  overflow: hidden;
}

.steps-table-header {
  display: flex;
  background-color: #fafafa;
  border-bottom: 1px solid #f0f0f0;
  padding: 12px 16px;
  font-weight: 500;
  color: rgba(0, 0, 0, 0.85);
}

.steps-list {
  display: flex;
  flex-direction: column;
}

.step-row {
  display: flex;
  border-bottom: 1px solid #f0f0f0;
  padding: 12px 16px;
  align-items: flex-start;
  transition: background-color 0.3s;
}

.step-row:hover {
  background-color: #fafafa;
}

.step-row:last-child {
  border-bottom: none;
}

.drag-col {
  width: 40px;
  text-align: center;
  padding: 8px 4px !important;
}

.sequence-col {
  width: 80px;
  text-align: center;
  padding: 8px !important;
}

.action-col {
  width: 40%;
  padding: 8px !important;
}

.expected-col {
  width: 40%;
  padding: 8px !important;
}

.operations-col {
  width: 80px;
  text-align: center;
  padding: 8px !important;
}

.step-sequence {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background-color: #f0f0f0;
  color: #666;
  font-weight: 500;
  font-size: 14px;
}

.drag-handle {
  cursor: move;
  color: #999;
  font-size: 16px;
  padding: 4px;
  transition: color 0.3s;
}

.drag-handle:hover {
  color: #1890ff;
}

.step-row {
  cursor: default;
}

.steps-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.step-item {
  margin-bottom: 16px;
}

.step-item .ant-card-head {
  background: #fafafa;
}

.step-content {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.step-action,
.step-expected {
  padding: 8px 12px;
  background: #f9f9f9;
  border-radius: 4px;
  border-left: 3px solid #1890ff;
}

.step-expected {
  border-left-color: #52c41a;
}

.attachments-header {
  margin-bottom: 16px;
  padding-bottom: 16px;
  border-bottom: 1px solid #f0f0f0;
}

.attachments-list {
  margin-top: 16px;
}

/* 响应式设计 */
@media (max-width: 1200px) {
  .test-case-edit {
    padding: 20px;
  }

  .info-card :deep(.ant-col) {
    margin-bottom: 20px;
  }

  .step-content {
    gap: 12px;
  }
}

@media (max-width: 992px) {
  .test-case-edit {
    padding: 16px;
  }

  .info-card {
    padding: 16px;
  }

  .info-card :deep(.ant-col) {
    margin-bottom: 16px;
  }

  .form-section {
    margin-bottom: 20px;
  }

  .form-section-title {
    font-size: 16px;
    margin-bottom: 12px;
  }
}

@media (max-width: 768px) {
  .test-case-edit {
    padding: 12px;
  }

  .info-card {
    padding: 12px;
    margin-bottom: 12px;
  }

  .info-card :deep(.ant-row) {
    gap: 8px;
  }

  .info-card :deep(.ant-col) {
    width: 100% !important;
    max-width: 100% !important;
    margin-bottom: 8px;
  }

  .form-section {
    margin-bottom: 16px;
  }

  .form-section-title {
    font-size: 15px;
    margin-bottom: 10px;
  }

  .step-content {
    gap: 8px;
  }

  .step-item {
    padding: 8px;
  }

  .step-actions {
    gap: 8px;
  }

  .attachment-upload {
    padding: 12px;
  }

  .attachments-list {
    margin-top: 12px;
  }

  .editor-actions {
    flex-direction: column;
    gap: 8px;
  }

  .editor-actions .ant-btn {
    width: 100%;
  }
}

@media (max-width: 576px) {
  .test-case-edit {
    padding: 8px;
  }

  .info-card {
    padding: 10px;
    margin-bottom: 10px;
  }

  .info-card :deep(.ant-row) {
    flex-direction: column;
    gap: 6px;
  }

  .info-card :deep(.ant-col) {
    margin-bottom: 6px;
  }

  .form-section {
    margin-bottom: 12px;
  }

  .form-section-title {
    font-size: 14px;
    margin-bottom: 8px;
    padding-bottom: 4px;
    border-bottom: 1px solid #f0f0f0;
  }

  .step-item {
    padding: 6px;
    border: 1px solid #f0f0f0;
    border-radius: 4px;
    margin-bottom: 6px;
  }

  .step-actions {
    flex-direction: column;
    gap: 6px;
    margin-top: 8px;
  }

  .step-actions .ant-btn {
    width: 100%;
  }

  .attachment-upload {
    padding: 10px;
  }

  .attachments-list {
    margin-top: 10px;
  }

  .editor-actions {
    margin-top: 16px;
  }

  .info-card :deep(.ant-form-item-label) {
    font-size: 13px;
  }

  .info-card :deep(.ant-input),
  .info-card :deep(.ant-select),
  .info-card :deep(.ant-input-textarea) {
    font-size: 14px;
  }
}
@media (max-width: 768px) {
  .edit-header { flex-wrap:wrap; gap:12px; padding:12px 16px; }
  .header-title { width:100%; min-width:0; flex-shrink:0; }
  .title-text,.sub-title { white-space:nowrap; }
  .header-actions { width:100%; }
  .edit-scroll-content { padding:12px 16px; }
  .info-card :deep(.ant-card-body) { padding:16px; }
}
</style>
