<template>
  <PlanFunctionalCases
    v-if="category === 'functional'"
    :plan="plan"
    :can-edit="canEdit"
    @changed="emit('changed')"
  />
  <PlanAutomationCases
    v-else
    :key="`${plan.id}:${category}`"
    :plan="plan"
    :category="category"
    :can-edit="canEdit"
    @changed="emit('changed')"
  />
</template>
<script setup lang="ts">
import type { TestPlan } from "@/types";
import type { PlanNode } from "@/api/planTree";
import PlanFunctionalCases from "./PlanFunctionalCases.vue";
import PlanAutomationCases from "./PlanAutomationCases.vue";
defineProps<{
  plan: TestPlan;
  category: PlanNode["category"];
  canEdit: boolean;
}>();
const emit = defineEmits<{ changed: [] }>();
</script>
