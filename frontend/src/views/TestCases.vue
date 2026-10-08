<template>
  <div class="test-cases-container" @click="hideModuleContextMenu">
    <a-layout class="test-cases-layout">
      <!-- 左侧模块树 -->
      <a-layout-sider v-show="showModules" width="240" class="module-tree-sider">
        <div class="module-tree-body">
        <a-input-search
          v-model:value="moduleSearchValue"
          placeholder="请输入模块名称"
          class="module-search"
          @search="handleModuleSearch"
        />

        <a-tree
          :tree-data="moduleTreeData"
          :selected-keys="recycleVisible ? [] : selectedModuleKeys"
          :expanded-keys="expandedModuleKeys"
          block-node
          show-icon
          multiple
          draggable
          :allow-drop="allowModuleDrop"
          @select="handleModuleSelect"
          @expand="handleModuleExpand"
          @rightClick="handleModuleRightClick"
          @drop="handleModuleDrop"
        >
          <template #title="{ title, count, nodeType, key: nodeKey }">
            <span class="tree-node-title" :class="{ 'root-module-title': nodeKey === 'all' }">
              {{ title }}
              <span v-if="count !== undefined && nodeType !== 'case'" class="count-badge">({{ count }})</span>
              <a-space v-if="nodeKey === 'all'" :size="0" class="root-module-actions" @click.stop>
                <a-button type="text" size="small" :title="expandedModuleKeys.length ? '收起全部模块' : '展开全部模块'" aria-label="展开或收起全部模块" @click="expandedModuleKeys = expandedModuleKeys.length ? [] : modules.map(m => m.id)"><FolderOutlined /></a-button>
                <a-button type="text" size="small" aria-label="新建根模块" @click="handleAddModule({ key: 'all' })"><PlusOutlined /></a-button>
              </a-space>
            </span>
          </template>
          <template #icon="{ nodeType, isLeaf }">
            <FolderOutlined v-if="nodeType === 'module'" style="color: #faad14" />
            <FileTextOutlined v-else-if="nodeType === 'case'" style="color: #1890ff" />
            <FileOutlined v-else-if="isLeaf" />
            <FolderOutlined v-else style="color: #faad14" />
          </template>
        </a-tree>

        <!-- 模块/用例树右键菜单 -->
        <div
          v-if="moduleContextMenu.visible"
          class="module-context-menu"
          :style="{ left: moduleContextMenu.x + 'px', top: moduleContextMenu.y + 'px' }"
          @click.stop
        >
          <a-menu @click="handleModuleContextMenuClick">
            <!-- 虚拟节点只显示新增操作 -->
            <template v-if="contextMenuNodeType === 'virtual'">
              <a-menu-item key="addModule">新增模块</a-menu-item>
              <a-menu-item key="addCase">新增用例</a-menu-item>
              <a-menu-divider />
              <a-menu-item key="export">导出用例</a-menu-item>
            </template>
            <!-- 模块节点显示全部操作 -->
            <template v-else-if="contextMenuNodeType === 'module'">
              <a-menu-item key="addModule">新增子模块</a-menu-item>
              <a-menu-item key="addCase">新增用例</a-menu-item>
              <a-menu-divider />
              <a-menu-item key="export">导出用例</a-menu-item>
              <a-menu-divider />
              <a-menu-item key="rename">重命名</a-menu-item>
              <a-menu-item key="delete">删除</a-menu-item>
              <a-menu-divider v-if="selectedModuleKeys.length > 1" />
              <a-menu-item v-if="selectedModuleKeys.length > 1" key="batchDelete">
                批量删除所选模块
              </a-menu-item>
            </template>
            <!-- 用例节点只显示删除操作 -->
            <template v-else-if="contextMenuNodeType === 'case'">
              <a-menu-item key="deleteCase">删除用例</a-menu-item>
            </template>
          </a-menu>
        </div>
        </div>
        <button class="recycle-module-entry" :class="{ active: recycleVisible }" @click="openRecycle"><DeleteOutlined /><span>回收站</span><span class="recycle-total">{{ recycleTotal }}</span></button>
      </a-layout-sider>

      <!-- 右侧主内容区 -->
      <a-layout-content class="cases-content">
        <div v-if="!recycleVisible" class="fixed-toolbar">
          <div class="toolbar-create">
            <a-button v-if="isNarrowScreen" @click="showModules=!showModules">{{showModules?'收起模块':'模块'}}</a-button>
            <a-button type="primary" @click="handleCreateCase">新建</a-button>
            <a-button @click="handleImport">导入</a-button>
          </div>
          <div class="toolbar-filter">
            <a-input-search v-if="!isAdvancedSearchMode" v-model:value="searchValue" placeholder="通过ID/名称/标签搜索" style="width:187px" allow-clear @search="handleSearch" />
            <CaseGovernancePanel v-if="projectId" ref="governancePanel" :project-id="projectId" :selected-ids="selectedRowKeys" :selection="selection.request.value" :selected-count="selection.count.value" :selection-ready="selection.ready.value" :after-selection-change="finishSelectionChange" @busy-change="selection.working.value=$event" :filters="savedViewFilters" :system-view="viewMode" :filter-saving="filterSaving" @new-view="openFilter(true)" @system-view="applySystemView" @changed="refreshGovernedCases" @apply-view="applySavedView" />
            <a-button aria-label="高级筛选" :type="isAdvancedSearchMode ? 'primary' : 'default'" @click="openFilter(false)"><FilterOutlined /> 筛选</a-button>
            <a-button v-if="isAdvancedSearchMode" aria-label="清空高级筛选" type="link" @click="clearAdvancedFilters">清空筛选</a-button>
            <a-button-group>
              <a-button :type="viewLayout === 'list' ? 'primary' : 'default'" aria-label="列表视图" title="列表视图" @click="changeViewLayout('list')"><UnorderedListOutlined /></a-button>
              <a-button :type="viewLayout === 'mind' ? 'primary' : 'default'" aria-label="脑图视图" title="脑图视图" @click="changeViewLayout('mind')"><AppstoreOutlined /></a-button>
            </a-button-group>
            <a-button aria-label="刷新用例" title="刷新" @click="refreshGovernedCases"><ReloadOutlined /></a-button>
          </div>
        </div>
        <div v-if="!recycleVisible" class="table-heading">
          <span class="module-heading">{{ tableTitle }}</span>
          <a-space :size="4">
            <a-dropdown><a-button type="text" aria-label="用例更多操作" title="更多操作"><MoreOutlined /></a-button><template #overlay><a-menu><a-menu-item @click="handleExport({key:'excel'})">导出 Excel</a-menu-item><a-menu-item @click="handleExport({key:'xmind'})">导出 XMind</a-menu-item><a-menu-item @click="templateVisible=true">模板字段</a-menu-item></a-menu></template></a-dropdown>
            <a-button v-if="viewLayout === 'list'" type="text" aria-label="用例表格设置" title="表格设置" @click="columnSettingVisible=true"><SettingOutlined /></a-button>
          </a-space>
        </div>

        <!-- 可滚动内容区域 -->
        <div class="scrollable-table-content">
          <!-- 表格 -->
          <CaseRecycleBin v-if="recycleVisible" :project-id="projectId" :open="true" embedded @changed="refreshGovernedCases" @total="recycleTotal = $event" @close="recycleVisible = false" />
          <CaseMindMap v-else-if="viewLayout === 'mind'" ref="mindMap" :scope-key="mindScope" :cases="testCases" :modules="modules" :saving="mindSaving" :persist-edit="saveMindNode" :persist-create="createMindCase" :persist-rename="renameMindModule" :persist-create-module="createMindModule" :persist-move="moveMindNode" :persist-delete="deleteMindNode" @create="createMindCase" @select="handleViewCase($event as TestCase)" />
          <a-card v-else class="table-card">
            <a-table
              :columns="columns"
              :data-source="testCases"
              :loading="loading"
              :row-selection="rowSelection"
              :pagination="false"
              row-key="id"
              :scroll="{ x: tableWidth }"
              @resizeColumn="resizeColumn"
              @change="handleTableChange"
              size="middle"
            >
            <template #bodyCell="{ column, record, index }">
              <template v-if="column.key === 'id'">
                <a @click="handleViewCase(record)" class="case-link">{{ getCaseDisplayId(record, index) }}</a>
              </template>

              <template v-else-if="column.key === 'name'">
                <div style="display: flex; align-items: center; gap: 8px;">
                  <BugOutlined v-if="record.type === 'bug'" style="color: #ff4d4f" />
                  <ThunderboltOutlined v-else-if="record.type === 'interface'" style="color: #1890ff" />
                  <AppstoreOutlined v-else-if="record.type === 'ui'" style="color: #722ed1" />
                  <FileTextOutlined v-else style="color: #8c8c8c" />
                  <a-typography-text :editable="{onChange:(value:string)=>saveInline(record,'name',value)}" :title="record.name">{{record.name}}</a-typography-text>
                </div>
              </template>

              <template v-else-if="column.key === 'level'">
                <a-select :value="record.priority" :bordered="false" class="inline-case-level" :aria-label="`修改用例 ${record.caseCode} 等级`" @change="(value: string) => saveInline(record,'priority',value)">
                  <a-select-option v-for="level in ['P0','P1','P2','P3']" :key="level" :value="level"><FlagOutlined :style="{ color: getLevelColor(level) }" /> {{ level }}</a-select-option>
                </a-select>
              </template>

              <template v-else-if="column.key === 'reviewResult'">
                <a-tag :color="getReviewResultColor((record as any).reviewResult || 'not_reviewed')">
                  <template #icon>
                    <CheckSquareOutlined v-if="(record as any).reviewResult === 'passed'" />
                  </template>
                  {{ getReviewResultLabel((record as any).reviewResult || 'not_reviewed') }}
                </a-tag>
              </template>

              <template v-else-if="column.key === 'executionResult'">
                {{ executionResultLabel(record.status) }}
              </template>

              <template v-else-if="column.key === 'modulePath'">
                <a-tree-select :value="record.moduleId || '__unassigned__'" :tree-data="moduleSelectTree" :field-names="{value:'key',label:'title',children:'children'}" :bordered="false" show-search tree-node-filter-prop="title" class="inline-case-module" :aria-label="`修改用例 ${record.caseCode} 模块`" @change="(value: string) => saveInline(record,'moduleId',value === '__unassigned__' ? null : value)" />
              </template>

              <template v-else-if="column.key === 'tags'">
                <span v-if="(record.tags || []).length === 0">-</span>
                <a-space v-else wrap :size="2">
                  <a-tag v-for="tag in (record.tags || []).slice(0, 2)" :key="tag" size="small">
                    <TagOutlined /> {{ tag }}
                  </a-tag>
                  <a-tag v-if="(record.tags || []).length > 2" size="small" color="default">
                    +{{ (record.tags || []).length - 2 }}
                  </a-tag>
                </a-space>
              </template>

              <template v-else-if="column.key === 'isAutomated'">
                <div v-if="(record.isAutomated ?? record.is_automated)" style="color: #52c41a">
                  <CodeOutlined /> 是
                </div>
                <div v-else style="color: #bfbfbf">
                  <BlockOutlined /> 否
                </div>
              </template>

              <template v-else-if="column.key === 'createdBy'">
                {{ getDisplayName(record.createdBy) }}
              </template>

              <template v-else-if="column.key === 'createdAt'">
                {{ formatDateTime(record.createdAt) }}
              </template>

              <template v-else-if="column.key === 'updatedBy'">
                {{ getDisplayName(record.updatedBy || record.createdBy) }}
              </template>

              <template v-else-if="column.key === 'updatedAt'">
                {{ formatDateTime(record.updatedAt) }}
              </template>

              <template v-else-if="column.key === 'actions'">
                <a-space>
                  <a-button type="link" size="small" @click="handleEditCase(record)">
                    编辑
                  </a-button>
                  <a-button type="link" size="small" @click="handleCopyCase(record)">
                    复制
            </a-button>
            <a-dropdown>
                    <a-button type="link" size="small">
                      <template #icon><MoreOutlined /></template>
              </a-button>
              <template #overlay>
                      <a-menu>
                        <a-menu-item key="delete" @click="handleDeleteCase(record)">
                          删除
                        </a-menu-item>
                        <a-menu-item key="execute" @click="handleExecuteCase(record)">
                          执行
                        </a-menu-item>
                        <a-menu-item key="versions" @click="governancePanel?.openVersions(record.id)">版本与比较</a-menu-item>
                </a-menu>
              </template>
            </a-dropdown>
          </a-space>
              </template>
            </template>
          </a-table>
        </a-card>
        </div>

        <!-- 固定底部分页器和批量操作栏 -->
        <div v-if="!recycleVisible" class="fixed-footer">
          <!-- 批量操作栏 -->
          <div v-if="selection.hasSelection.value" class="batch-actions">
            <a-alert v-if="selection.error.value" :message="selection.error.value" type="error" show-icon><template #action><a-button :loading="selection.loading.value" @click="selection.preview">重试核对选择范围</a-button></template></a-alert>
            <a-space wrap>
              <span aria-label="用例选择数量">{{selection.loading.value ? '正在核对选择范围…' : selection.count.value === undefined ? '选择范围未确认' : `已选择 ${selection.count.value} 条`}}</span>
              <a-dropdown :disabled="!selection.ready.value || !selection.permissions.value.export">
                <a-button :disabled="!selection.ready.value || !selection.permissions.value.export">
                  导出
                  <template #icon><DownOutlined /></template>
                </a-button>
                <template #overlay>
                  <a-menu @click="handleExport">
                    <a-menu-item key="excel">导出 Excel 格式 (xlsx)</a-menu-item>
                    <a-menu-item key="xmind">导出思维导图 (xmind)</a-menu-item>
                  </a-menu>
                </template>
              </a-dropdown>
              <a-button :disabled="!selection.ready.value || !selection.permissions.value.update" @click="handleBatchEdit">编辑</a-button>
              <a-button :disabled="!selection.ready.value || !selection.permissions.value.update" @click="handleBatchMove">移动到</a-button>
              <a-button :disabled="!selection.ready.value || !selection.permissions.value.create" @click="handleBatchCopy">复制到</a-button>
              <a-button :disabled="!selection.ready.value || !selection.permissions.value.update" @click="governancePanel?.openIssueLinks()">关联需求 / 缺陷</a-button>
              <a-button :disabled="!selection.ready.value || !selection.permissions.value.update" @click="governancePanel?.openCreateReview()">发起评审</a-button>
              <a-dropdown>
                <a-button>
                  <template #icon><MoreOutlined /></template>
                </a-button>
                <template #overlay>
                  <a-menu>
                    <a-menu-item key="delete" :disabled="!selection.ready.value || !selection.permissions.value.delete" @click="handleBatchDelete">批量删除</a-menu-item>
                  </a-menu>
                </template>
              </a-dropdown>
              <a-button :disabled="selection.working.value" @click="clearSelection">清空</a-button>
            </a-space>
          </div>
          <!-- 分页器 -->
          <a-pagination
            v-model:current="pagination.current"
            v-model:page-size="pagination.pageSize"
            :total="pagination.total"
            :show-size-changer="true"
            :page-size-options="pageSizes.map(String)"
            :show-quick-jumper="true"
            :show-total="paginationTotal"
            @change="handlePaginationChange"
            @show-size-change="handlePaginationChange"
            style="flex: 1; display: flex; justify-content: flex-end;"
          />
        </div>
      </a-layout-content>
    </a-layout>
  <TableDisplaySettings :open="columnSettingVisible" :definitions="displayDefinitions" :columns="tableDisplay.columns" :page-size="pagination.pageSize" :include-descendants="tableDisplay.includeDescendants" :error="tableSettingsError" show-mode @close="saveTableColumns" @page-size-change="setTablePageSize" @descendants-change="setSubdirectory" />

    <!-- 详情抽屉 -->
    <a-drawer
      :open="detailCaseVisible"
      @close="closeDetail"
      :title="viewingCaseId ? '用例详情' : ''"
      :width="detailFullscreen ? '100vw' : 'min(860px, 96vw)'"
      :body-style="{padding:'16px'}"
      placement="right"
      :mask="false"
      :mask-closable="true"
      :destroy-on-close="true"
      :closable="true"
    >
      <template #extra><a-space><a-button aria-label="上一条用例" :disabled="!canPreviousCase" @click="navigateDetail(-1)"><LeftOutlined /></a-button><a-button aria-label="下一条用例" :disabled="!canNextCase" @click="navigateDetail(1)"><RightOutlined /></a-button><a-button @click="detailFullscreen=!detailFullscreen">{{detailFullscreen ? '退出全屏':'全屏'}}</a-button></a-space></template>
      <TestCaseDetail
        ref="detailPanel"
        v-if="viewingCaseId"
        :case-id="viewingCaseId"
        :project-id="projectId"
        @edit="handleEditFromDetail"
        @copy="copyFromDetail"
        @delete="deleteFromDetail"
        @navigate="navigateDetailTo"
      />
    </a-drawer>

    <!-- 筛选抽屉 -->
    <TestCaseFilter
      v-model:visible="filterDrawerVisible"
      :available-fields="filterFields"
      :metadata-error="filterFieldError"
      :metadata-loading="filterFieldLoading"
      @retry-fields="loadFilterFields"
      :conditions="advancedFilters"
      :logic="filterLogic"
      :module-tree-data="moduleTreeData"
      @apply="handleFilterApply"
      :view="newFilterView ? undefined : governancePanel?.activeView"
      :view-names="governancePanel?.viewNames"
      :cannot-add="governancePanel?.cannotAdd"
      :new-view="newFilterView"
      :system-view="viewMode"
      :save-view="saveFilterView"
      @saving="filterSaving=$event"
    />

    <CaseExportDialog v-model:open="exportVisible" :initial-format="exportFormat" :busy="exportBusy" :selected-count="selection.count.value || 0" @export="confirmExport" />
    <CaseTemplateManager :project-id="projectId" v-model:open="templateVisible" @changed="loadFilterFields" />
    <!-- 导入用例对话框 -->
    <ImportCasesModal
      v-model:visible="importModalVisible"
      :project-id="projectId"
      @success="handleImportSuccess"
    />
  </div>
  <a-modal v-model:visible="caseExecutionVisible" title="执行所选单用例" @ok="confirmCaseExecution" :confirm-loading="caseExecutionLoading">
    <p>{{ executionCase?.name }}：仅执行这个用例，复用所选模板的环境和命令。</p>
    <a-select v-model:value="selectedExecutionTemplate" style="width:100%" placeholder="选择已有执行模板">
      <a-select-option v-for="suite in executionTemplates" :key="suite.id" :value="suite.id">{{ suite.name }}</a-select-option>
    </a-select>
    <a-empty v-if="!caseExecutionLoading && !executionTemplates.length" description="没有包含该用例的 XAT任务，请先在测试任务中配置" />
  </a-modal>
