<template>
  <a-config-provider
    :locale="zhCN"
    :theme="{
      token: {
        colorPrimary: '#811fa3',
        colorLink: '#811fa3',
        colorLinkHover: '#6e1a8b',
        colorLinkActive: '#6e1a8b',
        colorText: '#1d2129',
        colorTextSecondary: '#4e5969',
        colorBorder: '#e5e6eb',
        borderRadius: 4,
        fontSize: 14
      }
    }"
  >
    <router-view />
  </a-config-provider>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import zhCN from 'ant-design-vue/es/locale/zh_CN'
import { useUserStore } from '@/stores/user'
import { useRouter } from 'vue-router'

const userStore = useUserStore()
const router = useRouter()

onMounted(async () => {
  await userStore.checkAuth()
  if (!userStore.isAuthenticated && router.currentRoute.value.path !== '/login') {
    router.push('/login')
  }
})
</script>

<style>
#app {
  height: 100vh;
  width: 100vw;
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Helvetica Neue', Arial, 'PingFang SC', sans-serif;
}
</style>
