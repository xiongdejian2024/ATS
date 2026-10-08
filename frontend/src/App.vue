<template>
  <a-config-provider :locale="zhCN" :theme="atsBlueTheme">
    <router-view />
  </a-config-provider>
</template>

<script setup lang="ts">
import { onMounted } from "vue";
import zhCN from "ant-design-vue/es/locale/zh_CN";
import { atsBlueTheme } from "@/styles/theme";
import { useUserStore } from "@/stores/user";
import { useRouter } from "vue-router";

const userStore = useUserStore();
const router = useRouter();

onMounted(async () => {
  await userStore.checkAuth();
  if (
    !userStore.isAuthenticated &&
    router.currentRoute.value.path !== "/login"
  ) {
    router.push("/login");
  }
});
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
  font-family: "Helvetica Neue", Arial, "PingFang SC", sans-serif;
}
</style>