</template>

<script setup lang="ts">
import { testSuiteApi, type TestSuite } from '@/api/testSuite'
import { testPlanApi } from '@/api/testPlan'
import { ref, reactive, computed, onMounted, onUnmounted, watch, createVNode } from 'vue';
import { useRoute, useRouter, onBeforeRouteLeave, onBeforeRouteUpdate } from 'vue-router';
import { message, Modal, Input } from 'ant-design-vue';
import { LeftOutlined, RightOutlined, PlusOutlined, FilterOutlined, UnorderedListOutlined, AppstoreOutlined, ReloadOutlined, MoreOutlined, DownOutlined, FolderOutlined, FileOutlined, FileTextOutlined, SettingOutlined, TagOutlined, BugOutlined, CheckSquareOutlined, FlagOutlined, ThunderboltOutlined, CodeOutlined } from '@ant-design/icons-vue';
import { resizableColumn } from "@/components/Table/tableDisplay";
import { useTableColumnResize } from "@/components/Table/useTableColumnResize";
import TableDisplaySettings from '@/components/Table/TableDisplaySettings.vue'
import { readDisplay, normalizeDisplay, displayStorageKey, pageSizes, type DisplayColumn, type TableDisplay, type ColumnVisibility } from '@/components/Table/tableDisplay'
import TestCaseDetail from '@/components/TestCase/TestCaseDetail.vue'
import TestCaseFilter from '@/components/TestCase/TestCaseFilter.vue'
import { caseSearchParams, isAdvancedCaseSearch } from '@/components/TestCase/caseSearchScope'
import { useCaseSelection } from '@/components/TestCase/caseSelection'
import { filterFieldCatalog } from '@/components/TestCase/filterFieldCatalog'
import { caseGovernanceApi } from '@/api/caseGovernance'
import ImportCasesModal from '@/components/TestCase/ImportCasesModal.vue'
import CaseGovernancePanel from '@/components/TestCase/CaseGovernancePanel.vue'
import CaseMindMap from '@/components/TestCase/CaseMindMap.vue'
import CaseRecycleBin from '@/components/TestCase/CaseRecycleBin.vue'
import CaseTemplateManager from '@/components/TestCase/CaseTemplateManager.vue'
import CaseExportDialog from '@/components/TestCase/CaseExportDialog.vue'
import { testCaseApi } from '@/api/testCase';
import {saveCaseBlob,caseFeaturesApi} from '@/api/caseFeatures'
import { projectApi } from '@/api/project';
import { useProjectStore } from '@/stores/project';
import { useUserStore } from '@/stores/user';
import type { TestCase, Project } from '@/types';
import dayjs from 'dayjs'
import { useWindowSize } from '@vueuse/core'

