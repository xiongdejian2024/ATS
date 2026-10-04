<template>
  <a-layout class="main-layout">
    <a-layout-header class="layout-header">
      <a class="platform-brand" href="/dashboard" @click.prevent="navigateProjectPage('/dashboard')" aria-label="ATS 首页">
        <ExperimentOutlined /><span>ATS</span>
      </a>
      <a-button type="text" class="collapse-btn" aria-label="切换导航菜单"
        :icon="h(collapsed ? MenuUnfoldOutlined : MenuFoldOutlined)" @click="toggleCollapsed" />
      <a-select :value="currentProjectId" :options="projects.map(project => ({ value: project.id, label: project.name }))"
        class="global-project-select" :bordered="false" show-search option-filter-prop="label"
        placeholder="选择项目" aria-label="当前项目" @change="changeGlobalProject" />
      <nav class="context-tabs" aria-label="当前模块导航">
        <a v-for="tab in contextTabs" :key="tab.path" :href="projectPageHref(tab.path)" :class="{ active: route.path === tab.path || route.path.startsWith(tab.path + '/') }"
          :aria-current="route.path === tab.path ? 'page' : undefined" @click.prevent="navigateProjectPage(tab.path)">{{ tab.title }}</a>
      </nav>
        <div class="header-right">
          <a-button type="text" @click="router.push('/ai-assistant')">AI 辅助</a-button>
          <!-- 通知 -->
          <a-dropdown>
            <a-badge :count="unreadCount">
              <a-button type="text" aria-label="站内通知" :icon="h(BellOutlined)" />
            </a-badge>
            <template #overlay>
              <a-menu>
                <a-menu-item v-for="notification in notifications" :key="notification.id" @click="readNotification(notification)">
                  <div class="notification-item">
                    <div class="notification-title">{{ notification.title }}</div>
                    <div class="notification-content">{{ notification.content }}</div>
                    <div class="notification-time">{{ formatTime(notification.createdAt) }}</div>
                  </div>
                </a-menu-item>
                <a-menu-divider />
                <a-menu-item key="all-notifications">
                  <a @click="viewAllNotifications">全部标为已读</a>
                </a-menu-item>
              </a-menu>
            </template>
          </a-dropdown>

          <!-- 用户菜单 -->
          <a-dropdown>
            <a-avatar  :icon="h(UserOutlined)" />
            <template #overlay>
              <a-menu>
                <a-menu-item key="profile" @click="handleProfile">
                  <template #icon><UserOutlined /></template>
                  个人中心
                </a-menu-item>
                <a-menu-item key="settings" @click="handleSettings">
                  <template #icon><SettingOutlined /></template>
                  系统设置
                </a-menu-item>
                <a-menu-divider />
                <a-menu-item key="logout" @click="handleLogout">
                  <template #icon><LogoutOutlined /></template>
                  退出登录
                </a-menu-item>
              </a-menu>
            </template>
          </a-dropdown>
        </div>

    </a-layout-header>
    <a-layout class="layout-body">
      <a-layout-sider v-model:collapsed="collapsed" :trigger="null" collapsible class="layout-sider" :width="200" :collapsed-width="72">
        <a-menu v-model:selectedKeys="selectedKeys" v-model:openKeys="openKeys" mode="inline" class="layout-menu">
          <a-menu-item v-for="item in menuItems" :key="item.key" @click="handleMenuClick(item)">
            <template #icon><component :is="item.icon" /></template>{{ item.title }}
          </a-menu-item>
        </a-menu>
      </a-layout-sider>
      <div v-if="isMobile && !collapsed" class="mobile-mask" role="button" tabindex="0" aria-label="关闭导航菜单"
        @click="collapsed = true" @keydown.enter="collapsed = true" />
      <a-layout-content class="layout-content">
        <div class="page-breadcrumb"><span>{{ isCaseWorkspace ? '测试用例' : isPlanWorkspace ? '测试计划' : route.meta?.title || '仪表盘' }}</span>
          <template v-if="isCaseWorkspace"><span class="breadcrumb-separator">/</span><span>{{ route.path === '/case-reviews' ? '评审' : '用例' }}</span></template>
          <template v-else-if="isPlanWorkspace"><span class="breadcrumb-separator">/</span><span>{{ route.path.startsWith('/test-plan-reports') ? '计划报告' : '计划' }}</span></template>
        </div>
        <div class="page-workspace"><router-view /></div>
      </a-layout-content>
    </a-layout>
  </a-layout>
</template>

<script setup lang="ts">
import { ref, computed, h, onMounted, onUnmounted, watch } from 'vue';
import { useWindowSize } from '@vueuse/core';
import { useRouter, useRoute, isNavigationFailure } from 'vue-router';
import { message } from 'ant-design-vue';
import { MenuFoldOutlined, MenuUnfoldOutlined, DashboardOutlined, ProjectOutlined, ExperimentOutlined, ScheduleOutlined, AppstoreOutlined, SettingOutlined, BellOutlined, UserOutlined, LogoutOutlined } from '@ant-design/icons-vue';
import { useUserStore } from '@/stores/user';
import { useProjectStore } from '@/stores/project';
import dayjs from 'dayjs'
import { notificationApi } from '@/api/notification'
import type { Notification } from '@/types';

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()
const projectStore = useProjectStore()

