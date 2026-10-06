<template>
  <svg
    viewBox="0 0 24 24"
    width="16"
    height="16"
    aria-hidden="true"
    fill="none"
    stroke="currentColor"
    stroke-width="1.5"
    stroke-linejoin="round"
  >
    <template v-if="kind === 'preview'">
      <path d="M8 3H3v5M16 3h5v5M3 16v5h5M21 16v5h-5" />
      <rect x="7" y="7" width="10" height="10" rx="1" />
    </template>
    <template v-else>
      <rect x="2" y="5" width="20" height="14" rx="2" />
      <path d="M5 9h2m2 0h2m2 0h2m2 0h2M5 12h2m2 0h2m2 0h2m2 0h2M7 16h10" />
    </template>
  </svg>
</template>
<script setup lang="ts">
defineProps<{ kind: "preview" | "keyboard" }>();
</script>