const route = useRoute()
const router = useRouter()
const projectStore = useProjectStore()
const userStore = useUserStore()

// 当前项目 ID：优先使用 store，其次使用已有项目列表的第一个
const projects = computed<Project[]>(() => projectStore.projects)
const projectId = computed<string>(() => {
  if (projectStore.currentProject) {
    return projectStore.currentProject.id
  }
  return projects.value[0]?.id || ''
})

// 左侧模块树
const recycleTotal = ref(0)
const { width: windowWidth } = useWindowSize()
const isNarrowScreen = computed(() => windowWidth.value <= 900)
const showModules=ref(window.innerWidth>900)
const moduleSearchValue = ref('')
const moduleTreeData = ref<any[]>([])
const selectedModuleKeys = ref<string[]>(['all'])
const expandedModuleKeys = ref<string[]>([])
const modules = ref<any[]>([])
const flatModuleKeys = ref<string[]>([])
const lastSelectedModuleKey = ref<string | null>(null)
const isShiftKeyPressed = ref(false)

// 模块树右键菜单状态
const moduleContextMenu = reactive<{
  visible: boolean
  x: number
  y: number
  node: any | null
}>({
  visible: false,
  x: 0,
  y: 0,
  node: null
})

// 计算右键菜单节点类型
const contextMenuNodeType = computed(() => {
  const node = moduleContextMenu.node
  if (!node) return 'virtual'

  const key = node.key as string
  if (key === 'all' || key === 'unplanned') {
    return 'virtual'
  }

  // 检查是否是用例节点（key以case_开头）
  if (key.startsWith('case_')) {
    return 'case'
  }

  return 'module'
})

// 表格标题（自定义title信息）
const tableTitle = computed(() => {
  const selectedModule = selectedModuleKeys.value[0]
  if (!selectedModule || selectedModule === 'all') {
    return `全部用例 (${pagination.total})`
  }
  const module = findModuleById(selectedModule)
  if (module) {
    return `${module.name} (${pagination.total})`
  }
  return `用例列表 (${pagination.total})`
})

// 右侧表格
const loading = ref(false)
const testCases = ref<TestCase[]>([])
const selectedRowKeys = ref<string[]>([])
const searchValue = ref(''), appliedSearchValue = ref('')
const viewMode = ref('all')
const viewLayout = ref<'list' | 'mind'>('list')
const mindMap = ref<InstanceType<typeof CaseMindMap>>()
const mindScope = computed(() => JSON.stringify([projectId.value,userStore.user?.id]))
let mindGeneration = 0
watch(mindScope, () => { mindGeneration++; mindSaving.value=false }, {flush:'sync'})
async function changeViewLayout(value:'list'|'mind') { if(value!==viewLayout.value && await mindMap.value?.beforeClose()!==false) viewLayout.value=value }
async function openRecycle() { if(await mindMap.value?.beforeClose()!==false)recycleVisible.value=true }
const exportVisible=ref(false),exportBusy=ref(false),exportFormat=ref('xlsx')
const recycleVisible = ref(route.query.view === 'recycle'), templateVisible = ref(false), mindSaving = ref(false)
const sortBy = ref('updated_at'), sortOrder = ref('desc')
const filterDrawerVisible = ref(false)
const newFilterView = ref(false), filterSaving = ref(false)
onBeforeRouteLeave(async () => !filterSaving.value && !selection.working.value && !exportBusy.value && (await mindMap.value?.beforeClose()??true) && (await detailPanel.value?.beforeClose()??true))
onBeforeRouteUpdate(async () => !filterSaving.value && !selection.working.value && !exportBusy.value && (await mindMap.value?.beforeClose()??true) && (await detailPanel.value?.beforeClose()??true))
function openFilter(isNew: boolean) {
  if (filterSaving.value) return
  newFilterView.value = isNew
  filterDrawerVisible.value = true
}
watch(recycleVisible, async value => {
  const query = { ...route.query }
  if (value) query.view = 'recycle'; else delete query.view
  try { await router.replace({ path: route.path, query }) }
  catch (error) { console.error('同步回收站页面地址失败', error) }
})

// 高级筛选条件
const advancedFilters = ref<Array<{
  field: string
  operator: string
  value: any
}>>([])
const filterLogic = ref<'and' | 'or'>('and')

// 筛选字段定义（从数据库获取）
const filterFields = ref<any[]>([])
const filterFieldError = ref(''),
  filterFieldLoading = ref(false)

// 加载筛选字段配置
let filterLoadSequence = 0
let filterMetadataCache: {
  project: string
  fields?: any[]
  templates: any[]
  members: { id: string; name: string }[]
} = { project: '', templates: [], members: [] }
const loadFilterFields = async () => {
  const project = projectId.value
  if (!project) return
  const sequence = ++filterLoadSequence
  filterFieldLoading.value = true
  try {
    const results = await Promise.allSettled([
      testCaseApi.getFilterFields(project),
      caseFeaturesApi.templates(project),
      caseGovernanceApi.reviewers(project),
    ])
    if (sequence !== filterLoadSequence || project !== projectId.value) return
    const labels = ['筛选字段', '自定义字段', '项目成员']
    const failed: string[] = []
    results.forEach((result, index) => {
      if (result.status === 'rejected') {
        failed.push(labels[index])
        console.error(`加载${labels[index]}失败`, result.reason)
      }
    })
    if (filterMetadataCache.project !== project)
      filterMetadataCache = { project, templates: [], members: [] }
    if (results[0].status === 'fulfilled')
      filterMetadataCache.fields = results[0].value
    if (results[1].status === 'fulfilled')
      filterMetadataCache.templates = results[1].value
    if (results[2].status === 'fulfilled')
      filterMetadataCache.members = results[2].value
    const fields =
      filterMetadataCache.fields ||
      getDefaultFilterFields().map((f) => ({
        fieldKey: f.key,
        fieldLabel: f.label,
        fieldType: f.type,
        operators: 'operators' in f ? f.operators : undefined,
        options: 'options' in f ? f.options : undefined,
      }))
    filterFields.value = filterFieldCatalog(
      fields,
      filterMetadataCache.templates,
      filterMetadataCache.members,
    )
    filterFieldError.value = failed.length
      ? `${failed.join('、')}加载失败，请重试；已加载字段及筛选草稿保留`
      : ''
  } catch (error) {
    console.error('整理筛选字段失败，保留错误和重试入口', error)
    if (sequence === filterLoadSequence && project === projectId.value)
      filterFieldError.value = '筛选字段加载失败，请重试'
  } finally {
    if (sequence === filterLoadSequence) filterFieldLoading.value = false
  }
}

// 默认筛选字段（作为后备）
const getDefaultFilterFields = () => [
  {
    key: 'id',
    label: 'ID',
    type: 'text' as const,
    operators: ['contains', 'equals', 'not_equals']
  },
  {
    key: 'name',
    label: '用例名称',
    type: 'text' as const
  },
  {
    key: 'moduleId',
    label: '所属模块',
    type: 'module' as const
  },
  {
    key: 'priority',
    label: '用例等级',
    type: 'select' as const,
    options: [
      { label: 'P0', value: 'P0' },
      { label: 'P1', value: 'P1' },
      { label: 'P2', value: 'P2' },
      { label: 'P3', value: 'P3' }
    ]
  },
  {
    key: 'type',
    label: '用例类型',
    type: 'select' as const,
    options: [
      { label: '功能测试', value: 'functional' },
      { label: '接口测试', value: 'interface' },
      { label: 'UI测试', value: 'ui' },
      { label: '性能测试', value: 'performance' },
      { label: '安全测试', value: 'security' }
    ]
  },
  {
    key: 'status',
    label: '执行结果',
    type: 'select' as const,
    options: [
      { label: '未执行', value: 'not_executed' },
      { label: '通过', value: 'passed' },
      { label: '失败', value: 'failed' },
      { label: '阻塞', value: 'blocked' },
      { label: '跳过', value: 'skipped' }
    ]
  },
  {
    key: 'isAutomated',
    label: '是否自动化',
    type: 'select' as const,
    options: [
      { label: '是', value: true },
      { label: '否', value: false }
    ]
  },
  {
    key: 'tags',
    label: '标签',
    type: 'tags' as const
  },
  {
    key: 'requirementRef',
    label: '需求关联',
    type: 'text' as const
  },
  {
    key: 'precondition',
    label: '前置条件',
    type: 'text' as const
  },
  { key:'attachment',label:'关联附件',type:'text' as const },
  { key:'createdBy',label:'创建人',type:'member' as const },
  { key:'updatedBy',label:'更新人',type:'member' as const },
  { key:'createdAt',label:'创建时间',type:'date' as const },
  { key:'updatedAt',label:'更新时间',type:'date' as const }

]

// 旧的筛选条件（保留兼容性）
const filters = reactive({
  level: undefined as string | undefined,
  reviewResult: undefined as string | undefined,
  executionResult: undefined as string | undefined,
  isAutomated: undefined as boolean | undefined
})