const collapsed = ref(false)
const { width: windowWidth } = useWindowSize()
const isMobile = computed(() => windowWidth.value <= 768)
watch(isMobile, value => { collapsed.value = value }, { immediate: true })
const selectedKeys = ref<string[]>([])
const openKeys = ref<string[]>([])
const currentProjectId = computed(() => projectStore.currentProject?.id)
const isCaseWorkspace = computed(() => route.path.startsWith('/test-cases') || route.path.startsWith('/case-reviews'))
const isPlanWorkspace = computed(() => route.path.startsWith('/test-plans') || route.path.startsWith('/test-plan-reports'))
const projectPageHref = (path: string) => router.resolve({ path, query: currentProjectId.value ? { projectId: currentProjectId.value } : {} }).href
const navigateProjectPage = async (path: string) => { const failure=await router.push(projectPageHref(path));if(isNavigationFailure(failure))selectedKeys.value=menuSelection(route.path) }
const contextTabs = computed(() => isCaseWorkspace.value ? [{ path: '/test-cases', title: '用例' }, { path: '/case-reviews', title: '评审' }] : isPlanWorkspace.value ? [{path:'/test-plans',title:'计划'},{path:'/test-plan-reports',title:'计划报告'}] : [])
async function changeGlobalProject(id: string) {
  const target = projectStore.projects.find(item => item.id === id)
  if (!target) return
  try {
    // 切换项目时移除旧项目实体链接，不能把旧用例/批次带入新项目。
    const path=['CaseEdit','CaseCreated'].includes(String(route.name)) ? '/test-cases' : ['TestPlanDetailPage','PlanFunctionalExecution'].includes(String(route.name)) ? '/test-plans' : route.name==='TestPlanReportDetail' ? '/test-plan-reports' : route.path
    const failure=await router.replace({ path, query: { projectId: id } })
    if(isNavigationFailure(failure)) { console.info('项目切换已取消，保留原项目'); return }
    projectStore.setCurrentProject(target)
    console.info('已切换当前项目', { projectId: id })
  } catch (error) {
    console.error('切换项目失败', error)
    message.error('切换项目失败')
  }
}

const notifications = ref<Notification[]>([])
const refreshNotifications = async () => {
  try { notifications.value = (await notificationApi.getNotifications({ size: 1000 })).items }
  catch (error) { console.error('加载通知失败', error); notifications.value = [] }
}
const readNotification = async (item: Notification) => { await notificationApi.markAsRead(item.id); await refreshNotifications() }
let inboxTimer: ReturnType<typeof setInterval> | undefined
onMounted(() => { refreshNotifications(); inboxTimer = setInterval(refreshNotifications, 5000) })
onUnmounted(() => { if (inboxTimer) clearInterval(inboxTimer) })

const unreadCount = computed(() =>
  notifications.value.filter(n => !n.isRead).length
)

const menuItems = [
  {
    key: 'dashboard',
    title: '仪表盘',
    icon: DashboardOutlined,
    path: '/dashboard'
  },
  {
    key: 'projects',
    title: '项目管理',
    icon: ProjectOutlined,
    path: '/projects'
  },
  {
    key: 'test-cases',
    title: '测试用例',
    icon: ExperimentOutlined,
    path: '/test-cases'
  },
  {
    key: 'test-plans',
    title: '测试计划',
    icon: ScheduleOutlined,
    path: '/test-plans'
  },
  {
    key: 'test-suites',
    title: '测试套',
    icon: AppstoreOutlined,
    path: '/test-suites'
  },
  { key: 'task-center', title: '测试任务', icon: ScheduleOutlined, path: '/task-center' },
  { key: 'ai-assistant', title: 'AI 辅助', icon: ExperimentOutlined, path: '/ai-assistant' },
  {
    key: 'executions', title: '执行记录', icon: ScheduleOutlined, path: '/executions'
  },
  {
    key: 'reports', title: '测试报告', icon: ScheduleOutlined, path: '/reports'
  },
  {
    key: 'environments',
    title: '环境管理',
    icon: SettingOutlined,
    path: '/environments'
  }
]


const projects = computed(() => projectStore.projects)
function menuSelection(path:string){if(path.startsWith('/case-reviews'))return ['test-cases'];if(path.startsWith('/test-plan-reports'))return ['test-plans'];const selected=menuItems.find(item=>path===item.path||path.startsWith(item.path+'/'));return selected?[selected.key]:[]}
watch(() => route.path, path => { selectedKeys.value=menuSelection(path) }, { immediate: true })



