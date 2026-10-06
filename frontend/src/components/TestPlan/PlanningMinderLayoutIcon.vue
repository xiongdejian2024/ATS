<template>
  <svg
    viewBox="0 0 24 24"
    width="16"
    height="16"
    aria-hidden="true"
    fill="none"
    stroke="currentColor"
    stroke-width="1.5"
    stroke-linecap="round"
    stroke-linejoin="round"
  >
    <template v-if="mode === 'right'">
      <rect x="2" y="9" width="6" height="6" rx="1" />
      <path d="M8 12h5M13 5v14M13 5h3M13 19h3" />
      <rect x="16" y="2" width="6" height="6" rx="1" />
      <rect x="16" y="16" width="6" height="6" rx="1" />
    </template>
    <template v-else-if="mode === 'default'">
      <rect x="9" y="9" width="6" height="6" rx="1" />
      <path d="M6 12h3M15 12h3M6 5v14M18 5v14M2 5h4M2 19h4M18 5h4M18 19h4" />
    </template>
    <template v-else>
      <rect x="2" y="2" width="6" height="6" rx="1" />
      <path d="M5 8v11h9M5 12h9" />
      <rect x="14" y="9" width="7" height="5" rx="1" />
      <rect x="14" y="17" width="7" height="5" rx="1" />
    </template>
  </svg>
</template>
<script setup lang="ts">
import type { MinderMode } from "./planMinderView";
defineProps<{ mode: MinderMode }>();
</script>