const governancePanel = ref<InstanceType<typeof CaseGovernancePanel>>()
const savedViewFilters = computed(() => ({ filterConditions: advancedFilters.value, filterLogic: filterLogic.value }))
const searchScope = computed(() => ({
  personalView: !!governancePanel.value?.activeView,
  systemView: viewMode.value,
  conditions: advancedFilters.value,
  logic: filterLogic.value,
  search: appliedSearchValue.value,
  moduleKeys: selectedModuleKeys.value,
  moduleIds: selectedModuleKeys.value.filter(key=>!key.startsWith('case_')).flatMap(key=>tableDisplay.value.includeDescendants ? getModuleAndChildrenIds(key) : [key]),
  priority: filters.level, status: filters.executionResult, reviewStatus: filters.reviewResult, automated: filters.isAutomated
}))
const isAdvancedSearchMode = computed(() => isAdvancedCaseSearch(searchScope.value))
const currentCaseParams = computed(() => caseSearchParams(searchScope.value))
// 范围改变时清掉旧勾选；翻页和排序仍可保留当前范围内的跨页选择。
function resetBasicSearch() {
  searchValue.value=''; appliedSearchValue.value=''; filters.level=undefined; filters.executionResult=undefined; filters.reviewResult=undefined; filters.isAutomated=undefined
}
function resetSearchSelection() {
  resetBasicSearch(); selectedModuleKeys.value=['all']; selection.clear(); pagination.current=1
}
async function saveFilterView(name: string, conditions: any[], logic: 'and' | 'or', mode: 'create' | 'update' | 'copy') {
  if (!governancePanel.value) throw new Error('项目视图尚未加载')
  await governancePanel.value.persistFilterView(name, { filterConditions: conditions, filterLogic: logic }, mode)
}
const refreshGovernedCases = async () => { const casesLoaded=await loadTestCases(); await loadModuleTree(); return casesLoaded }
const clearAdvancedFilters = async () => {
  governancePanel.value?.resetViewSelection(); viewMode.value='all'; advancedFilters.value=[]; filterLogic.value='and'; newFilterView.value=false
  resetSearchSelection(); await loadTestCases()
}
const applySystemView = async (value: string) => {
  viewMode.value=value; advancedFilters.value=[]; filterLogic.value='and'; newFilterView.value=false
  resetSearchSelection(); await loadTestCases()
}
const applySavedView = async (saved: Record<string, any>) => {
  // 个人视图使用抽屉可见的条件；旧快照中的基础筛选不再暗中约束高级范围。
  viewMode.value='all'; newFilterView.value=false
  advancedFilters.value = Array.isArray(saved.filterConditions) ? saved.filterConditions : []
  filterLogic.value = saved.filterLogic === 'or' ? 'or' : 'and'
  resetSearchSelection(); await loadTestCases()
}

// 分页
const pagination = reactive({
  current: 1,
  pageSize: 20,
  total: 0,
  showSizeChanger: true,
  showQuickJumper: true,
  showTotal: (total: number) => `共 ${total} 条`
})

// 所有可用的表格列定义
const baseColumns = [
  {
    title: 'ID',
    dataIndex: 'id',
    key: 'id',
    width: 150,
    sorter: true,
    ellipsis: true,
    defaultVisible: true
  },
  {
    title: '用例名称',
    dataIndex: 'name',
    key: 'name',
    width: 180,
    sorter: true,
    ellipsis: true,
    defaultVisible: true
  },
  {
    title: '用例等级',
    dataIndex: 'priority',
    key: 'level',
    width: 150,
    filters: [
      { text: 'P0', value: 'P0' },
      { text: 'P1', value: 'P1' },
      { text: 'P2', value: 'P2' },
      { text: 'P3', value: 'P3' }
    ],
    defaultVisible: true
  },
  {
    title: '评审结果',
    dataIndex: 'reviewResult',
    key: 'reviewResult',
    width: 150,
    filters: [
      { text: '未评审', value: 'not_reviewed' },
      { text: '待评审', value: 'pending' },
      { text: '已通过', value: 'passed' },
      { text: '不通过', value: 'rejected' },
      { text: '重新提审', value: 'resubmit' }
    ],
    defaultVisible: true
  },
  {
    title: '执行结果',
    dataIndex: 'status',
    key: 'executionResult',
    width: 150,
    filters: [
      { text: '未执行', value: 'not_executed' },
      { text: '成功', value: 'passed' },
      { text: '失败', value: 'failed' },
      { text: '阻塞', value: 'blocked' },
      { text: '跳过', value: 'skipped' }
    ],
    defaultVisible: true
  },
  {
    title: '所属模块',
    dataIndex: 'modulePath',
    key: 'modulePath',
    width: 200,
    ellipsis: true,
    defaultVisible: true
  },
  {
    title: '标签',
    dataIndex: 'tags',
    key: 'tags',
    width: 300,
    ellipsis: true,
    defaultVisible: true
  },
  {
    title: '是否自动化',
    dataIndex: 'isAutomated',
    key: 'isAutomated',
    width: 100,
    align: 'center' as const,
    filters: [
      { text: '是', value: true },
      { text: '否', value: false }
    ],
    defaultVisible: false
  },
  {
    title: '创建人',
    dataIndex: 'createdByName',
    key: 'createdBy',
    width: 200,
    ellipsis: true,
    defaultVisible: true
  },
  {
    title: '创建时间',
    dataIndex: 'createdAt',
    key: 'createdAt',
    width: 200,
    sorter: true,
    defaultVisible: true
  },
  {
    title: '更新人',
    dataIndex: 'updatedByName',
    key: 'updatedBy',
    width: 200,
    ellipsis: true,
    defaultVisible: true
  },
  {
    title: '更新时间',
    dataIndex: 'updatedAt',
    key: 'updatedAt',
    width: 200,
    sorter: true,
    defaultVisible: true
  }
]

const defaultColumnOrder = ['id','name','level','reviewResult','executionResult','modulePath','tags','updatedBy','updatedAt','createdBy','createdAt','isAutomated']
const allColumns = defaultColumnOrder.map(key=>baseColumns.find(column=>column.key===key)!)

// 操作列（始终显示）
const actionColumn = {
  title: '操作',
  key: 'actions',
  width: 140,
  fixed: 'right' as const
}

// 显示偏好与当前用户、项目隔离，复用本地存储保存列宽。
const displayDefinitions: DisplayColumn[] = allColumns.map(column=>({key:column.key,title:column.title,required:['id','name'].includes(column.key),defaultVisible:column.defaultVisible}))
const tableStorageKey = computed(()=>displayStorageKey(userStore.user?.id || '',projectId.value,'test-cases'))
const tableDisplay = ref<TableDisplay>(readDisplay(localStorage,tableStorageKey.value,displayDefinitions))
pagination.pageSize = tableDisplay.value.pageSize
const columnSettingVisible = ref(false), tableSettingsError = ref('')
const columns = computed(()=>{
  const definitions = new Map(allColumns.map(column=>[column.key,column]))
  const shown = tableDisplay.value.columns.filter(column=>column.visible).map(column=>{
    const definition=definitions.get(column.key)!
    const values:Record<string,unknown>={level:filters.level,reviewResult:filters.reviewResult,executionResult:filters.executionResult,isAutomated:filters.isAutomated}
    return {...resizableColumn(definition,column), filters:isAdvancedSearchMode.value ? undefined : definition.filters, filteredValue:isAdvancedSearchMode.value || values[column.key]===undefined ? null : [values[column.key]]}
  })
  return [...shown,{...actionColumn,fixed:isNarrowScreen.value ? undefined : actionColumn.fixed}]
})
const tableWidth = computed(()=>columns.value.reduce((width,column)=>width+column.width,50))
function persistTableDisplay(next:TableDisplay):boolean {
  try {
    const normalized=normalizeDisplay(next,displayDefinitions)
    localStorage.setItem(tableStorageKey.value,JSON.stringify(normalized))
    tableDisplay.value=normalized
    tableSettingsError.value=''
    console.info('测试用例表格显示配置已保存',{projectId:projectId.value,pageSize:normalized.pageSize,includeDescendants:normalized.includeDescendants})
    return true
  } catch(error) {
    console.error('保存测试用例表格配置失败',error)
    tableSettingsError.value='保存失败，请检查浏览器存储后重试'
    message.error(tableSettingsError.value)
    return false
  }
}
const resizeColumn = useTableColumnResize(tableDisplay,tableStorageKey,persistTableDisplay)
function saveTableColumns(columns:ColumnVisibility[]) {
  if(persistTableDisplay({...tableDisplay.value,columns}))columnSettingVisible.value=false
}
function setTablePageSize(pageSize:number) {
  if(!pageSizes.includes(pageSize) || !persistTableDisplay({...tableDisplay.value,pageSize}))return
  pagination.pageSize=pageSize
  pagination.current=1
  void loadTestCases()
}
function setSubdirectory(includeDescendants:boolean) {
  if(!persistTableDisplay({...tableDisplay.value,includeDescendants}))return
  pagination.current=1
  void loadTestCases()
}
watch(tableStorageKey,()=>{
  columnSettingVisible.value=false
  tableSettingsError.value=''
  tableDisplay.value=readDisplay(localStorage,tableStorageKey.value,displayDefinitions)
  pagination.pageSize=tableDisplay.value.pageSize
  pagination.current=1
  testCases.value=[]
  void loadTestCases()
})

// 生成用例显示ID
const getCaseDisplayId = (record: TestCase, index: number) => {
  // 优先使用 caseCode
  if (record.caseCode) {
    return record.caseCode
  }
  // 否则生成序号格式（001, 002, ...）
  const pageOffset = (pagination.current - 1) * pagination.pageSize
  const num = pageOffset + index + 1
  return num.toString().padStart(3, '0')
}

// 行选择复用范围状态，表头默认复选框只改变当前页。
const selection = useCaseSelection(projectId, currentCaseParams, selectedRowKeys, computed(() => testCases.value.map(c => c.id)))
const rowSelection = computed(() => ({
  selectedRowKeys: selection.pageSelected.value,
  preserveSelectedRowKeys: !selection.selectAll.value,
  columnWidth: 50,
  getCheckboxProps: () => ({ disabled: selection.working.value || exportBusy.value || loading.value }),
  onChange: selection.keysChanged,
  selections: [
    { key: 'current', text: '全选当前页', onSelect: selection.current },
    selection.selectAll.value
      ? { key: 'cancelAll', text: '取消全选所有页', onSelect: () => { if (!selection.working.value) selection.clear() } }
      : { key: 'all', text: '全选所有页', onSelect: () => { if (pagination.total && !loading.value) selection.all() } },
  ],
}))

// 详情用例
const detailPanel=ref<InstanceType<typeof TestCaseDetail>>();
async function closeDetail(){if(await detailPanel.value?.beforeClose()??true)detailCaseVisible.value=false}
async function navigateDetailTo(id:string){if(await detailPanel.value?.beforeClose()??true)viewingCaseId.value=id}
const detailCaseVisible = ref(false)
const viewingCaseId = ref<string>('')

// 编辑用例

// 导入对话框
const importModalVisible = ref(false)

// 存储所有用例（用于构建模块树中的用例节点）
const allCasesForTree = ref<any[]>([])