const toggleCollapsed = () => {
  collapsed.value = !collapsed.value
}

const handleMenuClick = (item: any) => {
  if (item.path.includes('/projects/') && !currentProjectId.value) {
    message.warning('请先选择一个项目')
    return
  }
  navigateProjectPage(item.path)
  if (isMobile.value) collapsed.value = true
}



const handleProfile = () => {
  router.push('/profile')
}

const handleSettings = () => {
  message.info('系统设置功能开发中...')
}

const handleLogout = async () => {
  try {
    await userStore.logout()
    message.success('已成功退出')
    router.push('/login')
  } catch (error) {
    message.error('退出失败')
  }
}

const formatTime = (time: string) => {
  return dayjs(time).format('YYYY-MM-DD HH:mm')
}

const viewAllNotifications = () => {
  notificationApi.markAllAsRead().then(refreshNotifications)
}

// 实体深链接与全局项目选择保持一致，异步加载项目后再次核对。
watch(()=>[route.query.projectId,projectStore.projects],()=>{
  const linked=projectStore.projects.find(project=>project.id===route.query.projectId)
  if(linked&&linked.id!==currentProjectId.value)projectStore.setCurrentProject(linked)
},{immediate:true})

// 初始化
onMounted(async () => {
  // 获取项目列表
  await projectStore.fetchProjects()

  // 设置当前项目
  if (projects.value.length > 0 && !currentProjectId.value) {
    const linked = projects.value.find(project => project.id === route.query.projectId)
    projectStore.setCurrentProject(linked || projects.value[0])
  }

  // 设置当前菜单选中状态
  selectedKeys.value=menuSelection(route.path)
})
</script>


<style scoped>
.main-layout { height:100vh; background:var(--ms-page-bg); }
.layout-header { height:56px; line-height:normal; padding:0 16px 0 0; display:flex; align-items:center; flex-shrink:0; background:#fff; border-bottom:1px solid var(--ms-border); z-index:1000; }
.platform-brand { display:flex; gap:8px; align-items:center; width:200px; flex-shrink:0; padding:0 16px; color:var(--primary-color); font-size:16px; font-weight:700; }
.platform-brand .anticon { font-size:28px; }
.collapse-btn { width:32px; height:32px; padding:0; flex-shrink:0; color:var(--ms-text-secondary); }
.global-project-select { width:200px; flex-shrink:0; }
.context-tabs { display:flex; height:56px; align-items:stretch; flex:1; gap:24px; min-width:0; padding-left:16px; }
.context-tabs a { display:flex; align-items:center; border-bottom:2px solid transparent; color:var(--ms-text-secondary); padding:0 4px; white-space:nowrap; }
.context-tabs a.active { color:var(--primary-color); border-bottom-color:var(--primary-color); font-weight:500; }
.header-right { display:flex; align-items:center; gap:8px; margin-left:auto; flex-shrink:0; }
.layout-body { min-height:0; flex:1; }
.layout-sider { background:#fff !important; border-right:1px solid var(--ms-border); overflow-y:auto; }
.layout-menu { border-right:0; padding:8px; }
:deep(.layout-menu .ant-menu-item) { height:40px; line-height:40px; border-radius:4px; margin:4px 0; width:100%; }
:deep(.layout-menu .ant-menu-item-selected) { background:var(--ms-primary-soft); color:var(--primary-color); }
.layout-content { display:flex; flex-direction:column; min-width:0; min-height:0; overflow:hidden; padding:0 16px 16px; }
.page-breadcrumb { display:flex; align-items:center; gap:8px; height:40px; flex-shrink:0; font-size:12px; color:var(--ms-text-secondary); }
.breadcrumb-separator { color:var(--ms-text-muted); }
.page-workspace { flex:1; min-height:0; overflow:auto; }
.notification-item { max-width:280px; padding:8px 0; }
.notification-title { font-weight:500; margin-bottom:4px; color:var(--ms-text); }
.notification-content { font-size:12px; color:var(--ms-text-secondary); margin-bottom:4px; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }
.notification-time { font-size:12px; color:var(--ms-text-muted); }
@media(max-width:768px) {
  .platform-brand { width:62px; padding:0 8px; gap:4px; }
  .platform-brand .anticon { display:none; }
  .layout-header { padding-right:8px; }
  .global-project-select { width:104px; }
  .context-tabs { gap:8px; padding-left:4px; font-size:12px; }
  .header-right { gap:0; }
  .header-right > .ant-btn { display:none; }
  .layout-sider { position:fixed; left:0; top:56px; bottom:0; height:calc(100vh - 56px); z-index:999; transition:transform .2s ease; }
  .layout-sider.ant-layout-sider-collapsed { transform:translateX(-100%); }
  .mobile-mask { position:fixed; inset:56px 0 0; background:rgb(0 0 0 / 35%); z-index:998; }
  .layout-content { padding:0 8px 8px; }
}
</style>
