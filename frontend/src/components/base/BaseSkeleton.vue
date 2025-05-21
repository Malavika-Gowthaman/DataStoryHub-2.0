<template>
  <Skeleton v-bind="props"> </Skeleton>
</template>

<script lang="ts" setup>
import { Skeleton, type SkeletonProps } from "primevue";
const props = defineProps<SkeletonProps>();
</script>