// 加载模块树
let moduleListSequence=0
const loadModuleTree = async () => {
  const currentProject=projectId.value, scope=mindScope.value, request=++moduleListSequence
  const current=()=>request===moduleListSequence && scope===mindScope.value
  if (!currentProject) return
  try {
    // 先获取所有用例（用于在模块树中显示用例节点）
    const allCasesResponse = await testCaseApi.getTestCases(currentProject, {
      page: 1,
      size: 9999  // 获取所有用例
    })
    if(!current())return
    const response = await projectApi.getModules(currentProject)
    if(!current())return
    allCasesForTree.value = allCasesResponse.items || []
    // 新的响应格式包含 modules 和 totalCaseCount
    const moduleList = response.modules || response
    const totalCaseCount = response.totalCaseCount ?? allCasesForTree.value.length

    modules.value = moduleList
    const treeData = buildModuleTree(moduleList, allCasesForTree.value)

    // 添加"全部用例"节点，使用后端返回的总数
    moduleTreeData.value = [
      {
        title: '全部用例',
        key: 'all',
        count: totalCaseCount,
        isLeaf: true
      },
      {title:'未规划用例',key:'unplanned',nodeType:'virtual',count:allCasesForTree.value.filter(c=>!c.moduleId).length,isLeaf:true},
      ...treeData
    ]
    rebuildFlatModuleKeys()
    const recycled=await caseFeaturesApi.recycle(currentProject, { page: 1, size: 1 })
    if(current())recycleTotal.value = recycled.total
  } catch (error) {
    console.error('加载模块树与回收站计数失败', error)
  }
}

const moduleSelectTree = computed(() => [{title:'未规划用例',key:'__unassigned__'}, ...buildModuleTree(modules.value,[])])

const buildModuleTree = (modules: any[], allCases: any[]): any[] => {
  const treeMap = new Map()
  const treeData: any[] = []

  // 第一步：构建模块节点，使用后端返回的 caseCount
  modules.forEach(module => {
    treeMap.set(module.id, {
      title: module.name,
      key: module.id,
      directCount: module.caseCount || 0,  // 从后端获取的直接用例数
      count: 0,  // 总用例数（包含子模块），稍后计算
      isLeaf: false,
      nodeType: 'module',
      children: [],
      raw: module
    })
  })

  // 第二步：建立模块父子关系
  modules.forEach(module => {
    const node = treeMap.get(module.id)
    if (module.parentId && treeMap.has(module.parentId)) {
      treeMap.get(module.parentId).children.push(node)
    } else {
      treeData.push(node)
    }
  })

  // 第三步：将用例添加到对应模块下（用于树中显示用例节点）
  // 使用传入的 allCases 参数，而不是 testCases.value
  modules.forEach(module => {
    const moduleCases = allCases.filter(c => c.moduleId === module.id)
    const moduleNode = treeMap.get(module.id)

    moduleCases.forEach(tc => {
      moduleNode.children.push({
        title: tc.name,
        key: `case_${tc.id}`,
        isLeaf: true,
        nodeType: 'case',
        caseId: tc.id,
        caseCode: tc.caseCode,
        priority: tc.priority,
        raw: tc
      })
    })
  })

  // 第四步：递归计算每个模块的总用例数（包含所有子模块）
  const calculateTotalCount = (node: any): number => {
    let total = node.directCount || 0
    if (node.children) {
      node.children.forEach((child: any) => {
        if (child.nodeType === 'module') {
          total += calculateTotalCount(child)
        }
      })
    }
    node.count = total
    return total
  }

  treeData.forEach(node => calculateTotalCount(node))

  return treeData
}

const rebuildFlatModuleKeys = () => {
  const result: string[] = []
  const traverse = (nodes: any[]) => {
    nodes.forEach(node => {
      // 包含模块和用例节点，但排除虚拟节点
      if (node.key !== 'all' && node.key !== 'unplanned') {
        result.push(node.key)
      }
      if (node.children && node.children.length > 0) {
        traverse(node.children)
      }
    })
  }
  traverse(moduleTreeData.value)
  flatModuleKeys.value = result
}

// 获取模块及其所有子模块的 ID 列表
function getModuleAndChildrenIds(moduleId: string): string[] {
  const result: string[] = [moduleId]

  const findNode = (nodes: any[], targetId: string): any => {
    for (const node of nodes) {
      if (node.key === targetId) return node
      if (node.children && node.children.length > 0) {
        const found = findNode(node.children, targetId)
        if (found) return found
      }
    }
    return null
}

  const collectChildModuleIds = (node: any) => {
    if (!node.children) return
    node.children.forEach((child: any) => {
      if (child.nodeType === 'module') {
        result.push(child.key)
        collectChildModuleIds(child)
      }
    })
  }

  const targetNode = findNode(moduleTreeData.value, moduleId)
  if (targetNode) {
    collectChildModuleIds(targetNode)
  }

  return result
}

// 加载测试用例列表，旧项目响应不能覆盖当前项目。
let caseListSequence = 0
const loadTestCases = async () => {
  const currentProject=projectId.value, scope=mindScope.value, request=++caseListSequence
  if (!currentProject) return

    loading.value = true
  try {
    const params = { ...currentCaseParams.value, page:pagination.current, size:pagination.pageSize, sortBy:sortBy.value, sortOrder:sortOrder.value }

    console.log('调用 getTestCases API，参数:', params)
    const response = await testCaseApi.getTestCases(currentProject, params)
    if(request!==caseListSequence || scope!==mindScope.value)return
    console.log('API 返回结果:', { total: response.total, itemsCount: response.items?.length })
    testCases.value = response.items || []
    pagination.total = response.total || 0
    return true
  } catch (error) {
    console.error('加载测试用例失败', error)
    if(request===caseListSequence && scope===mindScope.value) message.error('加载测试用例失败')
  } finally {
    if(request===caseListSequence) loading.value = false
  }
}

// 处理模块/用例选择（支持 Shift + 左键 批量选择）
const handleModuleSelect = (_keys: string[], info: any) => {
  recycleVisible.value = false
  moduleContextMenu.visible = false
  const currentKey = info?.node?.key as string | undefined
  const currentNodeType = info?.node?.nodeType as string | undefined

  // 排除虚拟节点（'all'）不参与范围选择
  const isVirtualNode = currentKey === 'all'
  const lastKeyIsVirtual = lastSelectedModuleKey.value === 'all'

  // 如果按住了 Shift 键，且之前有选中的节点，且都不是虚拟节点，则进行范围选择
  if (isShiftKeyPressed.value && lastSelectedModuleKey.value && currentKey && !isVirtualNode && !lastKeyIsVirtual) {
    const flat = flatModuleKeys.value
    const startIndex = flat.indexOf(lastSelectedModuleKey.value)
    const endIndex = flat.indexOf(currentKey)
    if (startIndex !== -1 && endIndex !== -1) {
      const [start, end] =
        startIndex < endIndex ? [startIndex, endIndex] : [endIndex, startIndex]
      const rangeKeys = flat.slice(start, end + 1)
      // 合并到已选中的节点中
      selectedModuleKeys.value = Array.from(
        new Set([...selectedModuleKeys.value, ...rangeKeys])
      )
      // 更新最后选中的节点为当前节点
      lastSelectedModuleKey.value = currentKey
    } else {
      // 如果找不到范围，则只选中当前节点
      selectedModuleKeys.value = currentKey ? [currentKey] : []
      if (currentKey && !isVirtualNode) {
        lastSelectedModuleKey.value = currentKey
      }
    }
  } else {
    // 没有按 Shift，单选模式：只选中当前节点
    selectedModuleKeys.value = currentKey ? [currentKey] : []
    if (currentKey && !isVirtualNode) {
      lastSelectedModuleKey.value = currentKey
    }
  }

  // 只有选择模块或"全部用例"时才加载用例列表
  // 如果选择的是用例节点，不重新加载列表
  if (currentNodeType !== 'case') {
    pagination.current = 1
    loadTestCases()
  }
}

const handleModuleExpand = (keys: string[]) => {
  expandedModuleKeys.value = keys
}

const handleModuleSearch = () => {
  const needle=moduleSearchValue.value.trim().toLowerCase()
  if(!needle){expandedModuleKeys.value=[];return}
  const match=modules.value.filter(m=>m.name.toLowerCase().includes(needle))
  const ancestors=new Set<string>()
  for(const module of match){let current=module;while(current&&!ancestors.has(current.id)){ancestors.add(current.id);current=modules.value.find(m=>m.id===current.parentId)}}
  expandedModuleKeys.value=[...ancestors]
  if(match[0]){selectedModuleKeys.value=[match[0].id];pagination.current=1;loadTestCases()}else message.info('没有匹配模块')
}

// 处理搜索
const handleSearch = () => {
  appliedSearchValue.value = searchValue.value
  pagination.current = 1
  loadTestCases()
}

// 应用高级筛选
const handleFilterApply = (conditions: any[], logic: string) => {
  if (newFilterView.value) viewMode.value='all'
  newFilterView.value=false
  advancedFilters.value = conditions
  filterLogic.value = logic as 'and' | 'or'
  resetSearchSelection()
  console.info('应用用例高级检索',{projectId:projectId.value,mode:viewMode.value,conditions:conditions.length,logic})
  loadTestCases()
}

// 处理筛选（兼容旧代码）




// 处理表格变化
const handleTableChange = (_pag: any, _filters: any, sorter: any) => {
  const keys: Record<string,string> = {id:'case_code',name:'name',createdAt:'created_at',updatedAt:'updated_at'}
  sortBy.value = keys[sorter?.columnKey] || 'updated_at'
  sortOrder.value = sorter?.order === 'ascend' ? 'asc' : 'desc'
  pagination.current = 1
  if (!isAdvancedSearchMode.value) {
    filters.level = _filters?.level?.[0]
    filters.reviewResult = _filters?.reviewResult?.[0]
    filters.executionResult = _filters?.executionResult?.[0]
    filters.isAutomated = _filters?.isAutomated?.[0]
  }
  loadTestCases()
}

// 处理分页变化
const handlePaginationChange = (page: number, pageSize: number) => {
  if(pageSize!==tableDisplay.value.pageSize && !persistTableDisplay({...tableDisplay.value,pageSize})){pagination.pageSize=tableDisplay.value.pageSize;return}
  pagination.current = page
  pagination.pageSize = pageSize
  loadTestCases()
}

// 创建用例
const handleCreateCase = () => { void router.push({path:'/test-cases/create',query:{projectId:projectId.value,moduleId:!['all','unplanned'].includes(selectedModuleKeys.value[0]) ? selectedModuleKeys.value[0] : undefined}}) }

const saveInline=async(record:TestCase,field:string,value:unknown)=>{if(field==='name'&&!String(value).trim())return message.warning('用例名称不能为空');try{await testCaseApi.updateTestCase(projectId.value,record.id,{[field]:value});await refreshGovernedCases();message.success('用例已保存')}catch(error){console.error('行内编辑失败',error)}}
const saveMindNode = async (id: string, patch: Partial<TestCase>) => {
  let saved:TestCase|undefined
  const ok=await mindOperation(async p=>{saved=await testCaseApi.updateTestCase(p,id,patch)},'脑图节点已保存',loaded=>{if(loaded)saved=testCases.value.find(c=>c.id===id)||saved})
  return ok ? saved || true : false
}
const mindOperation = async (action:(project:string)=>Promise<unknown>,success:string,afterRefresh?:(loaded:boolean)=>void):Promise<boolean> => {
  if(mindSaving.value || !projectId.value)return false
  const p=projectId.value, scope=mindScope.value, generation=mindGeneration
  const current=()=>generation===mindGeneration && scope===mindScope.value
  mindSaving.value=true
  try {
    await action(p)
    if(!current())return false
    message.success(success)
    try { const loaded=await refreshGovernedCases(); if(current()){afterRefresh?.(Boolean(loaded));if(!loaded)message.warning('已保存，请刷新列表查看最新内容')} } catch { if(current())message.warning('已保存，请刷新列表查看最新内容') }
    return current()
  } catch(error){if(current())message.error('操作未确认，编辑内容已保留；请刷新核验结果后再重试');return false}
  finally { if(current())mindSaving.value=false }
}
const createMindCase = async (moduleId?: string, draft?: Partial<TestCase>) => {
  if (!draft) { await router.push({path:'/test-cases/create',query:{projectId:projectId.value,moduleId}});return true }
  return mindOperation(p=>testCaseApi.createTestCase(p,draft),'已粘贴为新用例')
}
const renameMindModule = async (id:string,name:string) => {
  if(!name.trim())return false
  return mindOperation(p=>projectApi.updateModule(p,id,{name:name.trim(),sortOrder:modules.value.find(m=>m.id===id)?.sortOrder || 0}),'模块名称已保存')
}
const createMindModule = (parentId:string|null,name:string) => mindOperation(p=>projectApi.createModule(p,{name,parentId,sortOrder:0}),'模块已创建')
const moveMindNode = (kind:'case'|'module',id:string,parentId:string|null) => {
  const module=modules.value.find(m=>m.id===id)
  if(kind==='module'&&!module)return Promise.resolve(false)
  return mindOperation(p=>kind==='case' ? caseGovernanceApi.batch(p,{caseIds:[id],moduleId:parentId}) : projectApi.updateModule(p,id,{name:module.name,parentId,sortOrder:module.sortOrder||0}),'节点已移动')
}
const deleteMindNode = (kind:'case'|'module',id:string) => mindOperation(p=>kind==='case' ? testCaseApi.deleteTestCase(p,id) : projectApi.deleteModule(p,id),'节点已删除')

// 编辑用例
const handleEditCase = (record: TestCase) => { void router.push({path:`/test-cases/${record.id}/edit`,query:{projectId:projectId.value}}) }

// 查看用例（打开详情页面）
const handleViewCase = async (record: TestCase) => {
  if(detailPanel.value&&!(await detailPanel.value.beforeClose()))return;
  viewingCaseId.value = record.id
  detailCaseVisible.value = true
}

// 从详情页面跳转到编辑页面
const detailFullscreen = ref(false)
const detailIndex = computed(()=>testCases.value.findIndex(c=>c.id===viewingCaseId.value))
const canPreviousCase = computed(()=>detailIndex.value>0 || pagination.current>1)
const canNextCase = computed(()=>detailIndex.value>=0 && (detailIndex.value<testCases.value.length-1 || pagination.current*pagination.pageSize<pagination.total))
const navigateDetail = async (direction: number) => {
  if(detailPanel.value&&!(await detailPanel.value.beforeClose()))return;
  const next=detailIndex.value+direction
  if (next>=0 && next<testCases.value.length) { viewingCaseId.value=testCases.value[next].id; return }
  if (direction<0 && pagination.current>1 || direction>0 && pagination.current*pagination.pageSize<pagination.total) {
    pagination.current+=direction;await loadTestCases()
    const row=direction>0 ? testCases.value[0] : testCases.value.at(-1)
    if(row)viewingCaseId.value=row.id
  }
}
const copyFromDetail = async () => { if(detailPanel.value&&!(await detailPanel.value.beforeClose()))return;try { const row=testCases.value.find(c=>c.id===viewingCaseId.value) || await testCaseApi.getTestCase(projectId.value,viewingCaseId.value);detailCaseVisible.value=false;await handleCopyCase(row) } catch(error) { console.error('复制详情用例失败',error) } }
const deleteFromDetail = async () => { if(detailPanel.value&&!(await detailPanel.value.beforeClose()))return;try { const row=await testCaseApi.getTestCase(projectId.value,viewingCaseId.value); await handleDeleteCase(row) } catch(error) { console.error('加载待删除用例失败',error) } }
const handleEditFromDetail = async () => {
  if(detailPanel.value&&!(await detailPanel.value.beforeClose()))return;
  detailCaseVisible.value = false
  void router.push({path:`/test-cases/${viewingCaseId.value}/edit`,query:{projectId:projectId.value}})
}

// 删除用例
const handleDeleteCase = async (record: TestCase) => {
  Modal.confirm({
    title: '确认删除',
    content: `确定要删除用例"${record.name}"吗？`,
    onOk: async () => {
      if(viewingCaseId.value===record.id&&detailPanel.value&&!(await detailPanel.value.beforeClose()))return;
      try {
        await testCaseApi.deleteTestCase(projectId.value, record.id)
        message.success('删除成功')
        if(viewingCaseId.value===record.id)detailCaseVisible.value=false
        await loadTestCases()
        await loadModuleTree()
  } catch (error) {
    console.error('删除用例失败',error)
    message.error('删除失败')
      }
    }
  })
}

// 复制用例
const handleCopyCase = async (record: TestCase) => { await router.push({path:'/test-cases/create',query:{projectId:projectId.value,copyFrom:record.id}}) }

// 执行用例
const executionCase = ref<TestCase | null>(null)
const executionTemplates = ref<TestSuite[]>([])
const caseExecutionVisible = ref(false)
const caseExecutionLoading = ref(false)
const selectedExecutionTemplate = ref<string>()
const handleExecuteCase = async (record: TestCase) => {
  if (!record.isAutomated) { message.warning('仅自动化用例支持Agent执行'); return }
  executionCase.value = record; selectedExecutionTemplate.value = undefined; executionTemplates.value = []
  caseExecutionVisible.value = true; caseExecutionLoading.value = true
  try {
    const plans = (await testPlanApi.getTestPlans(projectId.value, { size: 1000 })).items
    const groups = await Promise.all(plans.map(plan => testSuiteApi.getTestSuites(plan.id)))
    executionTemplates.value = groups.flatMap(group => group.items).filter(suite => suite.caseIds.includes(record.id) && /^(xat|ats-sat)(?:\s|$)/.test(suite.executionCommand.trim()))
    selectedExecutionTemplate.value = executionTemplates.value[0]?.id
  } catch (error) { console.error('加载执行模板失败',error);message.error('无法加载执行模板') } finally { caseExecutionLoading.value = false }
}
const confirmCaseExecution = async () => {
  if (!executionCase.value || !selectedExecutionTemplate.value) { message.warning('请选包含该用例的 XAT模板'); return }
  caseExecutionLoading.value = true
  try {
    await testCaseApi.executeCase(executionCase.value.id, selectedExecutionTemplate.value)
    message.success('单用例任务已提交；实际结果可在测试任务/执行记录查看'); caseExecutionVisible.value = false
  } catch (error: any) { console.error('执行用例失败',error);message.error(error.response?.data?.detail || '执行失败') }
  finally { caseExecutionLoading.value = false }
}

// 导入
const handleImport = () => {
  importModalVisible.value = true
}

const handleImportSuccess = async (result: any) => {
  if(result) message.success(`导入完成：新增 ${result.created} 条，更新 ${result.updated} 条`)
  await loadTestCases()
  await loadModuleTree()
}

// 批量操作
const handleExport = ({key}:{key:string})=>{exportFormat.value=key==='xmind'?'xmind':'xlsx';exportVisible.value=true}
const confirmExport=async(options:{format:string;layout:string;fields:string})=>{
  const project=projectId.value, body=selection.request.value;
  if(!project || exportBusy.value || (body && (!selection.ready.value || !selection.permissions.value.export)))return;
  exportBusy.value=true;selection.working.value=true;
  const hide=message.loading('正在导出…',0);
  try{
    const params={...currentCaseParams.value,...options,sortBy:sortBy.value,sortOrder:sortOrder.value};
    const blob=body
      ? await caseGovernanceApi.exportSelection(project,body,{...options,sortBy:sortBy.value,sortOrder:sortOrder.value})
      : await testCaseApi.exportCases(project,params);
    saveCaseBlob(blob,`测试用例_${new Date().toISOString().slice(0,10)}.${options.format}`);
    if (body && project === projectId.value) selection.clear();
    message.success('导出文件已生成');exportVisible.value=false;
  }catch(error){console.error('导出用例失败，保留选择范围',error)}
  finally{hide();exportBusy.value=false;selection.working.value=false}
}
const finishSelectionChange=async()=>{selection.clear();await refreshGovernedCases()}

const handleBatchEdit = () => {
  governancePanel.value?.openBatch()
}

const handleBatchMove = () => {
  governancePanel.value?.openOrganize('move')
}

const handleBatchCopy = () => {
  governancePanel.value?.openOrganize('copy')
}

const handleBatchDelete = () => {
  if (!selection.ready.value || !selection.permissions.value.delete || !selection.request.value) return
  const body=JSON.parse(JSON.stringify(selection.request.value)), project=projectId.value
  const confirmation = Modal.confirm({
    title: '批量删除', content: `确定将选中的 ${selection.count.value} 条用例移入回收站吗？`,
    onOk: async () => {
      selection.working.value=true
      confirmation.update({ cancelButtonProps: { disabled:true }, keyboard:false, maskClosable:false })
      try {
        const result=await caseGovernanceApi.deleteSelection(project,body)
        if(project!==projectId.value)return
        selection.clear();message.success(`已将 ${result.deleted} 条用例移入回收站`)
        await loadTestCases();await loadModuleTree()
      } catch (error) {console.error('批量删除失败，保留选择范围',error);throw error}
      finally {
        selection.working.value=false
        confirmation.update({ cancelButtonProps: { disabled:false }, keyboard:true })
      }
    },
  })
}

const clearSelection = () => { if(!selection.working.value)selection.clear() }

// 模块树右键菜单与拖拽
const hideModuleContextMenu = () => {
  moduleContextMenu.visible = false
}

const handleModuleRightClick = (info: any) => {
  const { event, node } = info
  event.preventDefault()

  // 使用 clientX/clientY 配合 fixed 定位，确保菜单显示在鼠标右侧
  const menuWidth = 150  // 菜单预估宽度
  const menuHeight = 200 // 菜单预估高度

  // 检查是否会超出屏幕边界
  let x = event.clientX
  let y = event.clientY

  // 如果菜单会超出右边界，则显示在鼠标左侧
  if (x + menuWidth > window.innerWidth) {
    x = x - menuWidth
  }

  // 如果菜单会超出下边界，则向上调整
  if (y + menuHeight > window.innerHeight) {
    y = window.innerHeight - menuHeight - 10
  }

  moduleContextMenu.visible = true
  moduleContextMenu.x = x
  moduleContextMenu.y = y
  moduleContextMenu.node = node

  const key = node.key as string
  if (!selectedModuleKeys.value.includes(key)) {
    selectedModuleKeys.value = [key]
    lastSelectedModuleKey.value = key
  }
}

const allowModuleDrop = (options: any) => {
  const dropKey = options.dropNode?.key
  return dropKey !== 'all' && dropKey !== 'unplanned'
}

const findModuleById = (id: string) => {
  return modules.value.find(m => m.id === id)
}

const getNextSortOrder = (parentId?: string) => {
  const siblings = modules.value.filter(m => m.parentId === parentId)
  if (!siblings.length) return 1
  const maxOrder = Math.max(
    ...siblings.map(s => (typeof s.sortOrder === 'number' ? s.sortOrder : 0))
  )
  return maxOrder + 1
}

const handleModuleDrop = async (info: any) => {
  const dragKey = info.dragNode?.key as string
  const dropKey = info.node?.key as string

  if (!projectId.value || !dragKey || !dropKey) return
  if (dragKey === 'all') return
  if (dropKey === 'all') return

  // 判断是否是用例节点（key 以 case_ 开头）
  const isDragCase = dragKey.startsWith('case_')
  const isDropCase = dropKey.startsWith('case_')

  if (isDragCase) {
    // 拖动的是用例，需要移动到目标模块
    const caseId = dragKey.replace('case_', '')
    let targetModuleId: string | null = null

    if (isDropCase) {
      // 放到另一个用例上，获取该用例的模块 ID
      const dropCaseId = dropKey.replace('case_', '')
      const dropCase = testCases.value.find(c => c.id === dropCaseId)
      targetModuleId = dropCase?.moduleId || null
    } else {
      // 放到模块上
      targetModuleId = dropKey
    }

    try {
      // 更新用例的 module_id
      await testCaseApi.updateTestCase(projectId.value, caseId, {
        moduleId: targetModuleId
      })
      message.success('用例已移动')

      // 自动展开目标模块
      if (targetModuleId && !expandedModuleKeys.value.includes(targetModuleId)) {
        expandedModuleKeys.value = [...expandedModuleKeys.value, targetModuleId]
      }

      await loadTestCases()
      await loadModuleTree()
    } catch (error) {
      console.error('Failed to move test case:', error)
      message.error('移动用例失败')
    }
  } else {
    // 拖动的是模块
    const dragModule = findModuleById(dragKey)
    if (!dragModule) return

    let newParentId: string | undefined
    if (info.dropToGap) {
      // 落在两个节点之间，保持与目标节点相同的父级
      const dropModule = findModuleById(dropKey)
      newParentId = dropModule?.parentId
    } else {
      // 落在节点上，变为该节点的子模块
      // 如果目标是用例，则获取用例的模块作为新父级
      if (isDropCase) {
        const dropCaseId = dropKey.replace('case_', '')
        const dropCase = testCases.value.find(c => c.id === dropCaseId)
        newParentId = dropCase?.moduleId || undefined
      } else {
        newParentId = dropKey
      }
    }

    try {
      await projectApi.updateModule(projectId.value, dragKey, {
        name: dragModule.name,
        parentId: newParentId,
        sortOrder: dragModule.sortOrder ?? 1,
        description: dragModule.description
      })
      message.success('模块已移动')

      // 自动展开新的父模块
      if (newParentId && !expandedModuleKeys.value.includes(newParentId)) {
        expandedModuleKeys.value = [...expandedModuleKeys.value, newParentId]
      }

      // 刷新用例和模块树以更新用例数量
      await loadTestCases()
      await loadModuleTree()
    } catch (error) {
      console.error('Failed to move module:', error)
      message.error('移动模块失败')
    }
  }
}

const handleModuleContextMenuClick = ({ key }: { key: string }) => {
  const node = moduleContextMenu.node
  moduleContextMenu.visible = false
  if (!node) return

  if (key === 'addModule') {
    handleAddModule(node)
  } else if (key === 'addCase') {
    handleAddCase(node)
  } else if (key === 'rename') {
    handleRenameModule(node)
  } else if (key === 'delete') {
    handleDeleteModule(node)
  } else if (key === 'batchDelete') {
    handleBatchDeleteModules()
  } else if (key === 'deleteCase') {
    handleDeleteCaseFromTree(node)
  } else if (key === 'export') {
    handleExportFromTree(node)
  }
}

// 从树节点删除用例
const handleDeleteCaseFromTree = (node: any) => {
  if (!projectId.value) {
    message.warning('请先选择项目')
    return
  }

  // 从 key 中提取用例 ID（格式：case_xxx）
  const nodeKey = node.key as string
  const caseId = nodeKey.replace('case_', '')
  const caseName = node.title || '该用例'

  Modal.confirm({
    title: '确认删除',
    content: `确定要删除用例"${caseName}"吗？`,
    onOk: async () => {
      try {
        await testCaseApi.deleteTestCase(projectId.value!, caseId)
        message.success('删除成功')
        await loadTestCases()
        await loadModuleTree()
      } catch (error) {
        console.error('Failed to delete case:', error)
        message.error('删除失败')
      }
    }
  })
}

const handleAddModule = (node: any) => {
  if (!projectId.value) {
    message.warning('请先选择项目')
    return
  }

  const parentKey = node.key as string
  const isSpecial = parentKey === 'all' || parentKey === 'unplanned'
  const parentId = isSpecial ? undefined : parentKey
  let inputValue = '新模块'

  Modal.confirm({
    title: '新建模块',
    content: createVNode(Input, {
      defaultValue: inputValue,
      onChange: (e: any) => {
        inputValue = e.target.value
      }
    }),
    async onOk() {
      const name = (inputValue || '').trim()
      if (!name) {
        message.warning('模块名称不能为空')
        return Promise.reject()
      }
      try {
        await projectApi.createModule(projectId.value!, {
          name,
          parentId,
          sortOrder: getNextSortOrder(parentId),
          description: ''
        })
  message.success('模块创建成功')
        await loadModuleTree()
      } catch (error) {
        console.error('创建模块失败', error)
        message.error('模块创建失败')
        return Promise.reject()
      }
    }
  })
}

const handleAddCase = (node: any) => { const key=node?.key as string;void router.push({path:'/test-cases/create',query:{projectId:projectId.value,moduleId:key && !['all','unplanned'].includes(key) ? key : undefined}}) }

const handleRenameModule = (node: any) => {
  if (!projectId.value) {
    message.warning('请先选择项目')
    return
  }

  const key = node.key as string
  if (key === 'all' || key === 'unplanned') {
    message.warning('该节点不支持重命名')
    return
  }

  const module = findModuleById(key)
  if (!module) return

  let inputValue = module.name

  Modal.confirm({
    title: '重命名模块',
    content: createVNode(Input, {
      defaultValue: inputValue,
      onChange: (e: any) => {
        inputValue = e.target.value
      }
    }),
    async onOk() {
      const name = (inputValue || '').trim()
      if (!name) {
        message.warning('模块名称不能为空')
        return Promise.reject()
      }
      try {
        await projectApi.updateModule(projectId.value!, key, {
          name,
          parentId: module.parentId,
          sortOrder: module.sortOrder ?? 1,
          description: module.description
        })
        message.success('重命名成功')
        await loadModuleTree()
      } catch (error) {
        console.error('Failed to rename module:', error)
        message.error('重命名失败')
        return Promise.reject()
      }
    }
  })
}

const handleDeleteModule = (node: any) => {
  if (!projectId.value) {
    message.warning('请先选择项目')
    return
  }

  const key = node.key as string
  if (key === 'all' || key === 'unplanned') {
    message.warning('该节点不支持删除')
    return
  }

  Modal.confirm({
    title: '确认删除',
    content: '删除模块将同时影响其下用例，确定要删除该模块吗？',
    async onOk() {
      try {
        await projectApi.deleteModule(projectId.value!, key)
        message.success('删除模块成功')
        await loadModuleTree()
        await loadTestCases()
      } catch (error) {
        console.error('Failed to delete module:', error)
        message.error('删除模块失败')
        return Promise.reject()
      }
    }
  })
}

const handleBatchDeleteModules = () => {
  if (!projectId.value) {
    message.warning('请先选择项目')
    return
  }
  const keys = selectedModuleKeys.value.filter(
    k => k !== 'all' && k !== 'unplanned'
  )
  if (keys.length === 0) {
    message.info('请选择要删除的模块')
    return
  }

  Modal.confirm({
    title: '批量删除模块',
    content: `确定要删除选中的 ${keys.length} 个模块吗？`,
    async onOk() {
      try {
        await Promise.all(
          keys.map(id => projectApi.deleteModule(projectId.value!, id))
        )
        message.success('批量删除模块成功')
        selectedModuleKeys.value = ['all']
        await loadModuleTree()
        await loadTestCases()
      } catch (error) {
        console.error('Failed to batch delete modules:', error)
        message.error('批量删除模块失败')
        return Promise.reject()
      }
    }
  })
}

// 从模块树右键菜单导出
const handleExportFromTree = async (node: any) => {
  if (!projectId.value) {
    message.warning('请先选择项目')
    return
  }

  try {
    const nodeKey = node.key as string

    // 构建导出参数
    const exportParams: any = {}

    // 如果选中的是模块（不是"全部用例"），则传递模块ID
    if (nodeKey && nodeKey !== 'all') {
      // 获取当前模块及其所有子模块的 ID
      const moduleIds = getModuleAndChildrenIds(nodeKey)
      exportParams.moduleIds = moduleIds.join(',')
    }
    // 如果选中的是"全部用例"，则不传递 moduleIds，导出全部用例

    // 显示加载提示
    const hide = message.loading('正在导出，请稍候...', 0)

    try {
      // 调用导出API
      const blob = await testCaseApi.exportCases(projectId.value, exportParams)

      // 创建下载链接
      const url = window.URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = url

      // 生成文件名
      const timestamp = new Date().toISOString().slice(0, 19).replace(/[:-]/g, '').replace('T', '_')
      const moduleName = nodeKey && nodeKey !== 'all'
        ? (node.title || findModuleById(nodeKey)?.name || '模块')
        : '全部用例'
      link.download = `测试用例_${moduleName}_${timestamp}.xlsx`

      // 触发下载
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
      window.URL.revokeObjectURL(url)

      message.success('导出成功')
    } finally {
      hide()
    }
  } catch (error) {
    console.error('导出失败:', error)
    message.error('导出失败，请稍后重试')
  }
}

// 工具函数
const getLevelColor = (level: string) => {
  const colors: Record<string, string> = {
    P0: 'red',
    P1: 'orange',
    P2: 'blue',
    P3: 'green'
  }
  return colors[level] || 'default'
}

const getReviewResultColor = (result: string) => {
  const colors: Record<string, string> = {
    not_reviewed: 'default',
    pending: 'blue',
    passed: 'green',
    rejected: 'red',
    resubmit: 'orange'
  }
  return colors[result] || 'default'
}

const getReviewResultLabel = (result: string) => {
  const labels: Record<string, string> = {
    not_reviewed: '未评审',
    pending: '待评审',
    passed: '已通过',
    rejected: '不通过',
    resubmit: '重新提审'
  }
  return labels[result] || result
}

const executionResultLabel = (result: string) => ({ not_executed: '未执行', pending: '待执行', running: '执行中', passed: '成功', failed: '失败', error: '错误', blocked: '阻塞', skipped: '跳过' }[result] || result)







// 格式化日期时间（包含时分秒）
const formatDateTime = (date: string) => {
  if (!date) return '-'
  return dayjs(date).format('YYYY-MM-DD HH:mm:ss')
}

// 获取显示名称（将用户ID转换为显示名称）
const getDisplayName = (userId: string) => {
  if (!userId) return '-'
  // 如果是当前登录用户，显示当前用户名
  if (userStore.user?.id === userId) {
    return userStore.user.username || userStore.user.email || '当前用户'
  }
  // 其他情况显示简短ID或默认名称
  return userId.length > 8 ? userId.substring(0, 8) + '...' : userId
}

// 生命周期
watch(viewLayout, () => { selection.clear() }, { flush:'sync' })
watch(
  () => mindScope.value,
  () => {
    testCases.value=[];modules.value=[];allCasesForTree.value=[];moduleTreeData.value=[];recycleTotal.value=0
    if (projectId.value) {
      if (!filterSaving.value) filterDrawerVisible.value = false
      advancedFilters.value = []; filterLogic.value = 'and'; viewMode.value='all'; resetBasicSearch()
      selection.clear();selectedModuleKeys.value=['all'];detailCaseVisible.value=false;recycleVisible.value=route.query.view === 'recycle';templateVisible.value=false;pagination.current=1
      loadTestCases()
      loadModuleTree()
      loadFilterFields()
    }
  },
  { immediate: true }
)

// 键盘事件处理函数
const handleKeyDown = (e: KeyboardEvent) => {
  if (e.key === 'Shift') {
    isShiftKeyPressed.value = true
  }
}

const handleKeyUp = (e: KeyboardEvent) => {
  if (e.key === 'Shift') {
    isShiftKeyPressed.value = false
  }
}

onMounted(async () => {
  // 确保项目列表已加载
  if (projects.value.length === 0) {
    await projectStore.fetchProjects()
  }
  const linkedProject = projects.value.find(p=>p.id===route.query.projectId)
  if(linkedProject) projectStore.setCurrentProject(linkedProject)
  if(typeof route.query.caseId === 'string'){ viewingCaseId.value=route.query.caseId; detailCaseVisible.value=true }
  // 如果没有当前项目，设置第一个项目为当前项目
  if (!projectStore.currentProject && projects.value.length > 0) {
    projectStore.setCurrentProject(projects.value[0])
  }
  if (projectId.value) {
    loadTestCases()
    loadModuleTree()
    loadFilterFields()
  }
  // 添加全局键盘事件监听器
  window.addEventListener('keydown', handleKeyDown)
  window.addEventListener('keyup', handleKeyUp)
})

onUnmounted(() => {
  // 移除全局键盘事件监听器
  window.removeEventListener('keydown', handleKeyDown)
  window.removeEventListener('keyup', handleKeyUp)
})
const paginationTotal = (total: number) => `共 ${total} 条`
</script>

<style scoped>
.test-cases-container {
  display:flex;flex-direction:column;min-height:0;
  height: 100%;
  background: #fff;
  }

.test-cases-layout {
  flex:1;min-height:0;
}

.module-tree-sider {
  background: #fff;
  border-right: 1px solid #f0f0f0;
  padding:0;
  overflow:hidden;
  }

.module-tree-body { height:calc(100% - 40px); padding:16px; overflow:auto; }
.root-module-title { display:flex !important; align-items:center; max-width:none !important; width:100%; overflow:visible !important; }
.root-module-actions { margin-left:auto; }
.root-module-actions :deep(.ant-btn) { padding:2px; width:24px; }
.recycle-module-entry { display:flex; align-items:center; gap:8px; width:100%; height:40px; padding:0 24px; border:0; border-top:1px solid var(--ms-border); background:#fff; color:var(--ms-text-secondary); cursor:pointer; font:inherit; }
.recycle-module-entry:hover,.recycle-module-entry.active { background:var(--ms-primary-soft); color:var(--primary-color); }
.recycle-total { margin-left:auto; color:var(--ms-text-muted); }
.module-search {
  margin-bottom: 16px;
}

.count-badge {
  color: #999;
  font-size: 12px;
  }

/* 树节点标题样式 - 单行显示 */
.tree-node-title {
  display: inline-block;
  max-width: 180px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  vertical-align: middle;
  text-align: left;
  }

/* 树容器横向滚动 */
.module-tree-sider :deep(.ant-tree) {
  overflow-x: auto;
  white-space: nowrap;
}

.module-tree-sider :deep(.ant-tree-treenode) {
  white-space: nowrap;
  display: flex !important;
  align-items: center;
}

.module-tree-sider :deep(.ant-tree-node-content-wrapper) {
  display: inline-flex !important;
  align-items: center;
  flex: 1;
  min-width: 0;
  }

/* 用例节点样式 */
.module-tree-sider :deep(.ant-tree-title) {
  display: inline-block;
  text-align: left;
  width: 100%;
  }

/* 右键菜单样式 - Windows 风格 */
.module-context-menu {
  position: fixed;
  z-index: 1000;
  background: #fff;
  border: 1px solid #d9d9d9;
  border-radius: 4px;
  box-shadow: 0 3px 6px -4px rgba(0, 0, 0, 0.12),
              0 6px 16px 0 rgba(0, 0, 0, 0.08),
              0 9px 28px 8px rgba(0, 0, 0, 0.05);
  padding: 4px 0;
  min-width: 140px;
  }

.module-context-menu :deep(.ant-menu) {
  border: none;
  box-shadow: none;
  background: transparent;
  }

.module-context-menu :deep(.ant-menu-item) {
  height: 32px;
  line-height: 32px;
  margin: 0 !important;
  padding: 0 12px !important;
  border-radius: 0;
  }

.module-context-menu :deep(.ant-menu-item:hover) {
  background-color: #f5f5f5;
  }

.module-context-menu :deep(.ant-menu-item-divider) {
  margin: 4px 0;
  background-color: #f0f0f0;
}

.cases-content {
  display: flex;
  flex-direction: column;
  background: #fff;
  margin: 0;
  overflow: hidden;
  height: 100%;
}

/* 对齐MS左侧创建、右侧搜索/视图/筛选的工作区工具栏 */
.fixed-toolbar { display:flex; align-items:center; justify-content:space-between; gap:16px; flex-wrap:wrap; padding:16px 16px 0; flex-shrink:0; background:#fff; }
.toolbar-create,.toolbar-filter { display:flex; align-items:center; gap:8px; flex-wrap:wrap; }
.toolbar-create { gap:12px; }
.table-heading { display:flex; align-items:center; justify-content:space-between; padding:12px 16px 4px; flex-shrink:0; }
.module-heading { overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }
.table-card :deep(.ant-card-body) { padding:0; }
.table-card { border:0; }
.inline-case-level { min-width:72px; width:100%; }
.inline-case-module { width:100%; }
.inline-case-level :deep(.ant-select-selector),.inline-case-module :deep(.ant-select-selector) { padding:0 4px !important; }
@media(max-width:900px) { .toolbar-filter { width:100%; } .toolbar-filter .ant-input-search { width:100% !important; } .toolbar-filter .case-view-select { flex:1; min-width:120px; } }

/* 可滚动表格内容区域 */
.scrollable-table-content {
  flex: 1;
  overflow-y: auto;
  padding: 0 16px;
}

.filter-panel {
  margin-bottom: 16px;
  }

.table-card {
  margin-bottom: 16px;
  }

/* 表格单行显示，不换行 */
.table-card :deep(.ant-table-cell) {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* 用例链接样式 */
.case-link {
  color: var(--primary-color);
  cursor: pointer;
  }

.case-link:hover {
  text-decoration: underline;
}

.batch-actions {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  max-width: 100%;
  gap: 8px;
}

.batch-actions [aria-label="用例选择数量"] { white-space: nowrap; }

/* 固定底部分页器和批量操作栏 */
.fixed-footer {
  position: sticky;
  bottom: 0;
  z-index: 100;
  background: #fff;
  border-top: 1px solid #f0f0f0;
  padding: 12px 16px;
  margin-bottom: 20px;
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  justify-content: space-between;
  align-items: center;
  flex-shrink: 0;
}

/* 响应式设计 */
@media (max-width: 1200px) {
  .module-tree-sider {
    width: 200px;
  }
}

@media (max-width: 768px) {
  .toolbar {gap:8px;align-items:center;}
  .fixed-toolbar{padding:10px}
  .module-tree-sider{position:absolute;inset:100px auto 0 0;z-index:110;box-shadow:4px 0 18px #0002}
  .fixed-footer{flex-wrap:wrap;gap:12px;overflow:auto}
  .scrollable-table-content{padding:0 8px}
}

/* 修复表格固定列重叠问题 */
:deep(.ant-table-cell-fix-right),
:deep(.ant-table-cell-fix-left) {
  background: #fff !important;
  z-index: 10 !important;
}

:deep(.ant-table-thead > tr > th.ant-table-cell-fix-right),
:deep(.ant-table-thead > tr > th.ant-table-cell-fix-left) {
  background: #fafafa !important;
  z-index: 20 !important;
}

:deep(.ant-table-tbody > tr:hover > td.ant-table-cell-fix-right),
:deep(.ant-table-tbody > tr:hover > td.ant-table-cell-fix-left) {
  background: #fafafa !important;
}
</style>
